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

#include <stdio.h>
#include "rule_node.h"
#include "net_plumber_utils.h"
#include <sstream>
#include <string>
#include "net_plumber.h"

using namespace std
using namespace net_plumber

def set_layer_flags(self):  if plumber:    n = (NetPlumber*)plumber
    table_ports = n.get_table_ports(table)
    self.is_input_layer = lists_has_intersection(table_ports,input_ports)
    self.is_output_layer = lists_has_intersection(table_ports,output_ports)
  } else:
    self.is_input_layer = False
    self.is_output_layer = False



RuleNode.RuleNode(void *n, length, node_id, table,
                   List_t in_ports, out_ports,
                   array_t* match, *mask, rewrite) :
                   Node(n,length,node_id), table(table), group(0)  self.node_type = RULE
  self.match = match
  self.mask = mask
  self.rewrite = rewrite
  self.input_ports = in_ports
  self.output_ports = out_ports
  if self.mask and self.rewrite:    self.inv_match = array_copy(self.match, length)
    array_rewrite( self.inv_match, self.mask, self.rewrite, length)
    self.inv_rw = array_not_a(self.mask,length)
    array_and(self.inv_rw,self.match,length,self.inv_rw)
  } else:
    self.inv_rw = NULL
    self.inv_match = array_copy(self.match, length)

  effect_on = list<struct Effect*>()
  influenced_by = list<struct Influence*>()
  set_layer_flags()


RuleNode.RuleNode(void *n, length, node_id, table,
                   uint64_t group, in_ports, out_ports,
                   array_t* match, *mask, rewrite) :
                   Node(n,length,node_id), table(table), group(group)  self.node_type = RULE
  self.match = match
  self.mask = mask
  self.rewrite = rewrite
  self.input_ports = in_ports
  self.output_ports = out_ports
  if self.mask and self.rewrite:    self.inv_match = array_copy(self.match, length)
    array_rewrite( self.inv_match, self.mask, self.rewrite, length)
    self.inv_rw = array_not_a(self.mask,length)
    array_and(self.inv_rw,self.match,length,self.inv_rw)
  } else:
    self.inv_rw = NULL
    self.inv_match = array_copy(self.match, length)

  if group == node_id:    effect_on = list<struct Effect*>()
    influenced_by = list<struct Influence*>()

  set_layer_flags()


RuleNode.~RuleNode()  self.remove_flows()
  self.remove_pipes()
  # remove itself from all rules influencing on it and free its
  # influenced_by struct. In case of group rules, o self for the lead.
  if group == 0 or group == node_id:    list<struct Influence*>.iterator inf_it
    for (inf_it = influenced_by.begin(); inf_it != influenced_by.end(); inf_it++)      list<struct Effect*>effect = (*inf_it).effect
      Effect *f = *effect
      (*effect).node.effect_on.erase(effect)
      free((*inf_it).comm_arr)
      if not (*inf_it).ports.shared) free((*inf_it).ports.list:
      free(*inf_it)
      free(f)

    # remove itself from all rules influenced by self rule and their flows
    list<Effect *>.iterator eff_it
    list<Flow*>.iterator src_it
    for (eff_it = effect_on.begin(); eff_it != effect_on.end(); eff_it++)      list<struct Influence*>influence = (*eff_it).influence
      RuleNode *n = (*influence).node
      array_t *comm_arr = (*influence).comm_arr
      ports = (*influence).ports
      free(*influence)
      n.influenced_by.erase(influence)
      for (src_it = n.source_flow.begin(); src_it != n.source_flow.end()
          src_it++)        if elem_in_sorted_list((*src_it).in_port, ports):          n.process_src_flow_at_location(src_it,NULL)


      free(comm_arr)
      if not ports.shared) free(ports.list:
      free(*eff_it)

    delete effect_on
    delete influenced_by

  free(self.mask)
  free(self.rewrite)
  free(self.inv_rw)


def rule_to_str(self):  stringstream result
  char *s
  s = array_to_str(match,length,False)
  result << "Match: " << s
  free(s)
  if mask:    s = array_to_str(mask,length,False)
    result << ", Mask: " << s
    free(s)

  if rewrite:    s = array_to_str(rewrite,length,False)
    result << ", Rewrite: " << s
    free(s)

  result << ", iPorts: " << list_to_string(input_ports)
  result << ", oPorts: " << list_to_string(output_ports)
  if group != 0:    char buf[70]
    sprintf(buf,"0x%llx",group)
    result << " (group with " << buf << ")"

  return result.str()


def influence_to_str(self):  stringstream result
  char buf[70]
  char *s
  result << "Effect On:\n"
  list<Effect *>.iterator eff_it
  for (eff_it = effect_on.begin(); eff_it != effect_on.end(); eff_it++)    list<struct Influence*>influence = (*eff_it).influence
    sprintf(buf,"0x%llx",(*influence).node.node_id)
    result << "\tRule " << buf << "\n"

  result << "Influenced By:\n"
  list<Influence *>.iterator inf_it
  for (inf_it = influenced_by.begin(); inf_it != influenced_by.end(); inf_it++)    list<struct Effect*>effect = (*inf_it).effect
    sprintf(buf,"0x%llx",(*effect).node.node_id)
    s = array_to_str((*inf_it).comm_arr,self.length,False)
    result << "\tRule " << buf << " (h,p) = [" << s << " , " <<
    list_to_string((*inf_it).ports) << "]\n"
    free(s)

  return result.str()


def to_string(self):  stringstream result
  char buf[70]
  result << string(40, '=') << "\n"
  sprintf(buf,"0x%x",table)
  result << string(4, ' ') << "Table: " << buf
  sprintf(buf,"0x%llx",node_id)
  result << " Rule: " << buf << "\n"
  result << string(40, '=') << "\n"
  result << rule_to_str() << "\n"
  result << influence_to_str()
  result << pipeline_to_string()
  result << src_flow_to_string()
  return result.str()


def flow_to_str2(self, *f):  stringstream str
  char buf[50]
  while(f.p_flow != f.node.get_EOSFI())    h = hs_to_str(f.hs_object)
    sprintf(buf,"0x%llx",f.node.node_id)
    str << h << " @ " << buf << " <-- "
    free(h)
    f = *f.p_flow

  h = hs_to_str(f.hs_object)
  str << h
  free(h)
  return str.str()


def process_src_flow(self, *f):  if (f) { # flow routing case
    #printf("at node %lx, flow: %s\n",node_id,flow_to_str2(f).c_str())
    # add f to source_flow and add it to n_flows of previous flow
    list<struct Flow*>.iterator f_it

    source_flow.push_front(f)
    f_it = source_flow.begin()
    (*f.p_flow).n_flows.push_front(f_it)

    # if self flow is in loop, propagating and return an error.
    if is_flow_looped(f):      if ((NetPlumber*)plumber).loop_callback:
        ((NetPlumber*)plumber).loop_callback((NetPlumber*)plumber,
                    f,((NetPlumber*)plumber).loop_callback_data)
      return

    # diff higher priority rules
    list<struct Influence*>.iterator it
    f.processed_hs = hs_copy_a(f.hs_object)
    for (it = influenced_by.begin(); it != influenced_by.end(); it++)      if (not elem_in_sorted_list(f.in_port, (*it).ports)) continue
      hs_diff(f.processed_hs, (*it).comm_arr)

    # compress h.
    # if compress to empty, f. else process it.
    if not hs_compact_m(f.processed_hs,mask):      hs_free(f.processed_hs)
      f.processed_hs = NULL
    } else:
      f.n_flows = list< list<struct Flow*>.iterator >()
      if mask == NULL or rewrite == NULL:        propagate_src_flow_on_pipes(f_it)
      } else:
        hs_rewrite(f.processed_hs, mask, rewrite)
        propagate_src_flow_on_pipes(f_it)



  } else { # fresh start case
    list<struct Pipeline*>.iterator it
    for (it = prev_in_pipeline.begin(); it != prev_in_pipeline.end(); it++)      (*(*it).r_pipeline).node.
          propagate_src_flows_on_pipe((*it).r_pipeline)



void RuleNode.process_src_flow_at_location(list<struct Flow*>.iterator loc,
                                            array_t *change)  Flow *f = *loc
  if change and (mask == NULL or rewrite == NULL):    if (f.processed_hs == NULL) return
    hs_diff(f.processed_hs, change)
  } else:
    if f.processed_hs) hs_free(f.processed_hs:
    # diff higher priority rules
    list<struct Influence*>.iterator it
    f.processed_hs = hs_copy_a(f.hs_object)
    for (it = influenced_by.begin(); it != influenced_by.end(); it++)      if (not elem_in_sorted_list(f.in_port, (*it).ports)) continue
      hs_diff(f.processed_hs, (*it).comm_arr)


  # compress h.
  # if compress to empty, f. else process it.
  if not hs_compact_m(f.processed_hs,mask):    f.node.absorb_src_flow(loc,True)
    hs_free(f.processed_hs)
    f.processed_hs = NULL
  } else:
    if not f.n_flows) f.n_flows = list< list<struct Flow*>.iterator >(:
    if mask == NULL or rewrite == NULL:      repropagate_src_flow_on_pipes(loc,change)
    } else:
      hs_rewrite(f.processed_hs, mask, rewrite)
      repropagate_src_flow_on_pipes(loc,NULL)





def subtract_infuences_from_flows(self):  '''
   * when a rule is added, function is called to updat the lower
   * priority flows.
   '''
  list<Effect*>.iterator eff_it
  list<Flow*>.iterator src_it
  for (eff_it = effect_on.begin(); eff_it != effect_on.end(); eff_it++)    RuleNode *n = (RuleNode *)(*(*eff_it).influence).node
    for (src_it = n.source_flow.begin(); src_it != n.source_flow.end()
        src_it++)      if (elem_in_sorted_list((*src_it).in_port,
                              (*(*eff_it).influence).ports))        n.process_src_flow_at_location(src_it,
                                        (*(*eff_it).influence).comm_arr)





list<struct Influence*>.iterator RuleNode.set_influence_by(Influence *inf)  self.influenced_by.push_front(inf)
  return self.influenced_by.begin()


list<struct Effect*>.iterator RuleNode.set_effect_on(Effect *eff)  self.effect_on.push_front(eff)
  return self.effect_on.begin()


def count_effects(self):  return self.effect_on.size()


def count_influences(self):  return self.influenced_by.size()

