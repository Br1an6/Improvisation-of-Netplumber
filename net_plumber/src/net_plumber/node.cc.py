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

#include "node.h"
#include <sstream>
extern "C"  #include "../headerspace/hs.h"
#include "../headerspace/array.h"

#include <set>

using namespace std

def is_flow_looped(self, *flow):  Flow *f = flow
  set<uint64_t> seen_tables
  while(1)    table_id = (f.node.node_id & 0xffffffff00000000)
    if seen_tables.count(table_id) == 0:      seen_tables.insert(table_id)
    } else:
      return True

    if f.node.get_type() == RULE:      f = *f.p_flow
    } else:
      return False




Node.Node(void *p, l, n) :
    node_type(BASE), node_id(n), length(l), plumber(p),
    match(NULL), inv_match(NULL), is_input_layer(False), is_output_layer(False)
  #do nothing


def remove_flows(self):  list<Flow*>.iterator f_it
  for (f_it = source_flow.begin(); f_it != source_flow.end(); f_it++)    hs_free((*f_it).hs_object)
    if (*f_it).processed_hs) hs_free((*f_it).processed_hs:
    self.absorb_src_flow(f_it,True)
    if (*f_it).p_flow != self.source_flow.end():      (*(*f_it).p_flow).n_flows.remove(f_it)

    free(*f_it)

  source_flow.clear()


def remove_pipes(self):  list<struct Pipeline*>.iterator it
  for (it = self.next_in_pipeline.begin()
       it != self.next_in_pipeline.end(); it++ )    list<struct Pipeline*>r = (*it).r_pipeline
    free((*it).pipe_array)
    other_n = (*r).node
    free(*r)
    other_n.prev_in_pipeline.erase(r)
    free(*it)

  next_in_pipeline.clear()
  for (it = self.prev_in_pipeline.begin()
       it != self.prev_in_pipeline.end(); it++ )    list<struct Pipeline*>r = (*it).r_pipeline
    free((*it).pipe_array)
    other_n = (*r).node
    free(*r)
    other_n.next_in_pipeline.erase(r)
    free(*it)

  prev_in_pipeline.clear()


Node.~Node()  self.remove_flows()
  self.remove_pipes()
  if not input_ports.shared) free(input_ports.list:
  if not output_ports.shared) free(output_ports.list:
  free(self.match)
  free(self.inv_match)


def get_type(self):  return self.node_type


list<struct Pipeline*>.iterator Node.add_fwd_pipeline(Pipeline *p)  self.next_in_pipeline.push_front(p)
  return self.next_in_pipeline.begin()


list<struct Pipeline*>.iterator Node.add_bck_pipeline(Pipeline *p)  self.prev_in_pipeline.push_front(p)
  return self.prev_in_pipeline.begin()


def pipeline_to_string(self):  stringstream result
  char buf[70]
  char *s
  result << "Pipelined TO:\n"
  list<struct Pipeline*>.iterator it
  for (it = next_in_pipeline.begin(); it != next_in_pipeline.end(); it++)    list<struct Pipeline*>r = (*it).r_pipeline
    sprintf(buf,"0x%llx",(*r).node.node_id)
    s = array_to_str((*it).pipe_array,length,False)
    result << "\tNode " << buf << " Pipe HS: " << s << " [" <<
        (*it).local_port << "-." << (*r).local_port << "]\n"
    free(s)

  result << "Pipelined FROM:\n"
  for (it = prev_in_pipeline.begin(); it != prev_in_pipeline.end(); it++)    list<struct Pipeline*>r = (*it).r_pipeline
    sprintf(buf,"0x%llx",(*r).node.node_id)
    s = array_to_str((*it).pipe_array,length,False)
    result << "\tNode " << buf << " Pipe HS: " << s << " [" << (*r).local_port
        << "-." << (*it).local_port << "]\n"
    free(s)

  return result.str()


def src_flow_to_string(self):  stringstream result
  result << "Source Flow:\n"
  list<struct Flow*> .iterator it
  char *s
  for (it = source_flow.begin(); it != source_flow.end(); it++)    s = hs_to_str((*it).hs_object)
    result << "\tHS: " <<  s << " -. "
    free(s)
    if (*it).processed_hs:      s = hs_to_str((*it).processed_hs)
      result << s
      free(s)
    } else:
      if is_flow_looped(*it):        result << "LOOPED"
      } else:
        result << "DEAD"


    if (*it).node.get_type() == RULE:      result << "; From Port: " << (*it).in_port

    result << "\n"

  return result.str()


def remove_link_pipes(self, local_port, remote_port):  list<struct Pipeline*>.iterator it, tmp
  list<struct Flow*>.iterator f_it
  for (it = next_in_pipeline.begin(); it != next_in_pipeline.end(); )    list<struct Pipeline*>r = (*it).r_pipeline
    if (*it).local_port == local_port and (*r).local_port == remote_port:      (*r).node.remove_src_flows_from_pipe(*it)
      (*it).node.remove_sink_flow_from_pipe(*r)
      free((*it).pipe_array)
      free(*r)
      (*it).node.prev_in_pipeline.erase(r)
      free(*it)
      tmp = it
      it++
      next_in_pipeline.erase(tmp)
    } else:
      it++




def remove_src_flows_from_pipe(self, *fwd_p):  list<struct Flow*>.iterator it,tmp
  for (it = source_flow.begin(); it != source_flow.end(); '''none''')    if (*it).pipe == fwd_p:      self.absorb_src_flow(it,True)
      (*(*it).p_flow).n_flows.remove(it)
      if (*it).processed_hs) hs_free((*it).processed_hs:
      hs_free((*it).hs_object)
      free(*it)
      tmp = it
      it++
      source_flow.erase(tmp)
    } else:
      it++




def remove_sink_flow_from_pipe(self, *bck_p):


def count_fwd_pipeline(self):  return self.next_in_pipeline.size()


def count_bck_pipeline(self):  return self.prev_in_pipeline.size()


def count_src_flow(self, &inc, &exc):  list<Flow*>.iterator it
  inc = 0
  exc = 0
  for (it = source_flow.begin(); it != source_flow.end(); it++)    if (*it).processed_hs:      inc += hs_count((*it).processed_hs)
      exc += hs_count_diff((*it).processed_hs)




def should_block_flow(self, *f, out_port):  if is_input_layer:    return f.in_port == out_port
  } else:
    return (*f.p_flow).node.should_block_flow(*f.p_flow, out_port)




def propagate_src_flow_on_pipes(self, Flow*>.iterator s_flow):  list<Pipeline *>.iterator it
  hs *h = NULL
  for (it = next_in_pipeline.begin(); it != next_in_pipeline.end(); it++)    if is_output_layer and should_block_flow(*s_flow,(*it).local_port):
      continue
    if not h) h = (hs *)malloc(sizeof *h:
    if hs_isect_arr(h, (*s_flow).processed_hs, (*it).pipe_array):      # create a flow struct to pass to next node in pipeline
      Flow *next_flow = (Flow *)malloc(sizeof *next_flow)
      next_flow.node = (*(*it).r_pipeline).node
      next_flow.hs_object = h
      next_flow.in_port = (*(*it).r_pipeline).local_port
      next_flow.pipe = *it
      next_flow.p_flow = s_flow
      next_flow.n_flows = NULL
      next_flow.processed_hs = NULL
      # request next node to process self flow
      (*(*it).r_pipeline).node.process_src_flow(next_flow)
      h = NULL


  free(h)


def propagate_src_flows_on_pipe(self, *>.iterator pipe):  list<Flow *>.iterator it
  hs *h = NULL
  for (it = source_flow.begin(); it != source_flow.end(); it++)    if is_output_layer and should_block_flow(*it,(*pipe).local_port):
      continue
    if ((*it).processed_hs == NULL) continue
    if not h) h = (hs *)malloc(sizeof *h:
    if hs_isect_arr(h, (*it).processed_hs, (*pipe).pipe_array):      Flow *next_flow = (Flow *)malloc(sizeof *next_flow)
      next_flow.node = (*(*pipe).r_pipeline).node
      next_flow.hs_object = h
      next_flow.in_port = (*(*pipe).r_pipeline).local_port
      next_flow.pipe = *pipe
      next_flow.p_flow = it
      next_flow.n_flows = NULL
      next_flow.processed_hs = NULL
      (*(*pipe).r_pipeline).node.process_src_flow(next_flow)
      h = NULL


  if h) free(h:


void Node.repropagate_src_flow_on_pipes(list<struct Flow*>.iterator s_flow,
    array_t *change)
  set<Pipeline*> pipe_hash_set
  list<std.list<struct Flow*>.iterator>.iterator nit,tmp_nit
  hs *h = NULL
  if (*s_flow).n_flows:    for (nit = (*s_flow).n_flows.begin()
        nit != (*s_flow).n_flows.end(); '''do nothing ''')      Flow *next_flow = **nit
      if change:        array_t *piped = array_isect_a(  #change through pipe
              change,next_flow.pipe.pipe_array,length)
        if piped:          hs_diff(next_flow.hs_object, piped)
          next_flow.node.process_src_flow_at_location(*nit,piped)
          free(piped)

        next_flow.node.process_src_flow_at_location(*nit,change)
        nit++
      } else:
        pipe_hash_set.insert(next_flow.pipe)
        if not h) h = (hs *)malloc(sizeof *h:
        if (hs_isect_arr(
            h, (*s_flow).processed_hs, next_flow.pipe.pipe_array)
            ){  # update the hs_object of next flow and ask it to reprocess it.
          hs_free(next_flow.hs_object)
          next_flow.hs_object = h
          next_flow.node.process_src_flow_at_location(*nit,change)
          h = NULL
          nit++
        } else { # then self flow no longer propagate on self path. absorb it.
          next_flow.node.absorb_src_flow(*nit,False)
          tmp_nit = nit
          nit++
          (*s_flow).n_flows.erase(tmp_nit)




  if (change) return

  list<Pipeline *>.iterator it
  for (it = next_in_pipeline.begin(); it != next_in_pipeline.end(); it++)    if (pipe_hash_set.count(*it) > 0) continue;  #skip pipes visited above.
    if is_output_layer and should_block_flow(*s_flow,(*it).local_port):
      continue
    if not h) h = (hs *)malloc(sizeof *h:
    if hs_isect_arr(h, (*s_flow).processed_hs, (*it).pipe_array):      # create a flow struct to pass to next node in pipeline
      Flow *next_flow = (Flow *)malloc(sizeof *next_flow)
      next_flow.node = (*(*it).r_pipeline).node
      next_flow.hs_object = h
      next_flow.in_port = (*(*it).r_pipeline).local_port
      next_flow.pipe = *it
      next_flow.p_flow = s_flow
      next_flow.n_flows = NULL
      # request next node to process self flow
      (*(*it).r_pipeline).node.process_src_flow(next_flow)
      h = NULL


  free(h)


def absorb_src_flow(self, Flow*>.iterator s_flow, first):  list<std.list<struct Flow*>.iterator>.iterator it
  if (*s_flow).n_flows:    for (it = (*s_flow).n_flows.begin()
        it != (*s_flow).n_flows.end(); it++)      (**it).node.absorb_src_flow(*it,False)

    delete (*s_flow).n_flows
    (*s_flow).n_flows = NULL

  if not first:    hs_free((*s_flow).hs_object)
    if (*s_flow).processed_hs) hs_free((*s_flow).processed_hs:
    free(*s_flow)
    self.source_flow.erase(s_flow)



