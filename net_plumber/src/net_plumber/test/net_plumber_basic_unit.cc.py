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

#include "net_plumber_basic_unit.h"
#include "../rule_node.h"
#include "../net_plumber.h"
#include "../net_plumber_utils.h"
extern "C"  #include "../../headerspace/array.h"
#include "../../headerspace/hs.h"


using namespace net_plumber

def setUp(self):


def tearDown(self):


def test_rule_node_create(self):  printf("\n")
  in_ports = make_sorted_list(2,2,3)
  out_ports = make_sorted_list(2,1,4)
  array_t *match = array_create(2,BIT_X)
  array_t *mask = array_from_str ("11111111,10000000")
  array_t *rewrite = array_from_str ("00000000,00000011")
  array_t *inv_match = array_from_str ("xxxxxxxx,x0000011")
  array_t *inv_rw = array_from_str ("00000000,0xxxxxxx")
  RuleNode *r = RuleNode(NULL,2,1,1,in_ports,out_ports,match,mask,rewrite)
  CPPUNIT_ASSERT(r.output_ports.size == 2)
  CPPUNIT_ASSERT(array_is_eq(r.inv_match,inv_match,2))
  CPPUNIT_ASSERT(array_is_eq(r.inv_rw,inv_rw,2))
  #printf("%s\n",r.to_string().c_str())
  free(inv_rw)
  free(inv_match)
  delete r


def test_create_topology(self):  printf("\n")
  NetPlumber *n = NetPlumber(1)
  n.add_link(1,2)
  n.add_link(1,3)
  n.add_link(2,1)
  #n.print_topology()
  CPPUNIT_ASSERT(n.get_dst_ports(1).size()==2)
  CPPUNIT_ASSERT(n.get_dst_ports(2).size()==1)
  CPPUNIT_ASSERT(n.get_src_ports(3).size()==1)
  delete n


def test_create_rule_id(self):  printf("\n")
  NetPlumber *n = NetPlumber(1)
  n.add_table(1,make_sorted_list(1,1))
  # two conseq. rules
  in_ports = make_sorted_list(1,1)
  out_ports = make_sorted_list(1,2)
  array_t *match = array_create(1,BIT_X)
  id1 = n.add_rule(1,-1,in_ports,out_ports,match,NULL,NULL)
  in_ports = make_sorted_list(1,2)
  out_ports = make_sorted_list(1,3)
  match = array_create(1,BIT_X)
  id2 = n.add_rule(1,-1,in_ports,out_ports,match,NULL,NULL)
  CPPUNIT_ASSERT(id2-id1==1)
  # add to an invalid table
  in_ports = make_sorted_list(1,1)
  out_ports = make_sorted_list(1,2)
  match = array_create(1,BIT_X)
  id3 = n.add_rule(2,-1,in_ports,out_ports,match,NULL,NULL)
  CPPUNIT_ASSERT(id3==0)
  # add to a removed table
  n.remove_table(1)
  in_ports = make_sorted_list(1,1)
  out_ports = make_sorted_list(1,2)
  match = array_create(1,BIT_X)
  id4 = n.add_rule(1,-1,in_ports,out_ports,match,NULL,NULL)
  CPPUNIT_ASSERT(id4==0)
  delete n




