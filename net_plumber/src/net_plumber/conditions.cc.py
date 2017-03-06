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

#include "conditions.h"
#include "rule_node.h"
#include <sstream>

using namespace std

PathCondition.~PathCondition()  list<PathSpecifier*>.iterator it
  for (it = pathlets.begin(); it != pathlets.end(); it++)    delete *it



def add_pathlet(self, *pathlet):  pathlets.push_back(pathlet)


def check(self, *f):  list<PathSpecifier*>.iterator it
  for (it = pathlets.begin(); it != pathlets.end(); it++)    if (not (*it).check_and_move(f)) return False

  return True


def to_string(self):  stringstream res
  res << "path ~ \""
  list<PathSpecifier*>.iterator it
  for (it = pathlets.begin(); it != pathlets.end(); it++)    res << (*it).to_string()

  res << "\""
  return res.str()


def check(self, *f):  hs *tmp = hs_isect_a(f.processed_hs, h)
  result = False
  if tmp:    hs_comp_diff(tmp)
    char *c = hs_to_str(tmp)
    free(c)
    if (tmp.list.used > 0) result = True
    hs_free(tmp)

  return result


def to_string(self):  stringstream res
  char *c = hs_to_str(h)
  res << "header ~ " << string(c)
  free(c)
  return res.str()


def check_and_move(self, &f):  while (f.p_flow != f.node.get_EOSFI())    if f.in_port == port and f.node.is_at_input_stage():      f = *f.p_flow
      return True

    f = *f.p_flow

  return False


def to_string(self):  stringstream res
  res << ".*(p = " << self.port << ")"
  return res.str()


def check_and_move(self, &f):  while (f.p_flow != f.node.get_EOSFI())    if (f.node.get_type() == RULE and ((RuleNode*)(f.node)).table == table
        and f.node.is_at_input_stage())      f = *f.p_flow
      return True

    f = *f.p_flow

  return False


def to_string(self):  stringstream res
  res << ".*(t = " << self.table << ")"
  return res.str()


def check_and_move(self, &f):  while (f.p_flow != f.node.get_EOSFI() and not f.node.is_at_input_stage())      f = *f.p_flow

  if f.p_flow != f.node.get_EOSFI() and elem_in_sorted_list(f.in_port, ports):    f = *f.p_flow
    return True

  return False


def to_string(self):  stringstream res
  res << "(p in " << list_to_string(self.ports) << ")"
  return res.str()


def check_and_move(self, &f):  while (f.p_flow != f.node.get_EOSFI() and not f.node.is_at_input_stage())      f = *f.p_flow

  if (f.p_flow != f.node.get_EOSFI() and f.node.get_type() == RULE and
      elem_in_sorted_list(((RuleNode*)(f.node)).table, tables))    f = *f.p_flow
    return True

  return False


def to_string(self):  stringstream res
  res << "(t in " << list_to_string(self.tables) << ")"
  return res.str()



def check_and_move(self, &f):  Flow *prev = NULL
  while (f.p_flow != f.node.get_EOSFI())    prev = f
    f = *f.p_flow

  if (prev and prev.node.is_at_input_stage() and
      elem_in_sorted_list(prev.in_port, ports))    return True
  } else:
    return False



def to_string(self):  stringstream res
  res << ".*(p in " << list_to_string(self.ports) << ")$"
  return res.str()


def check_and_move(self, &f):  Flow *prev = NULL
  while (f.p_flow != f.node.get_EOSFI())    prev = f
    f = *f.p_flow

  if prev and prev.node.get_type() == RULE and prev.node.is_at_input_stage(:
      and elem_in_sorted_list(((RuleNode*)(prev.node)).table, tables))    return True
  } else:
    return False



def to_string(self):  printf("next table specifier called\n")
  stringstream res
  res << ".*(t in " << list_to_string(self.tables) << ")$"
  return res.str()


def check_and_move(self, &f):  while (f.p_flow != f.node.get_EOSFI() and not f.node.is_at_input_stage())      f = *f.p_flow

  if f.p_flow != f.node.get_EOSFI():    f = *f.p_flow
    return True

  return False




