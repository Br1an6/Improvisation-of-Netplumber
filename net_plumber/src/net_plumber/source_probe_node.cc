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

#include "source_probe_node.h"
#include "net_plumber_utils.h"
#include <sstream>
#include <string>
#include "net_plumber.h"
#include <assert.h>

using namespace std;
using namespace log4cxx;
using namespace net_plumber;

LoggerPtr probe_def_logger(Logger::getLogger("DefaultProbeLogger"));

string probe_transition(PROBE_TRANSITION t) {
  switch (t) {
  case UNKNOWN: return "Unknown";
  case STARTED_FALSE: return "Started in False State";
  case STARTED_TRUE: return "Started in True State";
  case TRUE_TO_FALSE: return "Failed Probe Condition";
  case FALSE_TO_TRUE: return "Met Probe Condition";
  case MORE_FALSE: return "More Flows Failed Probe Condition";
  case LESS_FALSE: return "Fewer Flows Failed Probe Condition";
  case MORE_TRUE: return "More Flows Met Probe Condition";
  case LESS_TRUE: return "Fewer Flows Met Probe Condition";
  default: return "Undefined";
  }
}

void default_probe_callback(void *caller, SourceProbeNode *p, Flow *f,void *data,
                            PROBE_TRANSITION t) {
  NetPlumber *N = (NetPlumber *)caller;
  Event e = N->get_last_event();
  stringstream error_msg;
  if (p->get_mode() == EXISTENTIAL) error_msg << "Existential ";
  else error_msg << "Universal ";
  error_msg << "Probe " << p->node_id << " Activated after event " <<
      get_event_name(e.type) << ": " << probe_transition(t);
  LOG4CXX_WARN(probe_def_logger,error_msg.str());
}

SourceProbeNode::SourceProbeNode(void *n, int length, uint64_t node_id,
                                 PROBE_MODE mode, List_t ports,
                                 Condition *filter, Condition *test,
                                 src_probe_callback_t probe_callback, void* d)
: Node(n,length,node_id), state(STOPPED), mode(mode),
  filter(filter), test(test), cond_count(0), probe_callback_data(d)
{
  this->node_type = SOURCE_PROBE;
  this->match = array_create(length, BIT_X);
  this->inv_match = NULL;
  this->input_ports = ports;
  this->output_ports = make_sorted_list(0);
  if (probe_callback) this->probe_callback = probe_callback;
  else this->probe_callback = default_probe_callback;
}

SourceProbeNode::~SourceProbeNode() {
  delete test;
  delete filter;
}

void SourceProbeNode::process_src_flow(Flow *f) {
  if (f) {
    list<struct Flow*>::iterator f_it;
    source_flow.push_front(f);
    f_it = source_flow.begin();
    (*f->p_flow)->n_flows->push_front(f_it);
    f->processed_hs = hs_copy_a(f->hs_object);
    hs_comp_diff(f->processed_hs);
    if (state == RUNNING) update_check(f,0);
  } else {
    list<struct Pipeline*>::iterator it;
    for (it = prev_in_pipeline.begin(); it != prev_in_pipeline.end(); it++) {
      (*(*it)->r_pipeline)->node->
          propagate_src_flows_on_pipe((*it)->r_pipeline);
    }
  }
}

void SourceProbeNode::process_src_flow_at_location(
     list<struct Flow*>::iterator loc, array_t* change) {
  Flow *f = *loc;
  if (change) {
    if (f->processed_hs->list.used == 0) return;
    hs_diff(f->processed_hs, change);
  } else {
    hs_free(f->processed_hs);
    f->processed_hs = hs_copy_a(f->hs_object);
    hs_comp_diff(f->processed_hs);
  }
  if (state == RUNNING) update_check(f,1);
}

void SourceProbeNode::absorb_src_flow(list<struct Flow*>::iterator s_flow,
    bool first) {
  if (state == RUNNING) update_check(*s_flow,2);
  Node::absorb_src_flow(s_flow, first);
}

void SourceProbeNode::update_check(Flow *f, short action) {
  /*
   * 0: add
   * 1: modified
   * 2: deleted
   */
  assert(cond_count >= 0);
  // if flow is empty, do nothing
  if (f->processed_hs->list.used == 0) return;

  // Delete flow
  if (action == 2) {
    if (check_results.count(f) > 0) {
      if (mode == EXISTENTIAL && check_results[f]) {
        cond_count--;
        if (cond_count == 0) {
          probe_callback(this->plumber,this,f,probe_callback_data,TRUE_TO_FALSE);
        } else {
          probe_callback(this->plumber,this,f,probe_callback_data,LESS_TRUE);
        }
      } else if (mode == UNIVERSAL && !check_results[f]) {
        cond_count--;
        if (cond_count == 0) {
          probe_callback(this->plumber,this,f,probe_callback_data,FALSE_TO_TRUE);
        } else {
          probe_callback(this->plumber,this,f,probe_callback_data,LESS_FALSE);
        }
      }
      check_results.erase(f);
    }
    return;
  }

  bool m = filter->check(f);

  // Newly added flow
  if ((action == 0 && m) | (action == 1 && m && check_results.count(f) == 0)) {
    bool c = test->check(f);
    check_results[f] = c;
    if (mode == EXISTENTIAL && c) {
      cond_count++;
      if (cond_count == 1) {
        probe_callback(this->plumber,this,f,probe_callback_data,FALSE_TO_TRUE);
      } else {
        probe_callback(this->plumber,this,f,probe_callback_data,MORE_TRUE);
      }
    } else if (mode == UNIVERSAL && !c) {
      cond_count++;
      if (cond_count == 1) {
        probe_callback(this->plumber,this,f,probe_callback_data,TRUE_TO_FALSE);
      } else {
        probe_callback(this->plumber,this,f,probe_callback_data,MORE_FALSE);
      }
    }
  }

  // Updated flow
  else if (action == 1 && m) {
    bool c = test->check(f);
    if (check_results[f] == c) return;
    check_results[f] = c;
    if (mode == EXISTENTIAL && c) {
      cond_count++;
      if (cond_count == 1) {
        probe_callback(this->plumber,this,f,probe_callback_data,FALSE_TO_TRUE);
      } else {
        probe_callback(this->plumber,this,f,probe_callback_data,MORE_TRUE);
      }
    } else if (mode == EXISTENTIAL && !c) {
      cond_count--;
      if (cond_count == 0) {
        probe_callback(this->plumber,this,f,probe_callback_data,TRUE_TO_FALSE);
      } else {
        probe_callback(this->plumber,this,f,probe_callback_data,LESS_TRUE);
      }
    } else if (mode == UNIVERSAL && !c) {
      cond_count++;
      if (cond_count == 1) {
        probe_callback(this->plumber,this,f,probe_callback_data,TRUE_TO_FALSE);
      } else {
        probe_callback(this->plumber,this,f,probe_callback_data,MORE_FALSE);
      }
    } else if (mode == UNIVERSAL && c) {
      cond_count--;
      if (cond_count == 0) {
        probe_callback(this->plumber,this,f,probe_callback_data,FALSE_TO_TRUE);
      } else {
        probe_callback(this->plumber,this,f,probe_callback_data,LESS_FALSE);
      }
    }
  }
}

void SourceProbeNode::start_probe() {
  NetPlumber* n = (NetPlumber*)this->plumber;
  Event e = {START_SOURCE_PROBE,node_id,0};
  n->set_last_event(e);
  this->state = STARTED;
  list<Flow*>::iterator it;
  for (it = source_flow.begin(); it != source_flow.end(); it++) {
    if (!filter->check(*it)) continue;
    bool c = test->check(*it);
    check_results[*it] = c;
    if (mode == EXISTENTIAL && c) {
      cond_count++;
      probe_callback(this->plumber,this,*it,probe_callback_data,STARTED_TRUE);
    } else if (mode == UNIVERSAL && !c) {
      cond_count++;
      probe_callback(this->plumber,this,*it,probe_callback_data,STARTED_FALSE);
    }
  }
  if (mode == EXISTENTIAL && cond_count == 0)
    probe_callback(this->plumber,this,NULL,probe_callback_data,STARTED_FALSE);
  else if (mode == UNIVERSAL && cond_count == 0)
    probe_callback(this->plumber,this,NULL,probe_callback_data,STARTED_TRUE);
  this->state = RUNNING;
}

void SourceProbeNode::stop_probe() {
  NetPlumber* n = (NetPlumber*)this->plumber;
  Event e = {STOP_SOURCE_PROBE,node_id,0};
  n->set_last_event(e);
  this->state = STOPPED;
  check_results.clear();
  cond_count = 0;
}

list<Flow*>::iterator SourceProbeNode::get_source_flow_iterator() {
  return source_flow.begin();
}

string SourceProbeNode::to_string() {
  stringstream result;
  char buf[70];
  result << string(40, '=') << "\n";
  sprintf(buf,"0x%llx",node_id);
  if (mode == EXISTENTIAL) result << "  Existential ";
  else result << "  Universal ";
  result << "Probe: " << buf << "\n";
  result << string(40, '=') << "\n";
  result << "Filter: " << filter->to_string() << "\n";
  result << "Condition: " << test->to_string() << "\n";
  result << pipeline_to_string();
  result << src_flow_to_string();
  return result.str();
}


