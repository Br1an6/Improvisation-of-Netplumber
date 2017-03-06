/*
   Copyright 2012 Google Inc.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   Author: peyman.kazemian@gmail.com (Peyman Kazemian)
*/

#include "rpc_handler.h"
#include <ctime>
extern "C" {
  #include "../headerspace/hs.h"
}

using namespace Json::Rpc;
using namespace std;

namespace net_plumber {

array_t *val_to_array(const Json::Value &val) {
  if (val.isNull()) {
    return NULL;
  } else {
    return array_from_str(val.asCString());
  }
}

hs *val_to_hs(const Json::Value &val, int len) {
  hs *res = hs_create (len);
  if (val.isString()) hs_add (res, val_to_array(val));
  else if (val.isObject()) {
    const Json::Value &list = val["list"];
    const Json::Value &diff = val["diff"];
    hs_vec *v = &res->list;
    for (Json::Value::ArrayIndex i = 0; i < list.size(); i++) {
      hs_vec_append(v, val_to_array(list[i]), false);

      const Json::Value &d = diff[i];
      hs_vec *v_diff = &v->diff[i];
      for (Json::Value::ArrayIndex j = 0; j < d.size(); j++)
        hs_vec_append(v_diff, val_to_array(d[j]), true);
    }
  }
  return res;
}

List_t val_to_list(const Json::Value &val) {
  uint32_t elems[val.size()];
  for (unsigned i = 0; i < val.size(); i++)
    elems[i] = val[i].asUInt();
  return make_sorted_list_from_array(val.size(),elems);
}


Condition *val_to_path(const Json::Value &pathlets) {
  PathCondition *path = new PathCondition();
  for (Json::Value::ArrayIndex i = 0; i < pathlets.size(); i++) {
    const Json::Value &val = pathlets[i];
    const char *type = val["type"].asCString();
    PathSpecifier *p = NULL;
    if (!strcasecmp(type, "port")) p = new PortSpecifier(val["port"].asUInt());
    else if (!strcasecmp(type, "table")) p = new TableSpecifier(val["table"].asUInt());
    else if (!strncasecmp(type, "next", 4) || !strncasecmp(type, "last", 4)) {
      const Json::Value &arg = !strcasecmp(type + 5, "ports") ? val["ports"] : val["tables"];
      List_t l = val_to_list(arg);
      if (!strcasecmp(type, "next_ports")) p = new NextPortsSpecifier(l);
      else if (!strcasecmp(type, "next_tables")) p = new NextTablesSpecifier(l);
      else if (!strcasecmp(type, "last_ports")) p = new LastPortsSpecifier(l);
      else if (!strcasecmp(type, "last_tables")) p = new LastTablesSpecifier(l);
    }
    else if (!strcasecmp(type, "skip")) p = new SkipNextSpecifier();
    else if (!strcasecmp(type, "end")) p = new EndPathSpecifier();
    path->add_pathlet(p);
  }
  return path;
}

Condition *val_to_cond(const Json::Value &val, int length) {
  if (val.isNull()) return NULL;
  const char *type = val["type"].asCString();
  if (!strcasecmp(type, "true")) return new TrueCondition();
  if (!strcasecmp(type, "false")) return new FalseCondition();
  if (!strcasecmp(type, "path")) return val_to_path(val["pathlets"]);
  if (!strcasecmp(type, "header")) return new HeaderCondition(val_to_hs(val["header"], length));
  if (!strcasecmp(type, "not")) return new NotCondition(val_to_cond(val["arg"], length));
  if (!strcasecmp(type, "and") || !strcasecmp(type, "or")) {
    Condition *c1 = val_to_cond(val["arg1"], length);
    Condition *c2 = val_to_cond(val["arg2"], length);
    if (!strcasecmp(type, "and")) return new AndCondition(c1, c2);
    else return new OrCondition(c1, c2);
  }
  return NULL;
}


typedef bool (RpcHandler::*RpcFn) (const Json::Value &, Json::Value &);

void RpcHandler::initServer (TcpServer &server) {
#define FN(NAME) {#NAME, &RpcHandler::NAME}
  struct { string name; RpcFn fn; } methods[] = {
    FN(init), FN(destroy),
    FN(add_link), FN(remove_link),
    FN(add_table), FN(remove_table),
    FN(add_rule), FN(remove_rule),
    FN(add_source), FN(remove_source),
    FN(add_source_probe), FN(remove_source_probe),
    FN(print_table)
  };
  int n = sizeof methods / sizeof *methods;
  for (int i = 0; i < n; i++)
    server.AddMethod (new RpcMethod<RpcHandler> (*this, methods[i].fn, methods[i].name));
#undef FN
}

#define PROTO(NAME) \
  bool RpcHandler::NAME (const Json::Value &req, Json::Value &resp) { \
    cout << "Recv: " << req << endl; \
    resp["id"] = req["id"]; resp["jsonrpc"] = req["jsonrpc"]; \
    clock_t start, end; start = clock();

#define FINI do { \
    cout << "Send: " << resp << endl; \
    return true; \
  } while (0)
#define RETURN(VAL) \
  end = clock(); \
  cout << "Event handling time: " << (double(end - start) * 1000 / CLOCKS_PER_SEC) << "ms." << endl; \
  do { resp["result"] = (VAL); FINI; } while (0)

#define ERROR(MSG) do { \
    resp["error"]["code"] = 1; resp["error"]["message"] = (MSG); FINI; \
  } while (0)

#define PARAM(NAME) req["params"][#NAME]
#define VOID Json::Value::null

PROTO(init)
  length = PARAM(length).asInt();
  if (netPlumber) ERROR ("Already initialized.");
  netPlumber = new NetPlumber(length);
  RETURN(VOID);
}

PROTO(destroy)
  delete netPlumber;
  netPlumber = NULL;
  RETURN(VOID);
}

PROTO(add_link)
  uint32_t from = PARAM(from_port).asUInt();
  uint32_t to = PARAM(to_port).asUInt();
  netPlumber->add_link(from, to);
  RETURN(VOID);
}

PROTO(remove_link)
  uint32_t from = PARAM(from_port).asUInt();
  uint32_t to = PARAM(to_port).asUInt();
  netPlumber->remove_link(from, to);
  RETURN(VOID);
}

PROTO(add_table)
  uint32_t id = PARAM(id).asUInt();
  List_t ports = val_to_list(PARAM(in));
  netPlumber->add_table(id,ports);
  RETURN(VOID);
}

PROTO(remove_table)
  uint32_t id = PARAM(id).asUInt();
  netPlumber->remove_table(id);
  RETURN(VOID);
}

PROTO(add_rule)
  uint32_t table = PARAM(table).asUInt();
  int index = PARAM(index).asInt();
  List_t in = val_to_list(PARAM(in));
  List_t out = val_to_list(PARAM(out));
  array_t *match = val_to_array(PARAM(match));
  array_t *mask = val_to_array(PARAM(mask));
  array_t *rw = val_to_array(PARAM(rw));
  uint64_t ret = netPlumber->add_rule(table, index, in, out, match, mask, rw);
  RETURN((Json::Value::UInt64) ret);
}

PROTO(remove_rule)
  uint64_t node = PARAM(node).asUInt64();
clock_t st, en; st = clock();
  netPlumber->remove_rule(node);
en = clock();
cout << "Only deleting takes: " << (double(en - st) * 1000000 / CLOCKS_PER_SEC) << "us." << endl; \


  RETURN(VOID);
}

PROTO(add_source)
  hs *h = val_to_hs(PARAM(hs), length);
  List_t ports = val_to_list(PARAM(ports));
  uint64_t ret = netPlumber->add_source(h, ports);
  RETURN((Json::Value::UInt64) ret);
}

PROTO(remove_source)
  uint64_t id = PARAM(id).asUInt64();
  netPlumber->remove_source(id);
  RETURN(VOID);
}

PROTO(add_source_probe)
  List_t ports = val_to_list(PARAM(ports));
  PROBE_MODE mode = !strcasecmp(PARAM(mode).asCString(), "universal") ? UNIVERSAL : EXISTENTIAL;
  Condition *filter = val_to_cond(PARAM(filter), length);
  Condition *test = val_to_cond(PARAM(test), length);
  uint64_t ret = netPlumber->add_source_probe(ports, mode, filter, test, NULL, NULL);
  RETURN((Json::UInt64) ret);
}

PROTO(remove_source_probe)
  uint64_t id = PARAM(id).asUInt64();
  netPlumber->remove_source_probe(id);
  RETURN(VOID);
}

PROTO(print_table)
  uint64_t id = PARAM(id).asUInt();
  netPlumber->print_table(id);
  RETURN(VOID);
}

}

