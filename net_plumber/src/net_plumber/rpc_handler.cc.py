'''
   Copyright 2012 Google Inc.

   Licensed under the Apache License, 2.0 (the "License")
   you may not use self file except in compliance with the License.
   You may obtain a copy of the License at

       http:#www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   Author: peyman.kazemian@gmail.com (Peyman Kazemian)
'''

#include "rpc_handler.h"
#include <ctime>
extern "C"  #include "../headerspace/hs.h"


using namespace Json.Rpc
using namespace std

namespace net_plumber
array_t *val_to_array( Json.Value &val)  if val.isNull():    return NULL
  } else:
    return array_from_str(val.asCString())



hs *val_to_hs( Json.Value &val, len)  hs *res = hs_create (len)
  if val.isString()) hs_add (res, val_to_array(val):
  elif val.isObject():     Json.Value &list = val["list"]
     Json.Value &diff = val["diff"]
    hs_vec *v = &res.list
    for (i = 0; i < list.size(); i++)      hs_vec_append(v, val_to_array(list[i]), False)

       Json.Value &d = diff[i]
      hs_vec *v_diff = &v.diff[i]
      for (j = 0; j < d.size(); j++)
        hs_vec_append(v_diff, val_to_array(d[j]), True)


  return res


def val_to_list(self, &val):  uint32_t elems[val.size()]
  for (i = 0; i < val.size(); i++)
    elems[i] = val[i].asUInt()
  return make_sorted_list_from_array(val.size(),elems)



Condition *val_to_path( Json.Value &pathlets)  PathCondition *path = PathCondition()
  for (i = 0; i < pathlets.size(); i++)     Json.Value &val = pathlets[i]
     char *type = val["type"].asCString()
    PathSpecifier *p = NULL
    if not strcasecmp(type, "port")) p = PortSpecifier(val["port"].asUInt():
    elif not strcasecmp(type, "table")) p = TableSpecifier(val["table"].asUInt():
    elif not strncasecmp(type, "next", 4) or not strncasecmp(type, "last", 4):       Json.Value &arg = not strcasecmp(type + 5, "ports") ? val["ports"] : val["tables"]
      l = val_to_list(arg)
      if not strcasecmp(type, "next_ports")) p = NextPortsSpecifier(l:
      elif not strcasecmp(type, "next_tables")) p = NextTablesSpecifier(l:
      elif not strcasecmp(type, "last_ports")) p = LastPortsSpecifier(l:
      elif not strcasecmp(type, "last_tables")) p = LastTablesSpecifier(l:

    elif not strcasecmp(type, "skip")) p = SkipNextSpecifier(:
    elif not strcasecmp(type, "end")) p = EndPathSpecifier(:
    path.add_pathlet(p)

  return path


Condition *val_to_cond( Json.Value &val, length)  if (val.isNull()) return NULL
   char *type = val["type"].asCString()
  if not strcasecmp(type, "True")) return TrueCondition(:
  if not strcasecmp(type, "False")) return FalseCondition(:
  if not strcasecmp(type, "path")) return val_to_path(val["pathlets"]:
  if not strcasecmp(type, "header")) return HeaderCondition(val_to_hs(val["header"], length):
  if not strcasecmp(type, "not")) return NotCondition(val_to_cond(val["arg"], length):
  if not strcasecmp(type, "and") or not strcasecmp(type, "or"):    Condition *c1 = val_to_cond(val["arg1"], length)
    Condition *c2 = val_to_cond(val["arg2"], length)
    if not strcasecmp(type, "and")) return AndCondition(c1, c2:
    else return OrCondition(c1, c2)

  return NULL



typedef bool (RpcHandler.*RpcFn) ( Json.Value &, &)

void RpcHandler.initServer (TcpServer &server)#define FN(NAME) {#NAME, &RpcHandler.NAME
  struct { string name; RpcFn fn; } methods[] =    FN(init), FN(destroy),
    FN(add_link), FN(remove_link),
    FN(add_table), FN(remove_table),
    FN(add_rule), FN(remove_rule),
    FN(add_source), FN(remove_source),
    FN(add_source_probe), FN(remove_source_probe),
    FN(print_table)

  n = sizeof methods / sizeof *methods
  for (i = 0; i < n; i++)
    server.AddMethod (new RpcMethod<RpcHandler> (*self, methods[i].fn, methods[i].name))
#undef FN


#define PROTO(NAME) \
  bool RpcHandler.NAME ( Json.Value &req, &resp) { \
    cout << "Recv: " << req << endl; \
    resp["id"] = req["id"]; resp["jsonrpc"] = req["jsonrpc"]; \
    clock_t start, end; start = clock()

#define FINI do { \
    cout << "Send: " << resp << endl; \
    return True; \
  } while (0)
#define RETURN(VAL) \
  end = clock(); \
  cout << "Event handling time: " << (double(end - start) * 1000 / CLOCKS_PER_SEC) << "ms." << endl; \
  do { resp["result"] = (VAL); FINI; } while (0)

#define ERROR(MSG) do { \
    resp["error"]["code"] = 1; resp["error"]["message"] = (MSG); FINI; \
  } while (0)

#define PARAM(NAME) req["params"][#NAME]
#define VOID Json.Value.null

PROTO(init)
  length = PARAM(length).asInt()
  if netPlumber) ERROR ("Already initialized.":
  netPlumber = NetPlumber(length)
  RETURN(VOID)


PROTO(destroy)
  delete netPlumber
  netPlumber = NULL
  RETURN(VOID)


PROTO(add_link)
  from = PARAM(from_port).asUInt()
  to = PARAM(to_port).asUInt()
  netPlumber.add_link(from, to)
  RETURN(VOID)


PROTO(remove_link)
  from = PARAM(from_port).asUInt()
  to = PARAM(to_port).asUInt()
  netPlumber.remove_link(from, to)
  RETURN(VOID)


PROTO(add_table)
  id = PARAM(id).asUInt()
  ports = val_to_list(PARAM(in))
  netPlumber.add_table(id,ports)
  RETURN(VOID)


PROTO(remove_table)
  id = PARAM(id).asUInt()
  netPlumber.remove_table(id)
  RETURN(VOID)


PROTO(add_rule)
  table = PARAM(table).asUInt()
  index = PARAM(index).asInt()
  in = val_to_list(PARAM(in))
  out = val_to_list(PARAM(out))
  array_t *match = val_to_array(PARAM(match))
  array_t *mask = val_to_array(PARAM(mask))
  array_t *rw = val_to_array(PARAM(rw))
  ret = netPlumber.add_rule(table, index, in, out, match, mask, rw)
  RETURN((Json.Value.UInt64) ret)


PROTO(remove_rule)
  node = PARAM(node).asUInt64()
clock_t st, en; st = clock()
  netPlumber.remove_rule(node)
en = clock()
cout << "Only deleting takes: " << (double(en - st) * 1000000 / CLOCKS_PER_SEC) << "us." << endl; \


  RETURN(VOID)


PROTO(add_source)
  hs *h = val_to_hs(PARAM(hs), length)
  ports = val_to_list(PARAM(ports))
  ret = netPlumber.add_source(h, ports)
  RETURN((Json.Value.UInt64) ret)


PROTO(remove_source)
  id = PARAM(id).asUInt64()
  netPlumber.remove_source(id)
  RETURN(VOID)


PROTO(add_source_probe)
  ports = val_to_list(PARAM(ports))
  mode = not strcasecmp(PARAM(mode).asCString(), "universal") ? UNIVERSAL : EXISTENTIAL
  Condition *filter = val_to_cond(PARAM(filter), length)
  Condition *test = val_to_cond(PARAM(test), length)
  ret = netPlumber.add_source_probe(ports, mode, filter, test, NULL, NULL)
  RETURN((Json.UInt64) ret)


PROTO(remove_source_probe)
  id = PARAM(id).asUInt64()
  netPlumber.remove_source_probe(id)
  RETURN(VOID)


PROTO(print_table)
  id = PARAM(id).asUInt()
  netPlumber.print_table(id)
  RETURN(VOID)




