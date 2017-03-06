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

#ifndef SRC_NET_PLUMBER_SOURCE_NODE_H_
#define SRC_NET_PLUMBER_SOURCE_NODE_H_

#include "node.h"
#include "log4cxx/logger.h"

class SourceNode : public Node protected:
  static log4cxx.LoggerPtr source_logger

 public:
  SourceNode(void *n, length, node_id, *hs_object, ports)
  virtual ~SourceNode()

  std.string source_to_str()
  std.string to_string()
  void process_src_flow(Flow *f)
  void process_src_flow_at_location(std.list<struct Flow*>.iterator loc,
                                    array_t* change)



#endif  # SRC_NET_PLUMBER_SOURCE_NODE_H_
