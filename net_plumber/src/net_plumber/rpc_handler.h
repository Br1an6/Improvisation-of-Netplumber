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

#ifndef _RPC_HANDLER_H_
#define _RPC_HANDLER_H_

#include "net_plumber.h"
#include "../jsoncpp/jsonrpc.h"

namespace net_plumber {

array_t *val_to_array(const Json::Value &val);
hs *val_to_hs(const Json::Value &val, int len);
List_t val_to_list(const Json::Value &val);
Condition *val_to_path(const Json::Value &pathlets);
Condition *val_to_cond(const Json::Value &val, int length);

class RpcHandler {
  NetPlumber *netPlumber;
  int length;
public:
  RpcHandler(NetPlumber *N): netPlumber(N), length(N->get_length()) { }
  void initServer(Json::Rpc::TcpServer &server);

private:
#define FN(NAME) bool NAME (const Json::Value &, Json::Value &)
  FN(init); FN(destroy);
  FN(add_link); FN(remove_link);
  FN(add_table); FN(remove_table);
  FN(add_rule); FN(remove_rule);
  FN(add_source); FN(remove_source);
  FN(add_source_probe); FN(remove_source_probe);
  FN(print_table);
#undef FN
};

}

#endif

