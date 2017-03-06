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

#include "net_plumber_plumbing_unit.h"
#include "../net_plumber_utils.h"
#include <sstream>

using namespace net_plumber;
using namespace std;
using namespace log4cxx;

LoggerPtr NetPlumberPlumbingTest::logger(
    Logger::getLogger("NetPlumber-PlumbingUnitTest"));

void NetPlumberPlumbingTest::setUp() {
  N = new NetPlumber(1);
  N->add_link(2,4);
  N->add_link(4,2);
  N->add_link(3,6);
  N->add_link(6,3);
  N->add_link(5,8);
  N->add_link(8,5);
  N->add_link(7,9);
  N->add_link(9,7);
  N->add_table(1, make_sorted_list(3,1,2,3));
  N->add_table(2, make_sorted_list(3,4,5,11));
  N->add_table(3, make_sorted_list(2,6,12));
  N->add_table(4, make_sorted_list(2,8,13));
  node_ids.push_back(N->add_rule(1,-1,
              make_sorted_list(1,1),
              make_sorted_list(1,2),
              array_from_str ("1010xxxx"),
              NULL,
              NULL));
  node_ids.push_back(N->add_rule(1,-1,
              make_sorted_list(1,1),
              make_sorted_list(1,2),
              array_from_str ("10001xxx"),
              NULL,
              NULL));
  node_ids.push_back(N->add_rule(1,-1,
              make_sorted_list(2,1,2),
              make_sorted_list(1,3),
              array_from_str ("10xxxxxx"),
              NULL,
              NULL));
  node_ids.push_back(N->add_rule(2,-1,
              make_sorted_list(1,4),
              make_sorted_list(2,5,11),
              array_from_str ("1011xxxx"),
              array_from_str ("11100111"),
              array_from_str ("00001000")));
  node_ids.push_back(N->add_rule(2,-1,
              make_sorted_list(1,4),
              make_sorted_list(1,5),
              array_from_str ("10xxxxxx"),
              array_from_str ("10011111"),
              array_from_str ("01100000")));
  node_ids.push_back(N->add_rule(3,-1,
              make_sorted_list(2,6,12),
              make_sorted_list(1,7),
              array_from_str ("101xxxxx"),
              array_from_str ("11111000"),
              array_from_str ("00000111")));
  node_ids.push_back(N->add_rule(4,-1,
              make_sorted_list(1,8),
              make_sorted_list(1,13),
              array_from_str ("xxx010xx"),
              NULL,
              NULL));
  memset(&A,0,sizeof A);
}

void NetPlumberPlumbingTest::tearDown() {
  delete N;
}

void NetPlumberPlumbingTest::test_setup() {
  printf("\n");
  int stats[7][4]={
      {1,0,1,0},
      {1,0,1,0},
      {1,0,0,2},
      {1,0,1,0},
      {1,2,0,1},
      {0,1,0,0},
      {0,2,0,0}
  };
  //N->print_plumbing_network();
  this->verify_pipe_stats(stats);
}

void NetPlumberPlumbingTest::test_pipeline_add_rule() {
  printf("\n");
  node_ids.push_back(N->add_rule(1,0,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xx11xxxx"),
              NULL,
              NULL));
  int stats[8][4]={
      {1,0,1,0},
      {1,0,1,0},
      {1,0,0,3},
      {1,1,1,0},
      {1,3,0,1},
      {0,2,0,0},
      {0,2,0,0},
      {3,0,1,0} //new rule
  };
  //N->print_plumbing_network();
  this->verify_pipe_stats(stats);
}

void NetPlumberPlumbingTest::test_pipeline_remove_rule() {
  printf("\n");
  N->remove_rule(node_ids[4]);
  int stats[7][4]={
      {0,0,1,0},
      {0,0,1,0},
      {1,0,0,2},
      {1,0,0,0},
      {0,0,0,0},
      {0,1,0,0},
      {0,1,0,0}
  };
  //N->print_plumbing_network();
  this->verify_pipe_stats(stats);
}

void NetPlumberPlumbingTest::test_pipeline_add_group_rule() {
  printf("\n");
  node_ids.push_back(N->add_rule_to_group(1,1,
              make_sorted_list(1,1),
              make_sorted_list(1,2),
              array_from_str ("xxxx11xx"),
              array_from_str ("11001111"),
              array_from_str ("00000000"),0));
  node_ids.push_back(N->add_rule_to_group(1,0,
              make_sorted_list(1,1),
              make_sorted_list(1,3),
              array_from_str ("xxxx11xx"),
              NULL,
              NULL,node_ids[node_ids.size()-1]));
  int stats[9][4]={
      {1,0,2,0},
      {1,0,1,1},
      {1,0,0,3},
      {1,0,1,0},
      {1,3,0,1},
      {0,2,0,0},
      {0,2,0,0},
      {1,0,2,1}, //new rule 1
      {1,0,2,1}  //new rule 2
  };
  //N->print_plumbing_network();
  this->verify_pipe_stats(stats);
}

void NetPlumberPlumbingTest::test_pipeline_add_group_rule_mix() {
  printf("\n");
  this->test_pipeline_add_group_rule();
  node_ids.push_back(N->add_rule(1,2,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xx11xxxx"),
              NULL,
              NULL));
  int stats[10][4]={
      {1,0,2,0},
      {1,0,1,1},
      {1,0,0,4},
      {1,1,1,0},
      {1,4,0,1},
      {0,3,0,0},
      {0,2,0,0},
      {1,0,3,1}, //new rule 1
      {1,0,3,1}, //new rule 2
      {3,0,1,1}  //new rule 3
  };
  //N->print_plumbing_network();
  this->verify_pipe_stats(stats);
}

void NetPlumberPlumbingTest::test_pipeline_remove_group_rule() {
  printf("\n");
  this->test_pipeline_add_group_rule();
  N->remove_rule(node_ids[node_ids.size()-1]);
  node_ids.pop_back();
  node_ids.pop_back();
  this->test_setup();
}

void NetPlumberPlumbingTest::test_pipeline_add_link() {
  printf("\n");
  N->add_link(11,12);
  int stats[7][4]={
      {1,0,1,0},
      {1,0,1,0},
      {1,0,0,2},
      {2,0,1,0},
      {1,2,0,1},
      {0,2,0,0},
      {0,2,0,0}
  };
  //N->print_plumbing_network();
  this->verify_pipe_stats(stats);
}

void NetPlumberPlumbingTest::test_pipeline_remove_link() {
  this->test_pipeline_add_link();
  N->remove_link(11,12);
  //N->print_plumbing_network();
  this->test_setup();
}

void NetPlumberPlumbingTest::test_pipeline_add_source() {
  printf("\n");
  N->add_link(100,1);
  hs *h = hs_create(1);
  hs_add(h, array_from_str ("1xxxxxxx"));
  node_ids.push_back(
      N->add_source(h, make_sorted_list(1,100))
      );
  int stats[8][4]={
      {1,1,1,0},
      {1,1,1,0},
      {1,1,0,2},
      {1,0,1,0},
      {1,2,0,1},
      {0,1,0,0},
      {0,2,0,0},
      {3,0,0,0}
  };
  //N->print_plumbing_network();
  this->verify_pipe_stats(stats);
}

void NetPlumberPlumbingTest::test_pipeline_remove_source() {
  printf("\n");
  N->add_link(100,1);
  hs *h = hs_create(1);
  hs_add(h, array_from_str ("1xxxxxxx"));
  uint64_t id = N->add_source(h, make_sorted_list(1,100));
  //N->print_plumbing_network();
  N->remove_source(id);
  this->test_setup();
}

void NetPlumberPlumbingTest::test_pipeline_add_probe() {
  printf("\n");
  N->add_link(13,200);
  node_ids.push_back(N->add_source_probe(
      make_sorted_list(1,200), EXISTENTIAL, new TrueCondition(),
      new TrueCondition(),NULL, NULL));
  int stats[8][4]={
      {1,0,1,0},
      {1,0,1,0},
      {1,0,0,2},
      {1,0,1,0},
      {1,2,0,1},
      {0,1,0,0},
      {1,2,0,0},
      {0,1,0,0},
  };
  //N->print_plumbing_network();
  this->verify_pipe_stats(stats);
}

void NetPlumberPlumbingTest::test_pipeline_remove_probe() {
  this->test_pipeline_add_probe();
  N->remove_source_probe(node_ids[7]);
  node_ids.pop_back();
  //N->print_plumbing_network();
  this->test_setup();
}

void NetPlumberPlumbingTest::test_pipeline_shared_ports() {
  printf("\n");
  N->add_table(5,make_sorted_list(3,14,15,16));
  N->add_link(11,14);
  N->add_link(15,8);
  node_ids.push_back(N->add_rule(5,-1,
              make_sorted_list(0),
              make_sorted_list(1,15),
              array_from_str ("10xxxxxx"),
              array_from_str ("10011111"),
              array_from_str ("01100000")));
  node_ids.push_back(N->add_rule(5,-1,
              make_sorted_list(0),
              make_sorted_list(1,16),
              array_from_str ("1000xxxx"),
              NULL,
              NULL));
  node_ids.push_back(N->add_rule(5,-1,
              make_sorted_list(0),
              make_sorted_list(1,15),
              array_from_str ("1010xxxx"),
              array_from_str ("10011111"),
              array_from_str ("01000000")));
  int stats[10][4]={
      {1,0,1,0},
      {1,0,1,0},
      {1,0,0,2},
      {3,0,1,0},
      {1,2,0,1},
      {0,1,0,0},
      {0,4,0,0},
      {1,1,2,0},
      {0,0,0,1},
      {1,1,0,1}
  };
  //N->print_plumbing_network();
  this->verify_pipe_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_add_source() {
  printf("\n");
  N->add_link(100,1);
  hs *h = hs_create(1);
  hs_add(h, array_from_str ("1xxxxxxx"));
  N->add_source(h, make_sorted_list(1,100));
  int stats[7][2] = {
      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_remove_source() {
  printf("\n");
  N->add_link(100,1);
  hs *h = hs_create(1);
  hs_add(h, array_from_str ("1xxxxxxx"));
  uint64_t id1 = N->add_source(h, make_sorted_list(1,100));
  h = hs_create(1);
  hs_add(h, array_from_str ("xxxxxxxx"));
  uint64_t id2 = N->add_source(h, make_sorted_list(1,100));
  //N->print_plumbing_network();
  N->remove_source(id2);
  int stats[7][2] = {
      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_add_fwd_rule_lower_priority() {
  printf("\n");
  this->test_routing_add_source();
  node_ids.push_back(N->add_rule(1,-1,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xxx11xxx"),
              NULL,
              NULL));
  int stats[8][2] = {
      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0},
      {1,0},
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_add_rw_rule_lower_priority() {
  printf("\n");
  this->test_routing_add_source();
  node_ids.push_back(N->add_rule(1,-1,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xxx11xxx"),
              array_from_str ("10111111"),
              array_from_str ("00000000")));
  int stats[8][2] = {
      {1,0},
      {1,0},
      {1,2},
      {1,0},
      {3,0},
      {2,0},
      {3,0},
      {1,0},
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_add_fwd_rule_higher_priority() {
  printf("\n");
  this->test_routing_add_source();
  node_ids.push_back(N->add_rule(1,0,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xxxx11xx"),
              NULL,
              NULL));
  int stats[8][2] = {
      {1,1},
      {1,0},
      {1,3},
      {1,0},
      {3,1},
      {2,0},
      {2,0},
      {1,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_add_rw_rule_higher_priority() {
  printf("\n");
  this->test_routing_add_source();
  node_ids.push_back(N->add_rule(2,0,
              make_sorted_list(1,4),
              make_sorted_list(1,5),
              array_from_str ("10xx1xxx"),
              array_from_str ("00111111"),
              array_from_str ("01000000")
              ));
  int stats[8][2] = {
      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {1,0},
      {1,0},
      {2,0},
      {2,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_add_rw_rule_higher_priority2() {
  printf("\n");
  this->test_routing_add_source();
  node_ids.push_back(N->add_rule(3,0,
              make_sorted_list(1,6),
              make_sorted_list(1,5),
              array_from_str ("1xxxxxxx"),
              array_from_str ("11011111"),
              array_from_str ("00000000")
              ));
  int stats[8][2] = {
      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {0,0},
      {2,0},
      {1,1}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_add_group_rule_mid_priority() {
  printf("\n");
  this->test_routing_add_source();
  node_ids.push_back(N->add_rule_to_group(1,1,
              make_sorted_list(1,1),
              make_sorted_list(1,2),
              array_from_str ("xxxx11xx"),
              array_from_str ("11100111"),
              array_from_str ("00000000"),0));
  node_ids.push_back(N->add_rule_to_group(1,0,
              make_sorted_list(1,1),
              make_sorted_list(1,3),
              array_from_str ("xxxx11xx"),
              NULL,
              NULL,node_ids[node_ids.size()-1]));
  int stats[9][2] = {
      {1,0},
      {1,0},
      {1,3},
      {0,0},
      {3,0},
      {2,0},
      {2,0},
      {1,0}, // new rule 1
      {1,1}  // new rule 2
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_add_rule_block_bounce() {
  printf("\n");
  this->test_routing_add_source();
  node_ids.push_back(N->add_rule(1,0,
              make_sorted_list(3,1,2,3),
              make_sorted_list(2,2,3),
              array_from_str ("xxxx11xx"),
              NULL,
              NULL));
  node_ids.push_back(N->add_rule(3,0,
              make_sorted_list(1,6),
              make_sorted_list(1,6),
              array_from_str ("100x11xx"),
              NULL,
              NULL));
  int stats[9][2] = {
      {1,1},
      {1,0},
      {1,3},
      {1,0},
      {3,1},
      {2,0},
      {2,0},
      {1,0},
      {1,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_remove_group_rule_mid_priority() {
  this->test_routing_add_group_rule_mid_priority();
  N->remove_rule(node_ids[node_ids.size()-1]);
  node_ids.pop_back();
  node_ids.pop_back();
  int stats[7][2] = {
      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_remove_fwd_rule_lower_priority() {
  printf("\n");
  this->test_routing_add_source();
  N->remove_rule(node_ids[2]);
  std::vector<uint64_t>::iterator it = node_ids.begin();
  advance(it,2);
  node_ids.erase(it);
  int stats[6][2] = {
      {1,0},
      {1,0},
      {0,0},
      {2,0},
      {0,0},
      {2,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_remove_rw_rule_lower_priority() {
  printf("\n");
  this->test_routing_add_source();
  N->remove_rule(node_ids[4]);
  std::vector<uint64_t>::iterator it = node_ids.begin();
  advance(it,4);
  node_ids.erase(it);
  int stats[6][2] = {
      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {1,0},
      {0,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_remove_fwd_rule_higher_priority() {
  this->test_routing_add_fwd_rule_higher_priority();
  N->remove_rule(node_ids.back());
  node_ids.pop_back();
  int stats[7][2] = {
      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_remove_rw_rule_higher_priority() {
  this->test_routing_add_rw_rule_higher_priority();
  N->remove_rule(node_ids.back());
  node_ids.pop_back();
  int stats[7][2] = {
      {1,0},
      {1,0},
      {1,2},
      {0,0},
      {2,0},
      {1,0},
      {2,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_add_link() {
  this->test_routing_add_fwd_rule_higher_priority();
  node_ids.push_back(N->add_rule(3,0,
              make_sorted_list(1,12),
              make_sorted_list(1,7),
              array_from_str ("10xxxxx1"),
              array_from_str ("00011000"),
              array_from_str ("00000000")));
  N->add_link(11,12);
  N->add_link(7,8);
  int stats[9][2] = {
      {1,1},
      {1,0},
      {1,3},
      {1,0},
      {3,1},
      {3,0},
      {3,0},
      {1,0},
      {1,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats);
}

void NetPlumberPlumbingTest::test_routing_remove_link() {
  this->test_routing_add_link();

  N->remove_link(7,8);
  int stats1[9][2] = {
      {1,1},
      {1,0},
      {1,3},
      {1,0},
      {3,1},
      {3,0},
      {2,0},
      {1,0},
      {1,0}
  };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats1);
  N->remove_link(11,12);
  int stats2[9][2] = {
        {1,1},
        {1,0},
        {1,3},
        {1,0},
        {3,1},
        {2,0},
        {2,0},
        {1,0},
        {0,0}
    };
  //N->print_plumbing_network();
  this->verify_source_flow_stats(stats2);
}

void loop_detected(NetPlumber *N, Flow *f, void* data) {
  bool *is_looped = (bool *)(data);
  *is_looped = true;
  return;
  uint32_t table_ids[4] = {1,3,2,1};
  for (int i=0; i < 4; i++) {
    RuleNode *r = (RuleNode*)f->node;
    CPPUNIT_ASSERT(r->table == table_ids[i]);
    f = *f->p_flow;
  }
}

void NetPlumberPlumbingTest::test_detect_loop() {
  printf("\n");
  bool is_looped;
  N->loop_callback = loop_detected;
  N->loop_callback_data = &is_looped;
  this->test_routing_add_fwd_rule_higher_priority();
  N->add_link(11,12);
  N->add_link(14,15);
  node_ids.push_back(N->add_rule(3,0,
              make_sorted_list(1,12),
              make_sorted_list(1,14),
              array_from_str ("10xxxxx1"),
              NULL,
              NULL));
  node_ids.push_back(N->add_rule(1,0,
              make_sorted_list(1,15),
              make_sorted_list(1,2),
              array_from_str ("10xxxxxx"),
              NULL,
              NULL));
  //N->print_plumbing_network();
  CPPUNIT_ASSERT(is_looped);
}

void probe_fire_counter(void *caller, SourceProbeNode *p, Flow *f,
                   void *data, PROBE_TRANSITION t) {
  probe_counter_t *a = (probe_counter_t*)data;
  switch (t) {
    case(STARTED_FALSE): (*a).start_false++; break;
    case(STARTED_TRUE): (*a).start_true++; break;
    case(TRUE_TO_FALSE): (*a).true_to_false++; break;
    case(FALSE_TO_TRUE): (*a).false_to_true++; break;
    case(MORE_FALSE): (*a).more_false++; break;
    case(LESS_FALSE): (*a).less_false++; break;
    case(MORE_TRUE): (*a).more_true++; break;
    case(LESS_TRUE): (*a).less_true++; break;
    default: break;
  }
}

void NetPlumberPlumbingTest::test_false_probe() {
  this->test_routing_add_source();
  N->add_link(13,200);
  probe_counter_t a = {0};
  probe_counter_t r = {0,3,0,0,0,0,0,0};
  node_ids.push_back(N->add_source_probe(
       make_sorted_list(1,200), EXISTENTIAL, new TrueCondition(),
       new FalseCondition(), probe_fire_counter, &a));
  node_ids.push_back(N->add_source_probe(
       make_sorted_list(1,200), UNIVERSAL, new TrueCondition(),
       new FalseCondition(), probe_fire_counter, &a));
  this->check_probe_counter(a,r);
  //N->print_plumbing_network();
}

void NetPlumberPlumbingTest::test_true_probe() {
  this->test_routing_add_source();
  N->add_link(13,200);
  probe_counter_t a = {0};
  probe_counter_t r = {3,0,0,0,0,0,0,0};
  node_ids.push_back(N->add_source_probe(
       make_sorted_list(1,200), EXISTENTIAL, new TrueCondition(),
       new TrueCondition(), probe_fire_counter, &a));
  node_ids.push_back(N->add_source_probe(
       make_sorted_list(1,200), UNIVERSAL, new TrueCondition(),
       new TrueCondition(), probe_fire_counter, &a));
  this->check_probe_counter(a,r);
}

void NetPlumberPlumbingTest::test_port_probe() {
  this->test_routing_add_source();
  N->add_link(13,200);
  probe_counter_t a = {0};
  probe_counter_t r = {1,0,0,0,0,0,0,0};
  PathCondition *c = new PathCondition();
  c->add_pathlet(new PortSpecifier(4));
  N->add_source_probe(
         make_sorted_list(1,200), UNIVERSAL, new TrueCondition(),
         c, probe_fire_counter, &a);
  this->check_probe_counter(a,r);
}

void NetPlumberPlumbingTest::test_table_probe() {
  this->test_routing_add_source();
  N->add_link(13,200);
  probe_counter_t a = {0};
  probe_counter_t r = {2,0,0,0,0,0,0,0};
  PathCondition *c = new PathCondition();
  c->add_pathlet(new TableSpecifier(2));
  PathCondition *f = new PathCondition();
  c->add_pathlet(new LastPortsSpecifier(make_sorted_list(1,1)));
  N->add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, f,
         c, probe_fire_counter, &a);
  this->check_probe_counter(a,r);
}

void NetPlumberPlumbingTest::test_reachability() {
  this->test_routing_add_source();
  N->add_link(13,200);
  probe_counter_t a = {0};
  probe_counter_t r = {2,0,0,0,0,0,0,0};
  PathCondition *c = new PathCondition();
  c->add_pathlet(new LastPortsSpecifier(make_sorted_list(1,1)));
  N->add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, new TrueCondition(),
         c, probe_fire_counter, &a);
  this->check_probe_counter(a,r);
}

void NetPlumberPlumbingTest::test_probe_transition_no_update_add_rule() {
  this->test_routing_add_source();
  N->add_link(13,200);
  memset(&A,0,sizeof A);
  probe_counter_t r = {2,0,0,0,0,0,0,0};
  PathCondition *c = new PathCondition();
  c->add_pathlet(new LastPortsSpecifier(make_sorted_list(1,1)));
  N->add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, new TrueCondition(),
         c, probe_fire_counter, &A);
  node_ids.push_back(N->add_rule(1,-1,
              make_sorted_list(1,1),
              make_sorted_list(2,2,3),
              array_from_str ("xxx11xxx"),
              NULL,
              NULL));
  //N->print_plumbing_network();
  this->check_probe_counter(A,r);
}

void NetPlumberPlumbingTest::test_probe_transition_no_update_remove_rule() {
  this->test_probe_transition_no_update_add_rule();
  memset(&A,0,sizeof A);
  probe_counter_t r = {0,0,0,0,0,0,0,0};
  N->remove_rule(node_ids[node_ids.size()-1]);
  this->check_probe_counter(A,r);
}

void NetPlumberPlumbingTest::test_probe_transition_with_update_add_rule1() {
  this->test_routing_add_source();
  N->add_link(13,200);
  memset(&A,0,sizeof A);
  probe_counter_t r = {2,0,0,0,1,0,0,0};
  PathCondition *c = new PathCondition();
  c->add_pathlet(new LastPortsSpecifier(make_sorted_list(1,1)));
  N->add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, new TrueCondition(),
         c, probe_fire_counter, &A);
  node_ids.push_back(N->add_rule(3,0,
              make_sorted_list(1,6),
              make_sorted_list(1,5),
              array_from_str ("1xxxxxxx"),
              array_from_str ("11100111"),
              array_from_str ("00001000")
              ));
  //N->print_plumbing_network();
  this->check_probe_counter(A,r);
}

void NetPlumberPlumbingTest::test_probe_transition_with_update_add_rule2() {
  this->test_routing_add_source();
  N->add_link(13,200);
  memset(&A,0,sizeof A);
  probe_counter_t r = {2,0,1,0,0,0,0,1};
  PathCondition *c = new PathCondition();
  c->add_pathlet(new LastPortsSpecifier(make_sorted_list(1,1)));
  N->add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, new TrueCondition(),
         c, probe_fire_counter, &A);
  node_ids.push_back(N->add_rule(1,0,
              make_sorted_list(1,1),
              make_sorted_list(1,50),
              array_from_str ("10xxxxxx"),
              NULL,
              NULL));
  //N->print_plumbing_network();
  this->check_probe_counter(A,r);
}

void NetPlumberPlumbingTest::test_probe_transition_with_update_remove_rule() {
  this->test_probe_transition_with_update_add_rule2();
  memset(&A,0,sizeof A);
  N->remove_rule(node_ids[node_ids.size()-1]);
  probe_counter_t r = {0,0,0,1,1,0,0,0};
  this->check_probe_counter(A,r);
}

void NetPlumberPlumbingTest::test_probe_transition_add_link() {
  printf("\n");
  N->add_link(13,200);
  memset(&A,0,sizeof A);
  probe_counter_t r = {0,1,0,1,0,0,0,0};
  PathCondition *c = new PathCondition();
  c->add_pathlet(new TableSpecifier(3));
  N->add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, new TrueCondition(),
         c, probe_fire_counter, &A);
  this->test_routing_add_link();
  //N->print_plumbing_network();
  this->check_probe_counter(A,r);
}

void NetPlumberPlumbingTest::test_probe_transition_remove_link() {
  printf("\n");
  N->add_link(13,200);
  memset(&A,0,sizeof A);
  probe_counter_t r = {0,1,1,1,0,0,0,0};
  PathCondition *c = new PathCondition();
  c->add_pathlet(new TableSpecifier(3));
  N->add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, new TrueCondition(),
         c, probe_fire_counter, &A);
  this->test_routing_remove_link();
  //N->print_plumbing_network();
  this->check_probe_counter(A,r);
}

void NetPlumberPlumbingTest::test_probe_transition_add_source() {
  printf("\n");
  this->test_routing_add_source();
  N->add_link(13,200);
  N->add_link(300,4);
  memset(&A,0,sizeof A);
  probe_counter_t r = {0,1,0,1,1,0,0,0};
  PathCondition *c = new PathCondition();
  c->add_pathlet(new LastPortsSpecifier(make_sorted_list(1,4)));
  N->add_source_probe(
         make_sorted_list(1,200), EXISTENTIAL, new TrueCondition(),
         c, probe_fire_counter, &A);
  hs *h = hs_create(1);
  hs_add(h, array_from_str ("xxxxxxxx"));
  node_ids.push_back(
      N->add_source(h, make_sorted_list(1,300))
      );

  //N->print_plumbing_network();
  this->check_probe_counter(A,r);
}

void NetPlumberPlumbingTest::test_probe_transition_remove_source() {
  printf("\n");
  this->test_probe_transition_add_source();
  memset(&A,0,sizeof A);
  probe_counter_t r = {0,0,1,0,0,0,0,1};
  N->remove_source(node_ids[node_ids.size()-1]);
  //N->print_plumbing_network();
  this->check_probe_counter(A,r);
}

/* * * * * * * * * * *
 * Testing FUnctions *
 * * * * * * * * * * *
 */

void NetPlumberPlumbingTest::verify_pipe_stats(int stats[][4]) {
  for (unsigned i = 0; i < node_ids.size(); i++) {
      int fwd_pipeline;
      int bck_pipeline;
      int influence_on;
      int influenced_by;
      N->get_pipe_stats(node_ids[i],fwd_pipeline,bck_pipeline,
          influence_on,influenced_by);
      stringstream error_msg;
      error_msg << "(fwd, bck, inf_on, inf_by) - Obtained: " << fwd_pipeline <<
          " , " << bck_pipeline << " , " << influence_on << " , " <<
          influenced_by << " Expected " << stats[i][0] << " , " << stats[i][1]
          << " , " << stats[i][2] << " , " << stats[i][3];
      LOG4CXX_DEBUG(logger,error_msg.str());
      CPPUNIT_ASSERT(fwd_pipeline == stats[i][0]);
      CPPUNIT_ASSERT(bck_pipeline == stats[i][1]);
      CPPUNIT_ASSERT(influence_on == stats[i][2]);
      CPPUNIT_ASSERT(influenced_by == stats[i][3]);
  }
}

void NetPlumberPlumbingTest::verify_source_flow_stats(int stats[][2]) {
  for (unsigned i = 0; i < node_ids.size(); i++) {
    int inc, exc;
    N->get_source_flow_stats(node_ids[i], inc, exc);
    stringstream error_msg;
    error_msg << "(included wc, excluded_wc) - Obtained: " << inc <<
        " , " << exc << " Expected " << stats[i][0] << " , " << stats[i][1];
    LOG4CXX_DEBUG(logger,error_msg.str());
    CPPUNIT_ASSERT(inc == stats[i][0]);
    CPPUNIT_ASSERT(exc == stats[i][1]);
  }
}

void NetPlumberPlumbingTest::check_probe_counter(
    probe_counter_t result, probe_counter_t expected) {
  CPPUNIT_ASSERT(result.start_true == expected.start_true);
  CPPUNIT_ASSERT(result.start_false == expected.start_false);
  CPPUNIT_ASSERT(result.true_to_false == expected.true_to_false);
  CPPUNIT_ASSERT(result.false_to_true == expected.false_to_true);
  CPPUNIT_ASSERT(result.more_true == expected.more_true);
  CPPUNIT_ASSERT(result.more_false == expected.more_false);
  CPPUNIT_ASSERT(result.less_false == expected.less_false);
  CPPUNIT_ASSERT(result.less_true == expected.less_true);
}




