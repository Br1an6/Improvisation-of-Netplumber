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

#include "source_node.h"
#include "net_plumber_utils.h"
#include <sstream>
#include <string>

using namespace std;
using namespace log4cxx;

LoggerPtr SourceNode::source_logger(Logger::getLogger("SourceNode"));

SourceNode::SourceNode(void *n, int length, uint64_t node_id, hs *hs_object,
                       List_t ports)
  : Node(n,length,node_id) {
  this->node_type = SOURCE;
  this->match = NULL;
  this->inv_match = array_create(length, BIT_X);
  this->output_ports = ports;
  this->input_ports = make_sorted_list(0);
  // create the flow;
  Flow *f = (Flow *)malloc(sizeof *f);
  f->node = this;
  f->hs_object = hs_object;
  f->processed_hs = hs_copy_a(hs_object);
  f->in_port = 0;
  f->p_flow = this->source_flow.end();
  f->n_flows = new list< list<struct Flow*>::iterator >();
  this->source_flow.push_back(f);
}

SourceNode::~SourceNode() {
  // do nothing
}

string SourceNode::source_to_str() {
  stringstream result;
  char *s = hs_to_str((*source_flow.begin())->hs_object);
  result << "Source: " << s;
  free(s);
  result << " Ports: " << list_to_string(output_ports);
  return result.str();
}

string SourceNode::to_string() {
  stringstream result;
  char buf[70];
  result << string(40, '=') << "\n";
  sprintf(buf,"0x%llx",node_id);
  result << " Source: " << buf << "\n";
  result << string(40, '=') << "\n";
  result << source_to_str() << "\n";
  result << pipeline_to_string();
  result << src_flow_to_string();
  return result.str();
}

void SourceNode::process_src_flow_at_location(
    list<struct Flow*>::iterator loc, array_t* change) {
  // do nothing
  stringstream error_msg;
  error_msg << "Called process_src_flow_at_location on SourceNode " <<
      this->node_id << ". Unexpected behavior.";
  LOG4CXX_FATAL(source_logger,error_msg.str());

}

void SourceNode::process_src_flow(Flow *f) {
  propagate_src_flow_on_pipes(source_flow.begin());
}

