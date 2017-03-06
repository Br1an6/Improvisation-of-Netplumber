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

#include "net_plumber_plumbing_unit.h"
#include "../net_plumber_utils.h"
#include <sstream>

using namespace net_plumber
using namespace std
using namespace log4cxx

LoggerPtr NetPlumberPlumbingTest.logger(
    Logger.getLogger("NetPlumber-PlumbingUnitTest"))

def setUp(self):  N = NetPlumber(1)
  N.add_link(2,4)
  N.add_link(4,2)
  N.add_link(3,6)
  N.add_link(6,3)
  N.add_link(5,8)
  N.add_link(8,5)
  N.add_link(7,9)
  N.add_link(9,7)
  N.add_table(1, make_sorted_list(3,1,2,3))
  N.add_table(2, make_sorted_list(3,4,5,11))
  N.add_table(3, make_sorted_list(2,6,12))
  N.add_table(4, make_sorted_list(2,8,13))
  node_ids.push_back(N.add_rule(1,-1,
              make_sorted_list(1,1),
              make_sorted_list(1,2),
              array_from_str ("1010xxxx"),
              NULL,
              NULL))
  node_ids.push_back(N.add_rule(1,-1,
              make_sorted_list(1,1),
              make_sorted_list(1,2),
              array_from_str ("10001xxx"),
              NULL,
              NULL))
  node_ids.push_back(N.add_rule(1,-1,
              make_sorted_list(2,1,2),
              make_sorted_list(1,3),
              array_from_str ("10xxxxxx"),
              NULL,
              NULL))
  node_ids.push_back(N.add_rule(2,-1,
              make_sorted_list(1,4),
              make_sorted_list(2,5,11),
              array_from_str ("1011xxxx"),
              array_from_str ("11100111"),
              array_from_str ("00001000")))
  node_ids.push_back(N.add_rule(2,-1,
              make_sorted_list(1,4),
              make_sorted_list(1,5),
              array_from_str ("10xxxxxx"),
              array_from_str ("10011111"),
              array_from_str ("01100000")))
  node_ids.push_back(N.add_rule(3,-1,
              make_sorted_list(2,6,12),
              make_sorted_list(1,7),
              array_from_str ("101xxxxx"),
              array_from_str ("11111000"),
              array_from_str ("00000111")))
  node_ids.push_back(N.add_rule(4,-1,
              make_sorted_list(1,8),
              make_sorted_list(1,13),
              array_from_str ("xxx010xx"),
              NULL,
              NULL))
  memset(&A,0, A)


def tearDown(self):  delete N


def test_setup(self):  printf("\n")
  int stats[7][4]=      {1,0,1,0},
      {1,0,1,0},
      {1,0,0,2},
      {1,0,1,0},
      {1,2,0,1},
      {0,1,0,0},
      {0,2,0,0

  #N.print_plumbing_network()
  self.verify_pipe_stats(stats)


def test_pipeline_add_rule(self):  printf("\n")
  node_ids.push_back(N.add_rule(1,0,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xx11xxxx"),
              NULL,
              NULL))
  int stats[8][4]=      {1,0,1,0},
      {1,0,1,0},
      {1,0,0,3},
      {1,1,1,0},
      {1,3,0,1},
      {0,2,0,0},
      {0,2,0,0},
      {3,0,1,0} #new rule

  #N.print_plumbing_network()
  self.verify_pipe_stats(stats)


def test_pipeline_remove_rule(self):  printf("\n")
  N.remove_rule(node_ids[4])
  int stats[7][4]=      {0,0,1,0},
      {0,0,1,0},
      {1,0,0,2},
      {1,0,0,0},
      {0,0,0,0},
      {0,1,0,0},
      {0,1,0,0

  #N.print_plumbing_network()
  self.verify_pipe_stats(stats)


def test_pipeline_add_group_rule(self):  printf("\n")
  node_ids.push_back(N.add_rule_to_group(1,1,
              make_sorted_list(1,1),
              make_sorted_list(1,2),
              array_from_str ("xxxx11xx"),
              array_from_str ("11001111"),
              array_from_str ("00000000"),0))
  node_ids.push_back(N.add_rule_to_group(1,0,
              make_sorted_list(1,1),
              make_sorted_list(1,3),
              array_from_str ("xxxx11xx"),
              NULL,
              NULL,node_ids[node_ids.size()-1]))
  int stats[9][4]=      {1,0,2,0},
      {1,0,1,1},
      {1,0,0,3},
      {1,0,1,0},
      {1,3,0,1},
      {0,2,0,0},
      {0,2,0,0},
      {1,0,2,1}, #new rule 1
      {1,0,2,1}  #new rule 2

  #N.print_plumbing_network()
  self.verify_pipe_stats(stats)


def test_pipeline_add_group_rule_mix(self):  printf("\n")
  self.test_pipeline_add_group_rule()
  node_ids.push_back(N.add_rule(1,2,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xx11xxxx"),
              NULL,
              NULL))
  int stats[10][4]=      {1,0,2,0},
      {1,0,1,1},
      {1,0,0,4},
      {1,1,1,0},
      {1,4,0,1},
      {0,3,0,0},
      {0,2,0,0},
      {1,0,3,1}, #new rule 1
      {1,0,3,1}, #new rule 2
      {3,0,1,1}  #new rule 3

  #N.print_plumbing_network()
  self.verify_pipe_stats(stats)


def test_pipeline_remove_group_rule(self):  printf("\n")
  self.test_pipeline_add_group_rule()
  N.remove_rule(node_ids[node_ids.size()-1])
  node_ids.pop_back()
  node_ids.pop_back()
  self.test_setup()


def test_pipeline_add_link(self):  printf("\n")
  N.add_link(11,12)
  int stats[7][4]=      {1,0,1,0},
      {1,0,1,0},
      {1,0,0,2},
      {2,0,1,0},
      {1,2,0,1},
      {0,2,0,0},
      {0,2,0,0

  #N.print_plumbing_network()
  self.verify_pipe_stats(stats)


def test_pipeline_remove_link(self):  self.test_pipeline_add_link()
  N.remove_link(11,12)
  #N.print_plumbing_network()
  self.test_setup()


def test_pipeline_add_source(self):  printf("\n")
  N.add_link(100,1)
  hs *h = hs_create(1)
  hs_add(h, array_from_str ("1xxxxxxx"))
  node_ids.push_back(
      N.add_source(h, make_sorted_list(1,100))
      )
  int stats[8][4]=      {1,1,1,0},
      {1,1,1,0},
      {1,1,0,2},
      {1,0,1,0},
      {1,2,0,1},
      {0,1,0,0},
      {0,2,0,0},
      {3,0,0,0

  #N.print_plumbing_network()
  self.verify_pipe_stats(stats)


def test_pipeline_remove_source(self):  printf("\n")
  N.add_link(100,1)
  hs *h = hs_create(1)
  hs_add(h, array_from_str ("1xxxxxxx"))
  id = N.add_source(h, make_sorted_list(1,100))
  #N.print_plumbing_network()
  N.remove_source(id)
  self.test_setup()


def test_pipeline_add_probe(self):  printf("\n")
  N.add_link(13,200)
  node_ids.push_back(N.add_source_probe(
      make_sorted_list(1,200), EXISTENTIAL, TrueCondition(),
      TrueCondition(),NULL, NULL))
  int stats[8][4]=      {1,0,1,0},
      {1,0,1,0},
      {1,0,0,2},
      {1,0,1,0},
      {1,2,0,1},
      {0,1,0,0},
      {1,2,0,0},
      {0,1,0,0},

  #N.print_plumbing_network()
  self.verify_pipe_stats(stats)


def test_pipeline_remove_probe(self):  self.test_pipeline_add_probe()
  N.remove_source_probe(node_ids[7])
  node_ids.pop_back()
  #N.print_plumbing_network()
  self.test_setup()


def test_pipeline_shared_ports(self):  printf("\n")
  N.add_table(5,make_sorted_list(3,14,15,16))
  N.add_link(11,14)
  N.add_link(15,8)
  node_ids.push_back(N.add_rule(5,-1,
              make_sorted_list(0),
              make_sorted_list(1,15),
              array_from_str ("10xxxxxx"),
              array_from_str ("10011111"),
              array_from_str ("01100000")))
  node_ids.push_back(N.add_rule(5,-1,
              make_sorted_list(0),
              make_sorted_list(1,16),
              array_from_str ("1000xxxx"),
              NULL,
              NULL))
  node_ids.push_back(N.add_rule(5,-1,
              make_sorted_list(0),
              make_sorted_list(1,15),
              array_from_str ("1010xxxx"),
              array_from_str ("10011111"),
              array_from_str ("01000000")))
  int stats[10][4]=      {1,0,1,0},
      {1,0,1,0},
      {1,0,0,2},
      {3,0,1,0},
      {1,2,0,1},
      {0,1,0,0},
      {0,4,0,0},
      {1,1,2,0},
      {0,0,0,1},
      {1,1,0,1

  #N.print_plumbing_network()
  self.verify_pipe_stats(stats)


def test_routing_add_source(self):  printf("\n")
  N.add_link(100,1)
  hs *h = hs_create(1)
  hs_add(h, array_from_str ("1xxxxxxx"))
  N.add_source(h, make_sorted_list(1,100))
  int stats[7][2] =      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_remove_source(self):  printf("\n")
  N.add_link(100,1)
  hs *h = hs_create(1)
  hs_add(h, array_from_str ("1xxxxxxx"))
  id1 = N.add_source(h, make_sorted_list(1,100))
  h = hs_create(1)
  hs_add(h, array_from_str ("xxxxxxxx"))
  id2 = N.add_source(h, make_sorted_list(1,100))
  #N.print_plumbing_network()
  N.remove_source(id2)
  int stats[7][2] =      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_add_fwd_rule_lower_priority(self):  printf("\n")
  self.test_routing_add_source()
  node_ids.push_back(N.add_rule(1,-1,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xxx11xxx"),
              NULL,
              NULL))
  int stats[8][2] =      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0},
      {1,0},

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_add_rw_rule_lower_priority(self):  printf("\n")
  self.test_routing_add_source()
  node_ids.push_back(N.add_rule(1,-1,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xxx11xxx"),
              array_from_str ("10111111"),
              array_from_str ("00000000")))
  int stats[8][2] =      {1,0},
      {1,0},
      {1,2},
      {1,0},
      {3,0},
      {2,0},
      {3,0},
      {1,0},

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_add_fwd_rule_higher_priority(self):  printf("\n")
  self.test_routing_add_source()
  node_ids.push_back(N.add_rule(1,0,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xxxx11xx"),
              NULL,
              NULL))
  int stats[8][2] =      {1,1},
      {1,0},
      {1,3},
      {1,0},
      {3,1},
      {2,0},
      {2,0},
      {1,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_add_rw_rule_higher_priority(self):  printf("\n")
  self.test_routing_add_source()
  node_ids.push_back(N.add_rule(2,0,
              make_sorted_list(1,4),
              make_sorted_list(1,5),
              array_from_str ("10xx1xxx"),
              array_from_str ("00111111"),
              array_from_str ("01000000")
              ))
  int stats[8][2] =      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {1,0},
      {1,0},
      {2,0},
      {2,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_add_rw_rule_higher_priority2(self):  printf("\n")
  self.test_routing_add_source()
  node_ids.push_back(N.add_rule(3,0,
              make_sorted_list(1,6),
              make_sorted_list(1,5),
              array_from_str ("1xxxxxxx"),
              array_from_str ("11011111"),
              array_from_str ("00000000")
              ))
  int stats[8][2] =      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {0,0},
      {2,0},
      {1,1

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_add_group_rule_mid_priority(self):  printf("\n")
  self.test_routing_add_source()
  node_ids.push_back(N.add_rule_to_group(1,1,
              make_sorted_list(1,1),
              make_sorted_list(1,2),
              array_from_str ("xxxx11xx"),
              array_from_str ("11100111"),
              array_from_str ("00000000"),0))
  node_ids.push_back(N.add_rule_to_group(1,0,
              make_sorted_list(1,1),
              make_sorted_list(1,3),
              array_from_str ("xxxx11xx"),
              NULL,
              NULL,node_ids[node_ids.size()-1]))
  int stats[9][2] =      {1,0},
      {1,0},
      {1,3},
      {0,0},
      {3,0},
      {2,0},
      {2,0},
      {1,0}, # rule 1
      {1,1}  # rule 2

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_add_rule_block_bounce(self):  printf("\n")
  self.test_routing_add_source()
  node_ids.push_back(N.add_rule(1,0,
              make_sorted_list(3,1,2,3),
              make_sorted_list(2,2,3),
              array_from_str ("xxxx11xx"),
              NULL,
              NULL))
  node_ids.push_back(N.add_rule(3,0,
              make_sorted_list(1,6),
              make_sorted_list(1,6),
              array_from_str ("100x11xx"),
              NULL,
              NULL))
  int stats[9][2] =      {1,1},
      {1,0},
      {1,3},
      {1,0},
      {3,1},
      {2,0},
      {2,0},
      {1,0},
      {1,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_remove_group_rule_mid_priority(self):  self.test_routing_add_group_rule_mid_priority()
  N.remove_rule(node_ids[node_ids.size()-1])
  node_ids.pop_back()
  node_ids.pop_back()
  int stats[7][2] =      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_remove_fwd_rule_lower_priority(self):  printf("\n")
  self.test_routing_add_source()
  N.remove_rule(node_ids[2])
  std.vector<uint64_t>it = node_ids.begin()
  advance(it,2)
  node_ids.erase(it)
  int stats[6][2] =      {1,0},
      {1,0},
      {0,0},
      {2,0},
      {0,0},
      {2,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_remove_rw_rule_lower_priority(self):  printf("\n")
  self.test_routing_add_source()
  N.remove_rule(node_ids[4])
  std.vector<uint64_t>it = node_ids.begin()
  advance(it,4)
  node_ids.erase(it)
  int stats[6][2] =      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {1,0},
      {0,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_remove_fwd_rule_higher_priority(self):  self.test_routing_add_fwd_rule_higher_priority()
  N.remove_rule(node_ids.back())
  node_ids.pop_back()
  int stats[7][2] =      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_remove_rw_rule_higher_priority(self):  self.test_routing_add_rw_rule_higher_priority()
  N.remove_rule(node_ids.back())
  node_ids.pop_back()
  int stats[7][2] =      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_add_link(self):  self.test_routing_add_fwd_rule_higher_priority()
  node_ids.push_back(N.add_rule(3,0,
              make_sorted_list(1,12),
              make_sorted_list(1,7),
              array_from_str ("10xxxxx1"),
              array_from_str ("00011000"),
              array_from_str ("00000000")))
  N.add_link(11,12)
  N.add_link(7,8)
  int stats[9][2] =      {1,1},
      {1,0},
      {1,3},
      {1,0},
      {3,1},
      {3,0},
      {3,0},
      {1,0},
      {1,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats)


def test_routing_remove_link(self):  self.test_routing_add_link()

  N.remove_link(7,8)
  int stats1[9][2] =      {1,1},
      {1,0},
      {1,3},
      {1,0},
      {3,1},
      {3,0},
      {2,0},
      {1,0},
      {1,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats1)
  N.remove_link(11,12)
  int stats2[9][2] =        {1,1},
        {1,0},
        {1,3},
        {1,0},
        {3,1},
        {2,0},
        {2,0},
        {1,0},
        {0,0

  #N.print_plumbing_network()
  self.verify_source_flow_stats(stats2)


def loop_detected(self, *N, *f, data):  bool *is_looped = (bool *)(data)
  *is_looped = True
  return
  uint32_t table_ids[4] = {1,3,2,1
  for (int i=0; i < 4; i++)    RuleNode *r = (RuleNode*)f.node
    CPPUNIT_ASSERT(r.table == table_ids[i])
    f = *f.p_flow



def test_detect_loop(self):  printf("\n")
  bool is_looped
  N.loop_callback = loop_detected
  N.loop_callback_data = &is_looped
  self.test_routing_add_fwd_rule_higher_priority()
  N.add_link(11,12)
  N.add_link(14,15)
  node_ids.push_back(N.add_rule(3,0,
              make_sorted_list(1,12),
              make_sorted_list(1,14),
              array_from_str ("10xxxxx1"),
              NULL,
              NULL))
  node_ids.push_back(N.add_rule(1,0,
              make_sorted_list(1,15),
              make_sorted_list(1,2),
              array_from_str ("10xxxxxx"),
              NULL,
              NULL))
  #N.print_plumbing_network()
  CPPUNIT_ASSERT(is_looped)


void probe_fire_counter(void *caller, *p, *f,
                   void *data, t)  probe_counter_t *a = (probe_counter_t*)data
  switch (t)    case(STARTED_FALSE): (*a).start_False++; break
    case(STARTED_TRUE): (*a).start_True++; break
    case(TRUE_TO_FALSE): (*a).True_to_False++; break
    case(FALSE_TO_TRUE): (*a).False_to_True++; break
    case(MORE_FALSE): (*a).more_False++; break
    case(LESS_FALSE): (*a).less_False++; break
    case(MORE_TRUE): (*a).more_True++; break
    case(LESS_TRUE): (*a).less_True++; break
    default: break



def test_False_probe(self):  self.test_routing_add_source()
  N.add_link(13,200)
  a = {0
  r = {0,3,0,0,0,0,0,0
  node_ids.push_back(N.add_source_probe(
       make_sorted_list(1,200), EXISTENTIAL, TrueCondition(),
       FalseCondition(), probe_fire_counter, &a))
  node_ids.push_back(N.add_source_probe(
       make_sorted_list(1,200), UNIVERSAL, TrueCondition(),
       FalseCondition(), probe_fire_counter, &a))
  self.check_probe_counter(a,r)
  #N.print_plumbing_network()


def test_True_probe(self):  self.test_routing_add_source()
  N.add_link(13,200)
  a = {0
  r = {3,0,0,0,0,0,0,0
  node_ids.push_back(N.add_source_probe(
       make_sorted_list(1,200), EXISTENTIAL, TrueCondition(),
       TrueCondition(), probe_fire_counter, &a))
  node_ids.push_back(N.add_source_probe(
       make_sorted_list(1,200), UNIVERSAL, TrueCondition(),
       TrueCondition(), probe_fire_counter, &a))
  self.check_probe_counter(a,r)


def test_port_probe(self):  self.test_routing_add_source()
  N.add_link(13,200)
  a = {0
  r = {1,0,0,0,0,0,0,0
  PathCondition *c = PathCondition()
  c.add_pathlet(new PortSpecifier(4))
  N.add_source_probe(
         make_sorted_list(1,200), UNIVERSAL, TrueCondition(),
         c, probe_fire_counter, &a)
  self.check_probe_counter(a,r)


def test_table_probe(self):  self.test_routing_add_source()
  N.add_link(13,200)
  a = {0
  r = {2,0,0,0,0,0,0,0
  PathCondition *c = PathCondition()
  c.add_pathlet(new TableSpecifier(2))
  PathCondition *f = PathCondition()
  c.add_pathlet(new LastPortsSpecifier(make_sorted_list(1,1)))
  N.add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, f,
         c, probe_fire_counter, &a)
  self.check_probe_counter(a,r)


def test_reachability(self):  self.test_routing_add_source()
  N.add_link(13,200)
  a = {0
  r = {2,0,0,0,0,0,0,0
  PathCondition *c = PathCondition()
  c.add_pathlet(new LastPortsSpecifier(make_sorted_list(1,1)))
  N.add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, TrueCondition(),
         c, probe_fire_counter, &a)
  self.check_probe_counter(a,r)


def test_probe_transition_no_update_add_rule(self):  self.test_routing_add_source()
  N.add_link(13,200)
  memset(&A,0, A)
  r = {2,0,0,0,0,0,0,0
  PathCondition *c = PathCondition()
  c.add_pathlet(new LastPortsSpecifier(make_sorted_list(1,1)))
  N.add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, TrueCondition(),
         c, probe_fire_counter, &A)
  node_ids.push_back(N.add_rule(1,-1,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xxx11xxx"),
              NULL,
              NULL))
  #N.print_plumbing_network()
  self.check_probe_counter(A,r)


def test_probe_transition_no_update_remove_rule(self):  self.test_probe_transition_no_update_add_rule()
  memset(&A,0, A)
  r = {0,0,0,0,0,0,0,0
  N.remove_rule(node_ids[node_ids.size()-1])
  self.check_probe_counter(A,r)


def test_probe_transition_with_update_add_rule1(self):  self.test_routing_add_source()
  N.add_link(13,200)
  memset(&A,0, A)
  r = {2,0,0,0,1,0,0,0
  PathCondition *c = PathCondition()
  c.add_pathlet(new LastPortsSpecifier(make_sorted_list(1,1)))
  N.add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, TrueCondition(),
         c, probe_fire_counter, &A)
  node_ids.push_back(N.add_rule(3,0,
              make_sorted_list(1,6),
              make_sorted_list(1,5),
              array_from_str ("1xxxxxxx"),
              array_from_str ("11100111"),
              array_from_str ("00001000")
              ))
  #N.print_plumbing_network()
  self.check_probe_counter(A,r)


def test_probe_transition_with_update_add_rule2(self):  self.test_routing_add_source()
  N.add_link(13,200)
  memset(&A,0, A)
  r = {2,0,1,0,0,0,0,1
  PathCondition *c = PathCondition()
  c.add_pathlet(new LastPortsSpecifier(make_sorted_list(1,1)))
  N.add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, TrueCondition(),
         c, probe_fire_counter, &A)
  node_ids.push_back(N.add_rule(1,0,
              make_sorted_list(1,1),
              make_sorted_list(1,50),
              array_from_str ("10xxxxxx"),
              NULL,
              NULL))
  #N.print_plumbing_network()
  self.check_probe_counter(A,r)


def test_probe_transition_with_update_remove_rule(self):  self.test_probe_transition_with_update_add_rule2()
  memset(&A,0, A)
  N.remove_rule(node_ids[node_ids.size()-1])
  r = {0,0,0,1,1,0,0,0
  self.check_probe_counter(A,r)


def test_probe_transition_add_link(self):  printf("\n")
  N.add_link(13,200)
  memset(&A,0, A)
  r = {0,1,0,1,0,0,0,0
  PathCondition *c = PathCondition()
  c.add_pathlet(new TableSpecifier(3))
  N.add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, TrueCondition(),
         c, probe_fire_counter, &A)
  self.test_routing_add_link()
  #N.print_plumbing_network()
  self.check_probe_counter(A,r)


def test_probe_transition_remove_link(self):  printf("\n")
  N.add_link(13,200)
  memset(&A,0, A)
  r = {0,1,1,1,0,0,0,0
  PathCondition *c = PathCondition()
  c.add_pathlet(new TableSpecifier(3))
  N.add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, TrueCondition(),
         c, probe_fire_counter, &A)
  self.test_routing_remove_link()
  #N.print_plumbing_network()
  self.check_probe_counter(A,r)


def test_probe_transition_add_source(self):  printf("\n")
  self.test_routing_add_source()
  N.add_link(13,200)
  N.add_link(300,4)
  memset(&A,0, A)
  r = {0,1,0,1,1,0,0,0
  PathCondition *c = PathCondition()
  c.add_pathlet(new LastPortsSpecifier(make_sorted_list(1,4)))
  N.add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, TrueCondition(),
         c, probe_fire_counter, &A)
  hs *h = hs_create(1)
  hs_add(h, array_from_str ("xxxxxxxx"))
  node_ids.push_back(
      N.add_source(h, make_sorted_list(1,300))
      )

  #N.print_plumbing_network()
  self.check_probe_counter(A,r)


def test_probe_transition_remove_source(self):  printf("\n")
  self.test_probe_transition_add_source()
  memset(&A,0, A)
  r = {0,0,1,0,0,0,0,1
  N.remove_source(node_ids[node_ids.size()-1])
  #N.print_plumbing_network()
  self.check_probe_counter(A,r)


''' * * * * * * * * * *
 * Testing FUnctions *
 * * * * * * * * * * *
 '''

def verify_pipe_stats(self, stats[][4]):  for (i = 0; i < node_ids.size(); i++)      int fwd_pipeline
      int bck_pipeline
      int influence_on
      int influenced_by
      N.get_pipe_stats(node_ids[i],fwd_pipeline,bck_pipeline,
          influence_on,influenced_by)
      stringstream error_msg
      error_msg << "(fwd, bck, inf_on, inf_by) - Obtained: " << fwd_pipeline <<
          " , " << bck_pipeline << " , " << influence_on << " , " <<
          influenced_by << " Expected " << stats[i][0] << " , " << stats[i][1]
          << " , " << stats[i][2] << " , " << stats[i][3]
      LOG4CXX_DEBUG(logger,error_msg.str())
      CPPUNIT_ASSERT(fwd_pipeline == stats[i][0])
      CPPUNIT_ASSERT(bck_pipeline == stats[i][1])
      CPPUNIT_ASSERT(influence_on == stats[i][2])
      CPPUNIT_ASSERT(influenced_by == stats[i][3])



def verify_source_flow_stats(self, stats[][2]):  for (i = 0; i < node_ids.size(); i++)    int inc, exc
    N.get_source_flow_stats(node_ids[i], inc, exc)
    stringstream error_msg
    error_msg << "(included wc, excluded_wc) - Obtained: " << inc <<
        " , " << exc << " Expected " << stats[i][0] << " , " << stats[i][1]
    LOG4CXX_DEBUG(logger,error_msg.str())
    CPPUNIT_ASSERT(inc == stats[i][0])
    CPPUNIT_ASSERT(exc == stats[i][1])



void NetPlumberPlumbingTest.check_probe_counter(
    probe_counter_t result, expected)  CPPUNIT_ASSERT(result.start_True == expected.start_True)
  CPPUNIT_ASSERT(result.start_False == expected.start_False)
  CPPUNIT_ASSERT(result.True_to_False == expected.True_to_False)
  CPPUNIT_ASSERT(result.False_to_True == expected.False_to_True)
  CPPUNIT_ASSERT(result.more_True == expected.more_True)
  CPPUNIT_ASSERT(result.more_False == expected.more_False)
  CPPUNIT_ASSERT(result.less_False == expected.less_False)
  CPPUNIT_ASSERT(result.less_True == expected.less_True)





