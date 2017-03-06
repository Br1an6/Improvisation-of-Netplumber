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

#include "conditions.h"
#include "rule_node.h"
#include <sstream>

using namespace std;

PathCondition::~PathCondition() {
  list<PathSpecifier*>::iterator it;
  for (it = pathlets.begin(); it != pathlets.end(); it++) {
    delete *it;
  }
}

void PathCondition::add_pathlet(PathSpecifier *pathlet) {
  pathlets.push_back(pathlet);
}

bool PathCondition::check(Flow *f) {
  list<PathSpecifier*>::iterator it;
  for (it = pathlets.begin(); it != pathlets.end(); it++) {
    if (!(*it)->check_and_move(f)) return false;
  }
  return true;
}

string PathCondition::to_string() {
  stringstream res;
  res << "path ~ \"";
  list<PathSpecifier*>::iterator it;
  for (it = pathlets.begin(); it != pathlets.end(); it++) {
    res << (*it)->to_string();
  }
  res << "\"";
  return res.str();
}

bool HeaderCondition::check(Flow *f) {
  hs *tmp = hs_isect_a(f->processed_hs, h);
  bool result = false;
  if (tmp) {
    hs_comp_diff(tmp);
    char *c = hs_to_str(tmp);
    free(c);
    if (tmp->list.used > 0) result = true;
    hs_free(tmp);
  }
  return result;
}

string HeaderCondition::to_string() {
  stringstream res;
  char *c = hs_to_str(h);
  res << "header ~ " << string(c);
  free(c);
  return res.str();
}

bool PortSpecifier::check_and_move(Flow* &f) {
  while (f->p_flow != f->node->get_EOSFI()) {
    if (f->in_port == port && f->node->is_at_input_stage()) {
      f = *f->p_flow;
      return true;
    }
    f = *f->p_flow;
  }
  return false;
}

string PortSpecifier::to_string() {
  stringstream res;
  res << ".*(p = " << this->port << ")";
  return res.str();
}

bool TableSpecifier::check_and_move(Flow* &f) {
  while (f->p_flow != f->node->get_EOSFI()) {
    if (f->node->get_type() == RULE && ((RuleNode*)(f->node))->table == table
        && f->node->is_at_input_stage()){
      f = *f->p_flow;
      return true;
    }
    f = *f->p_flow;
  }
  return false;
}

string TableSpecifier::to_string() {
  stringstream res;
  res << ".*(t = " << this->table << ")";
  return res.str();
}

bool NextPortsSpecifier::check_and_move(Flow* &f) {
  while (f->p_flow != f->node->get_EOSFI() && !f->node->is_at_input_stage()) {
      f = *f->p_flow;
  }
  if (f->p_flow != f->node->get_EOSFI() && elem_in_sorted_list(f->in_port, ports)) {
    f = *f->p_flow;
    return true;
  }
  return false;
}

string NextPortsSpecifier::to_string() {
  stringstream res;
  res << "(p in " << list_to_string(this->ports) << ")";
  return res.str();
}

bool NextTablesSpecifier::check_and_move(Flow* &f) {
  while (f->p_flow != f->node->get_EOSFI() && !f->node->is_at_input_stage()) {
      f = *f->p_flow;
  }
  if (f->p_flow != f->node->get_EOSFI() && f->node->get_type() == RULE &&
      elem_in_sorted_list(((RuleNode*)(f->node))->table, tables)) {
    f = *f->p_flow;
    return true;
  }
  return false;
}

string NextTablesSpecifier::to_string() {
  stringstream res;
  res << "(t in " << list_to_string(this->tables) << ")";
  return res.str();
}


bool LastPortsSpecifier::check_and_move(Flow* &f) {
  Flow *prev = NULL;
  while (f->p_flow != f->node->get_EOSFI()) {
    prev = f;
    f = *f->p_flow;
  }
  if (prev && prev->node->is_at_input_stage() &&
      elem_in_sorted_list(prev->in_port, ports)) {
    return true;
  } else {
    return false;
  }
}

string LastPortsSpecifier::to_string() {
  stringstream res;
  res << ".*(p in " << list_to_string(this->ports) << ")$";
  return res.str();
}

bool LastTablesSpecifier::check_and_move(Flow* &f) {
  Flow *prev = NULL;
  while (f->p_flow != f->node->get_EOSFI()) {
    prev = f;
    f = *f->p_flow;
  }
  if (prev && prev->node->get_type() == RULE && prev->node->is_at_input_stage()
      && elem_in_sorted_list(((RuleNode*)(prev->node))->table, tables)) {
    return true;
  } else {
    return false;
  }
}

string LastTablesSpecifier::to_string() {
  printf("next table specifier called\n");
  stringstream res;
  res << ".*(t in " << list_to_string(this->tables) << ")$";
  return res.str();
}

bool SkipNextSpecifier::check_and_move(Flow* &f) {
  while (f->p_flow != f->node->get_EOSFI() && !f->node->is_at_input_stage()) {
      f = *f->p_flow;
  }
  if (f->p_flow != f->node->get_EOSFI()) {
    f = *f->p_flow;
    return true;
  }
  return false;
}



