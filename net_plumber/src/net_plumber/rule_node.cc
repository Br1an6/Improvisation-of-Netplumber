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

#include <stdio.h>
#include "rule_node.h"
#include "net_plumber_utils.h"
#include <sstream>
#include <string>
#include "net_plumber.h"

using namespace std;
using namespace net_plumber;

void RuleNode::set_layer_flags() {
  if (plumber) {
    NetPlumber* n = (NetPlumber*)plumber;
    List_t table_ports = n->get_table_ports(table);
    this->is_input_layer = lists_has_intersection(table_ports,input_ports);
    this->is_output_layer = lists_has_intersection(table_ports,output_ports);
  } else {
    this->is_input_layer = false;
    this->is_output_layer = false;
  }
}

RuleNode::RuleNode(void *n, int length, uint64_t node_id, uint32_t table,
                   List_t in_ports, List_t out_ports,
                   array_t* match, array_t *mask, array_t* rewrite) :
                   Node(n,length,node_id), table(table), group(0) {
  this->node_type = RULE;
  this->match = match;
  this->mask = mask;
  this->rewrite = rewrite;
  this->input_ports = in_ports;
  this->output_ports = out_ports;
  if (this->mask && this->rewrite) {
    this->inv_match = array_copy(this->match, length);
    array_rewrite( this->inv_match, this->mask, this->rewrite, length);
    this->inv_rw = array_not_a(this->mask,length);
    array_and(this->inv_rw,this->match,length,this->inv_rw);
  } else {
    this->inv_rw = NULL;
    this->inv_match = array_copy(this->match, length);
  }
  effect_on = new list<struct Effect*>();
  influenced_by = new list<struct Influence*>();
  set_layer_flags();
}

RuleNode::RuleNode(void *n, int length, uint64_t node_id, uint32_t table,
                   uint64_t group, List_t in_ports, List_t out_ports,
                   array_t* match, array_t *mask, array_t* rewrite) :
                   Node(n,length,node_id), table(table), group(group) {
  this->node_type = RULE;
  this->match = match;
  this->mask = mask;
  this->rewrite = rewrite;
  this->input_ports = in_ports;
  this->output_ports = out_ports;
  if (this->mask && this->rewrite) {
    this->inv_match = array_copy(this->match, length);
    array_rewrite( this->inv_match, this->mask, this->rewrite, length);
    this->inv_rw = array_not_a(this->mask,length);
    array_and(this->inv_rw,this->match,length,this->inv_rw);
  } else {
    this->inv_rw = NULL;
    this->inv_match = array_copy(this->match, length);
  }
  if (group == node_id) {
    effect_on = new list<struct Effect*>();
    influenced_by = new list<struct Influence*>();
  }
  set_layer_flags();
}

RuleNode::~RuleNode() {
  this->remove_flows();
  this->remove_pipes();
  // remove itself from all rules influencing on it and free its
  // influenced_by struct. In case of group rules, only o this for the lead.
  if (group == 0 || group == node_id) {
    list<struct Influence*>::iterator inf_it;
    for (inf_it = influenced_by->begin(); inf_it != influenced_by->end(); inf_it++){
      list<struct Effect*>::iterator effect = (*inf_it)->effect;
      Effect *f = *effect;
      (*effect)->node->effect_on->erase(effect);
      free((*inf_it)->comm_arr);
      if (!(*inf_it)->ports.shared) free((*inf_it)->ports.list);
      free(*inf_it);
      free(f);
    }
    // remove itself from all rules influenced by this rule and their flows
    list<Effect *>::iterator eff_it;
    list<Flow*>::iterator src_it;
    for (eff_it = effect_on->begin(); eff_it != effect_on->end(); eff_it++) {
      list<struct Influence*>::iterator influence = (*eff_it)->influence;
      RuleNode *n = (*influence)->node;
      array_t *comm_arr = (*influence)->comm_arr;
      List_t ports = (*influence)->ports;
      free(*influence);
      n->influenced_by->erase(influence);
      for (src_it = n->source_flow.begin(); src_it != n->source_flow.end();
          src_it++) {
        if (elem_in_sorted_list((*src_it)->in_port, ports)) {
          n->process_src_flow_at_location(src_it,NULL);
        }
      }
      free(comm_arr);
      if (!ports.shared) free(ports.list);
      free(*eff_it);
    }
    delete effect_on;
    delete influenced_by;
  }
  free(this->mask);
  free(this->rewrite);
  free(this->inv_rw);
}

string RuleNode::rule_to_str() {
  stringstream result;
  char *s;
  s = array_to_str(match,length,false);
  result << "Match: " << s;
  free(s);
  if (mask) {
    s = array_to_str(mask,length,false);
    result << ", Mask: " << s;
    free(s);
  }
  if (rewrite) {
    s = array_to_str(rewrite,length,false);
    result << ", Rewrite: " << s;
    free(s);
  }
  result << ", iPorts: " << list_to_string(input_ports);
  result << ", oPorts: " << list_to_string(output_ports);
  if (group != 0) {
    char buf[70];
    sprintf(buf,"0x%llx",group);
    result << " (group with " << buf << ")";
  }
  return result.str();
}

string RuleNode::influence_to_str() {
  stringstream result;
  char buf[70];
  char *s;
  result << "Effect On:\n";
  list<Effect *>::iterator eff_it;
  for (eff_it = effect_on->begin(); eff_it != effect_on->end(); eff_it++) {
    list<struct Influence*>::iterator influence = (*eff_it)->influence;
    sprintf(buf,"0x%llx",(*influence)->node->node_id);
    result << "\tRule " << buf << "\n";
  }
  result << "Influenced By:\n";
  list<Influence *>::iterator inf_it;
  for (inf_it = influenced_by->begin(); inf_it != influenced_by->end(); inf_it++) {
    list<struct Effect*>::iterator effect = (*inf_it)->effect;
    sprintf(buf,"0x%llx",(*effect)->node->node_id);
    s = array_to_str((*inf_it)->comm_arr,this->length,false);
    result << "\tRule " << buf << " (h,p) = [" << s << " , " <<
    list_to_string((*inf_it)->ports) << "]\n";
    free(s);
  }
  return result.str();
}

string RuleNode::to_string() {
  stringstream result;
  char buf[70];
  result << string(40, '=') << "\n";
  sprintf(buf,"0x%x",table);
  result << string(4, ' ') << "Table: " << buf;
  sprintf(buf,"0x%llx",node_id);
  result << " Rule: " << buf << "\n";
  result << string(40, '=') << "\n";
  result << rule_to_str() << "\n";
  result << influence_to_str();
  result << pipeline_to_string();
  result << src_flow_to_string();
  return result.str();
}

string flow_to_str2(Flow *f) {
  stringstream str;
  char buf[50];
  while(f->p_flow != f->node->get_EOSFI()) {
    char* h = hs_to_str(f->hs_object);
    sprintf(buf,"0x%llx",f->node->node_id);
    str << h << " @ " << buf << " <-- ";
    free(h);
    f = *f->p_flow;
  }
  char* h = hs_to_str(f->hs_object);
  str << h;
  free(h);
  return str.str();
}

void RuleNode::process_src_flow(Flow *f) {
  if (f) { // flow routing case
    //printf("at node %lx, processing flow: %s\n",node_id,flow_to_str2(f).c_str());
    // add f to source_flow and add it to n_flows of previous flow
    list<struct Flow*>::iterator f_it;

    source_flow.push_front(f);
    f_it = source_flow.begin();
    (*f->p_flow)->n_flows->push_front(f_it);

    // if this flow is in loop, stop propagating and return an error.
    if (is_flow_looped(f)) {
      if (((NetPlumber*)plumber)->loop_callback)
        ((NetPlumber*)plumber)->loop_callback((NetPlumber*)plumber,
                    f,((NetPlumber*)plumber)->loop_callback_data);
      return;
    }
    // diff higher priority rules
    list<struct Influence*>::iterator it;
    f->processed_hs = hs_copy_a(f->hs_object);
    for (it = influenced_by->begin(); it != influenced_by->end(); it++) {
      if (!elem_in_sorted_list(f->in_port, (*it)->ports)) continue;
      hs_diff(f->processed_hs, (*it)->comm_arr);
    }
    // compress h.
    // if compress to empty, free f. else process it.
    if (!hs_compact_m(f->processed_hs,mask)) {
      hs_free(f->processed_hs);
      f->processed_hs = NULL;
    } else {
      f->n_flows = new list< list<struct Flow*>::iterator >();
      if (mask == NULL || rewrite == NULL) {
        propagate_src_flow_on_pipes(f_it);
      } else {
        hs_rewrite(f->processed_hs, mask, rewrite);
        propagate_src_flow_on_pipes(f_it);
      }
    }

  } else { // fresh start case
    list<struct Pipeline*>::iterator it;
    for (it = prev_in_pipeline.begin(); it != prev_in_pipeline.end(); it++) {
      (*(*it)->r_pipeline)->node->
          propagate_src_flows_on_pipe((*it)->r_pipeline);
    }
  }
}
void RuleNode::process_src_flow_at_location(list<struct Flow*>::iterator loc,
                                            array_t *change) {
  Flow *f = *loc;
  if (change && (mask == NULL || rewrite == NULL)) {
    if (f->processed_hs == NULL) return;
    hs_diff(f->processed_hs, change);
  } else {
    if (f->processed_hs) hs_free(f->processed_hs);
    // diff higher priority rules
    list<struct Influence*>::iterator it;
    f->processed_hs = hs_copy_a(f->hs_object);
    for (it = influenced_by->begin(); it != influenced_by->end(); it++) {
      if (!elem_in_sorted_list(f->in_port, (*it)->ports)) continue;
      hs_diff(f->processed_hs, (*it)->comm_arr);
    }
  }
  // compress h.
  // if compress to empty, free f. else process it.
  if (!hs_compact_m(f->processed_hs,mask)) {
    f->node->absorb_src_flow(loc,true);
    hs_free(f->processed_hs);
    f->processed_hs = NULL;
  } else {
    if (!f->n_flows) f->n_flows = new list< list<struct Flow*>::iterator >();
    if (mask == NULL || rewrite == NULL) {
      repropagate_src_flow_on_pipes(loc,change);
    } else {
      hs_rewrite(f->processed_hs, mask, rewrite);
      repropagate_src_flow_on_pipes(loc,NULL);
    }
  }
}


void RuleNode::subtract_infuences_from_flows() {
  /*
   * when a new rule is added, this function is called to updat the lower
   * priority flows.
   */
  list<Effect*>::iterator eff_it;
  list<Flow*>::iterator src_it;
  for (eff_it = effect_on->begin(); eff_it != effect_on->end(); eff_it++) {
    RuleNode *n = (RuleNode *)(*(*eff_it)->influence)->node;
    for (src_it = n->source_flow.begin(); src_it != n->source_flow.end();
        src_it++) {
      if (elem_in_sorted_list((*src_it)->in_port,
                              (*(*eff_it)->influence)->ports)) {
        n->process_src_flow_at_location(src_it,
                                        (*(*eff_it)->influence)->comm_arr);
      }
    }
  }
}

list<struct Influence*>::iterator RuleNode::set_influence_by(Influence *inf) {
  this->influenced_by->push_front(inf);
  return this->influenced_by->begin();
}

list<struct Effect*>::iterator RuleNode::set_effect_on(Effect *eff) {
  this->effect_on->push_front(eff);
  return this->effect_on->begin();
}

int RuleNode::count_effects() {
  return this->effect_on->size();
}

int RuleNode::count_influences() {
  return this->influenced_by->size();
}
