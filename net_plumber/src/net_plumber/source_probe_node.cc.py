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

#include "source_probe_node.h"
#include "net_plumber_utils.h"
#include <sstream>
#include <string>
#include "net_plumber.h"
#include <assert.h>

using namespace std
using namespace log4cxx
using namespace net_plumber

LoggerPtr probe_def_logger(Logger.getLogger("DefaultProbeLogger"))

def probe_transition(self, t):  switch (t)  case UNKNOWN: return "Unknown"
  case STARTED_FALSE: return "Started in False State"
  case STARTED_TRUE: return "Started in True State"
  case TRUE_TO_FALSE: return "Failed Probe Condition"
  case FALSE_TO_TRUE: return "Met Probe Condition"
  case MORE_FALSE: return "More Flows Failed Probe Condition"
  case LESS_FALSE: return "Fewer Flows Failed Probe Condition"
  case MORE_TRUE: return "More Flows Met Probe Condition"
  case LESS_TRUE: return "Fewer Flows Met Probe Condition"
  default: return "Undefined"



void default_probe_callback(void *caller, *p, *f, *data,
                            PROBE_TRANSITION t)  NetPlumber *N = (NetPlumber *)caller
  e = N.get_last_event()
  stringstream error_msg
  if (p.get_mode() == EXISTENTIAL) error_msg << "Existential "
  else error_msg << "Universal "
  error_msg << "Probe " << p.node_id << " Activated after event " <<
      get_event_name(e.type) << ": " << probe_transition(t)
  LOG4CXX_WARN(probe_def_logger,error_msg.str())


SourceProbeNode.SourceProbeNode(void *n, length, node_id,
                                 PROBE_MODE mode, ports,
                                 Condition *filter, *test,
                                 src_probe_callback_t probe_callback, d)
: Node(n,length,node_id), state(STOPPED), mode(mode),
  filter(filter), test(test), cond_count(0), probe_callback_data(d)
  self.node_type = SOURCE_PROBE
  self.match = array_create(length, BIT_X)
  self.inv_match = NULL
  self.input_ports = ports
  self.output_ports = make_sorted_list(0)
  if (probe_callback) self.probe_callback = probe_callback
  else self.probe_callback = default_probe_callback


SourceProbeNode.~SourceProbeNode()  delete test
  delete filter


def process_src_flow(self, *f):  if f:    list<struct Flow*>.iterator f_it
    source_flow.push_front(f)
    f_it = source_flow.begin()
    (*f.p_flow).n_flows.push_front(f_it)
    f.processed_hs = hs_copy_a(f.hs_object)
    hs_comp_diff(f.processed_hs)
    if state == RUNNING) update_check(f,0:
  } else:
    list<struct Pipeline*>.iterator it
    for (it = prev_in_pipeline.begin(); it != prev_in_pipeline.end(); it++)      (*(*it).r_pipeline).node.
          propagate_src_flows_on_pipe((*it).r_pipeline)




void SourceProbeNode.process_src_flow_at_location(
     list<struct Flow*>.iterator loc, change)  Flow *f = *loc
  if change:    if (f.processed_hs.list.used == 0) return
    hs_diff(f.processed_hs, change)
  } else:
    hs_free(f.processed_hs)
    f.processed_hs = hs_copy_a(f.hs_object)
    hs_comp_diff(f.processed_hs)

  if state == RUNNING) update_check(f,1:


void SourceProbeNode.absorb_src_flow(list<struct Flow*>.iterator s_flow,
    bool first)  if state == RUNNING) update_check(*s_flow,2:
  Node.absorb_src_flow(s_flow, first)


def update_check(self, *f, action):  '''
   * 0: add
   * 1: modified
   * 2: deleted
   '''
  assert(cond_count >= 0)
  # if flow is empty, nothing
  if (f.processed_hs.list.used == 0) return

  # Delete flow
  if action == 2:    if check_results.count(f) > 0:      if mode == EXISTENTIAL and check_results[f]:        cond_count--
        if cond_count == 0:          probe_callback(self.plumber,self,f,probe_callback_data,TRUE_TO_FALSE)
        } else:
          probe_callback(self.plumber,self,f,probe_callback_data,LESS_TRUE)

      } elif mode == UNIVERSAL and not check_results[f]:        cond_count--
        if cond_count == 0:          probe_callback(self.plumber,self,f,probe_callback_data,FALSE_TO_TRUE)
        } else:
          probe_callback(self.plumber,self,f,probe_callback_data,LESS_FALSE)


      check_results.erase(f)

    return


  m = filter.check(f)

  # Newly added flow
  if (action == 0 and m) | (action == 1 and m and check_results.count(f) == 0):    c = test.check(f)
    check_results[f] = c
    if mode == EXISTENTIAL and c:      cond_count++
      if cond_count == 1:        probe_callback(self.plumber,self,f,probe_callback_data,FALSE_TO_TRUE)
      } else:
        probe_callback(self.plumber,self,f,probe_callback_data,MORE_TRUE)

    } elif mode == UNIVERSAL and not c:      cond_count++
      if cond_count == 1:        probe_callback(self.plumber,self,f,probe_callback_data,TRUE_TO_FALSE)
      } else:
        probe_callback(self.plumber,self,f,probe_callback_data,MORE_FALSE)




  # Updated flow
  elif action == 1 and m:    c = test.check(f)
    if (check_results[f] == c) return
    check_results[f] = c
    if mode == EXISTENTIAL and c:      cond_count++
      if cond_count == 1:        probe_callback(self.plumber,self,f,probe_callback_data,FALSE_TO_TRUE)
      } else:
        probe_callback(self.plumber,self,f,probe_callback_data,MORE_TRUE)

    } elif mode == EXISTENTIAL and not c:      cond_count--
      if cond_count == 0:        probe_callback(self.plumber,self,f,probe_callback_data,TRUE_TO_FALSE)
      } else:
        probe_callback(self.plumber,self,f,probe_callback_data,LESS_TRUE)

    } elif mode == UNIVERSAL and not c:      cond_count++
      if cond_count == 1:        probe_callback(self.plumber,self,f,probe_callback_data,TRUE_TO_FALSE)
      } else:
        probe_callback(self.plumber,self,f,probe_callback_data,MORE_FALSE)

    } elif mode == UNIVERSAL and c:      cond_count--
      if cond_count == 0:        probe_callback(self.plumber,self,f,probe_callback_data,FALSE_TO_TRUE)
      } else:
        probe_callback(self.plumber,self,f,probe_callback_data,LESS_FALSE)





def start_probe(self):  n = (NetPlumber*)self.plumber
  e = {START_SOURCE_PROBE,node_id,0
  n.set_last_event(e)
  self.state = STARTED
  list<Flow*>.iterator it
  for (it = source_flow.begin(); it != source_flow.end(); it++)    if (not filter.check(*it)) continue
    c = test.check(*it)
    check_results[*it] = c
    if mode == EXISTENTIAL and c:      cond_count++
      probe_callback(self.plumber,self,*it,probe_callback_data,STARTED_TRUE)
    } elif mode == UNIVERSAL and not c:      cond_count++
      probe_callback(self.plumber,self,*it,probe_callback_data,STARTED_FALSE)


  if mode == EXISTENTIAL and cond_count == 0:
    probe_callback(self.plumber,self,NULL,probe_callback_data,STARTED_FALSE)
  elif mode == UNIVERSAL and cond_count == 0:
    probe_callback(self.plumber,self,NULL,probe_callback_data,STARTED_TRUE)
  self.state = RUNNING


def stop_probe(self):  n = (NetPlumber*)self.plumber
  e = {STOP_SOURCE_PROBE,node_id,0
  n.set_last_event(e)
  self.state = STOPPED
  check_results.clear()
  cond_count = 0


def get_source_flow_iterator(self):  return source_flow.begin()


def to_string(self):  stringstream result
  char buf[70]
  result << string(40, '=') << "\n"
  sprintf(buf,"0x%llx",node_id)
  if (mode == EXISTENTIAL) result << "  Existential "
  else result << "  Universal "
  result << "Probe: " << buf << "\n"
  result << string(40, '=') << "\n"
  result << "Filter: " << filter.to_string() << "\n"
  result << "Condition: " << test.to_string() << "\n"
  result << pipeline_to_string()
  result << src_flow_to_string()
  return result.str()



