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

#include "node.h"
#include <sstream>
extern "C" {
  #include "../headerspace/hs.h"
#include "../headerspace/array.h"
}
#include <set>

using namespace std;

bool is_flow_looped(Flow *flow) {
  Flow *f = flow;
  set<uint64_t> seen_tables;
  while(1) {
    uint64_t table_id = (f->node->node_id & 0xffffffff00000000);
    if (seen_tables.count(table_id) == 0) {
      seen_tables.insert(table_id);
    } else {
      return true;
    }
    if (f->node->get_type() == RULE) {
      f = *f->p_flow;
    } else {
      return false;
    }
  }
}

Node::Node(void *p, int l, uint64_t n) :
    node_type(BASE), node_id(n), length(l), plumber(p),
    match(NULL), inv_match(NULL), is_input_layer(false), is_output_layer(false)
{
  //do nothing
}

void Node::remove_flows() {
  list<Flow*>::iterator f_it;
  for (f_it = source_flow.begin(); f_it != source_flow.end(); f_it++) {
    hs_free((*f_it)->hs_object);
    if ((*f_it)->processed_hs) hs_free((*f_it)->processed_hs);
    this->absorb_src_flow(f_it,true);
    if ((*f_it)->p_flow != this->source_flow.end()) {
      (*(*f_it)->p_flow)->n_flows->remove(f_it);
    }
    free(*f_it);
  }
  source_flow.clear();
}

void Node::remove_pipes() {
  list<struct Pipeline*>::iterator it;
  for (it = this->next_in_pipeline.begin();
       it != this->next_in_pipeline.end(); it++ ) {
    list<struct Pipeline*>::iterator r = (*it)->r_pipeline;
    free((*it)->pipe_array);
    Node* other_n = (*r)->node;
    free(*r);
    other_n->prev_in_pipeline.erase(r);
    free(*it);
  }
  next_in_pipeline.clear();
  for (it = this->prev_in_pipeline.begin();
       it != this->prev_in_pipeline.end(); it++ ) {
    list<struct Pipeline*>::iterator r = (*it)->r_pipeline;
    free((*it)->pipe_array);
    Node* other_n = (*r)->node;
    free(*r);
    other_n->next_in_pipeline.erase(r);
    free(*it);
  }
  prev_in_pipeline.clear();
}

Node::~Node() {
  this->remove_flows();
  this->remove_pipes();
  if (!input_ports.shared) free(input_ports.list);
  if (!output_ports.shared) free(output_ports.list);
  free(this->match);
  free(this->inv_match);
}

NODE_TYPE Node::get_type() {
  return this->node_type;
}

list<struct Pipeline*>::iterator Node::add_fwd_pipeline(Pipeline *p) {
  this->next_in_pipeline.push_front(p);
  return this->next_in_pipeline.begin();
}

list<struct Pipeline*>::iterator Node::add_bck_pipeline(Pipeline *p) {
  this->prev_in_pipeline.push_front(p);
  return this->prev_in_pipeline.begin();
}

string Node::pipeline_to_string() {
  stringstream result;
  char buf[70];
  char *s;
  result << "Pipelined TO:\n";
  list<struct Pipeline*>::iterator it;
  for (it = next_in_pipeline.begin(); it != next_in_pipeline.end(); it++) {
    list<struct Pipeline*>::iterator r = (*it)->r_pipeline;
    sprintf(buf,"0x%llx",(*r)->node->node_id);
    s = array_to_str((*it)->pipe_array,length,false);
    result << "\tNode " << buf << " Pipe HS: " << s << " [" <<
        (*it)->local_port << "-->" << (*r)->local_port << "]\n";
    free(s);
  }
  result << "Pipelined FROM:\n";
  for (it = prev_in_pipeline.begin(); it != prev_in_pipeline.end(); it++) {
    list<struct Pipeline*>::iterator r = (*it)->r_pipeline;
    sprintf(buf,"0x%llx",(*r)->node->node_id);
    s = array_to_str((*it)->pipe_array,length,false);
    result << "\tNode " << buf << " Pipe HS: " << s << " [" << (*r)->local_port
        << "-->" << (*it)->local_port << "]\n";
    free(s);
  }
  return result.str();
}

string Node::src_flow_to_string() {
  stringstream result;
  result << "Source Flow:\n";
  list<struct Flow*> ::iterator it;
  char *s;
  for (it = source_flow.begin(); it != source_flow.end(); it++) {
    s = hs_to_str((*it)->hs_object);
    result << "\tHS: " <<  s << " --> ";
    free(s);
    if ((*it)->processed_hs) {
      s = hs_to_str((*it)->processed_hs);
      result << s;
      free(s);
    } else {
      if (is_flow_looped(*it)) {
        result << "LOOPED";
      } else {
        result << "DEAD";
      }
    }
    if ((*it)->node->get_type() == RULE) {
      result << "; From Port: " << (*it)->in_port;
    }
    result << "\n";
  }
  return result.str();
}

void Node::remove_link_pipes(uint32_t local_port,uint32_t remote_port) {
  list<struct Pipeline*>::iterator it, tmp;
  list<struct Flow*>::iterator f_it;
  for (it = next_in_pipeline.begin(); it != next_in_pipeline.end(); ) {
    list<struct Pipeline*>::iterator r = (*it)->r_pipeline;
    if ((*it)->local_port == local_port && (*r)->local_port == remote_port) {
      (*r)->node->remove_src_flows_from_pipe(*it);
      (*it)->node->remove_sink_flow_from_pipe(*r);
      free((*it)->pipe_array);
      free(*r);
      (*it)->node->prev_in_pipeline.erase(r);
      free(*it);
      tmp = it;
      it++;
      next_in_pipeline.erase(tmp);
    } else {
      it++;
    }
  }
}

void Node::remove_src_flows_from_pipe(Pipeline *fwd_p) {
  list<struct Flow*>::iterator it,tmp;
  for (it = source_flow.begin(); it != source_flow.end(); /*none*/) {
    if ((*it)->pipe == fwd_p) {
      this->absorb_src_flow(it,true);
      (*(*it)->p_flow)->n_flows->remove(it);
      if ((*it)->processed_hs) hs_free((*it)->processed_hs);
      hs_free((*it)->hs_object);
      free(*it);
      tmp = it;
      it++;
      source_flow.erase(tmp);
    } else {
      it++;
    }
  }
}

void Node::remove_sink_flow_from_pipe(Pipeline *bck_p) {

}

int Node::count_fwd_pipeline() {
  return this->next_in_pipeline.size();
}

int Node::count_bck_pipeline() {
  return this->prev_in_pipeline.size();
}

void Node::count_src_flow(int &inc, int &exc) {
  list<Flow*>::iterator it;
  inc = 0;
  exc = 0;
  for (it = source_flow.begin(); it != source_flow.end(); it++) {
    if ((*it)->processed_hs) {
      inc += hs_count((*it)->processed_hs);
      exc += hs_count_diff((*it)->processed_hs);
    }
  }
}

bool Node::should_block_flow(Flow *f, uint32_t out_port) {
  if (is_input_layer) {
    return f->in_port == out_port;
  } else {
    return (*f->p_flow)->node->should_block_flow(*f->p_flow, out_port);
  }

}

void Node::propagate_src_flow_on_pipes(list<struct Flow*>::iterator s_flow) {
  list<Pipeline *>::iterator it;
  hs *h = NULL;
  for (it = next_in_pipeline.begin(); it != next_in_pipeline.end(); it++) {
    if (is_output_layer && should_block_flow(*s_flow,(*it)->local_port))
      continue;
    if (!h) h = (hs *)malloc(sizeof *h);
    if (hs_isect_arr(h, (*s_flow)->processed_hs, (*it)->pipe_array)) {
      // create a new flow struct to pass to next node in pipeline
      Flow *next_flow = (Flow *)malloc(sizeof *next_flow);
      next_flow->node = (*(*it)->r_pipeline)->node;
      next_flow->hs_object = h;
      next_flow->in_port = (*(*it)->r_pipeline)->local_port;
      next_flow->pipe = *it;
      next_flow->p_flow = s_flow;
      next_flow->n_flows = NULL;
      next_flow->processed_hs = NULL;
      // request next node to process this flow
      (*(*it)->r_pipeline)->node->process_src_flow(next_flow);
      h = NULL;
    }
  }
  free(h);
}

void Node::propagate_src_flows_on_pipe(list<Pipeline *>::iterator pipe) {
  list<Flow *>::iterator it;
  hs *h = NULL;
  for (it = source_flow.begin(); it != source_flow.end(); it++) {
    if (is_output_layer && should_block_flow(*it,(*pipe)->local_port))
      continue;
    if ((*it)->processed_hs == NULL) continue;
    if (!h) h = (hs *)malloc(sizeof *h);
    if (hs_isect_arr(h, (*it)->processed_hs, (*pipe)->pipe_array)) {
      Flow *next_flow = (Flow *)malloc(sizeof *next_flow);
      next_flow->node = (*(*pipe)->r_pipeline)->node;
      next_flow->hs_object = h;
      next_flow->in_port = (*(*pipe)->r_pipeline)->local_port;
      next_flow->pipe = *pipe;
      next_flow->p_flow = it;
      next_flow->n_flows = NULL;
      next_flow->processed_hs = NULL;
      (*(*pipe)->r_pipeline)->node->process_src_flow(next_flow);
      h = NULL;
    }
  }
  if (h) free(h);
}

void Node::repropagate_src_flow_on_pipes(list<struct Flow*>::iterator s_flow,
    array_t *change) {

  set<Pipeline*> pipe_hash_set;
  list<std::list<struct Flow*>::iterator>::iterator nit,tmp_nit;
  hs *h = NULL;
  if ((*s_flow)->n_flows) {
    for (nit = (*s_flow)->n_flows->begin();
        nit != (*s_flow)->n_flows->end(); /*do nothing */) {
      Flow *next_flow = **nit;
      if (change) {
        array_t *piped = array_isect_a(  //change through pipe
              change,next_flow->pipe->pipe_array,length);
        if (piped) {
          hs_diff(next_flow->hs_object, piped);
          next_flow->node->process_src_flow_at_location(*nit,piped);
          free(piped);
        }
        next_flow->node->process_src_flow_at_location(*nit,change);
        nit++;
      } else {
        pipe_hash_set.insert(next_flow->pipe);
        if (!h) h = (hs *)malloc(sizeof *h);
        if (hs_isect_arr(
            h, (*s_flow)->processed_hs, next_flow->pipe->pipe_array)
            ){  // update the hs_object of next flow and ask it to reprocess it.
          hs_free(next_flow->hs_object);
          next_flow->hs_object = h;
          next_flow->node->process_src_flow_at_location(*nit,change);
          h = NULL;
          nit++;
        } else { // then this flow no longer propagate on this path. absorb it.
          next_flow->node->absorb_src_flow(*nit,false);
          tmp_nit = nit;
          nit++;
          (*s_flow)->n_flows->erase(tmp_nit);
        }
      }
    }
  }
  if (change) return;

  list<Pipeline *>::iterator it;
  for (it = next_in_pipeline.begin(); it != next_in_pipeline.end(); it++) {
    if (pipe_hash_set.count(*it) > 0) continue;  //skip pipes visited above.
    if (is_output_layer && should_block_flow(*s_flow,(*it)->local_port))
      continue;
    if (!h) h = (hs *)malloc(sizeof *h);
    if (hs_isect_arr(h, (*s_flow)->processed_hs, (*it)->pipe_array)) {
      // create a new flow struct to pass to next node in pipeline
      Flow *next_flow = (Flow *)malloc(sizeof *next_flow);
      next_flow->node = (*(*it)->r_pipeline)->node;
      next_flow->hs_object = h;
      next_flow->in_port = (*(*it)->r_pipeline)->local_port;
      next_flow->pipe = *it;
      next_flow->p_flow = s_flow;
      next_flow->n_flows = NULL;
      // request next node to process this flow
      (*(*it)->r_pipeline)->node->process_src_flow(next_flow);
      h = NULL;
    }
  }
  free(h);
}

void Node::absorb_src_flow(list<struct Flow*>::iterator s_flow, bool first) {
  list<std::list<struct Flow*>::iterator>::iterator it;
  if ((*s_flow)->n_flows) {
    for (it = (*s_flow)->n_flows->begin();
        it != (*s_flow)->n_flows->end(); it++) {
      (**it)->node->absorb_src_flow(*it,false);
    }
    delete (*s_flow)->n_flows;
    (*s_flow)->n_flows = NULL;
  }
  if (!first) {
    hs_free((*s_flow)->hs_object);
    if ((*s_flow)->processed_hs) hs_free((*s_flow)->processed_hs);
    free(*s_flow);
    this->source_flow.erase(s_flow);
  }
}

