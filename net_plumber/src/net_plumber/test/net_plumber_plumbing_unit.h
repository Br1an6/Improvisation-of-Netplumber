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


#ifndef NET_PLUMBER_PLUMBING_UNIT_H_
#define NET_PLUMBER_PLUMBING_UNIT_H_

#include "cppunit/TestCase.h"
#include "cppunit/TestFixture.h"
#include <cppunit/extensions/HelperMacros.h>
#include "../net_plumber.h"
#include <vector>

struct probe_counter_t {
  int start_true;
  int start_false;
  int true_to_false;
  int false_to_true;
  int more_true;
  int more_false;
  int less_false;
  int less_true;
};

class NetPlumberPlumbingTest : public CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(NetPlumberPlumbingTest);

  CPPUNIT_TEST(test_setup);
  CPPUNIT_TEST(test_pipeline_add_rule);
  CPPUNIT_TEST(test_pipeline_remove_rule);
  CPPUNIT_TEST(test_pipeline_add_group_rule);
  CPPUNIT_TEST(test_pipeline_add_group_rule_mix);
  CPPUNIT_TEST(test_pipeline_remove_group_rule);
  CPPUNIT_TEST(test_pipeline_add_link);
  CPPUNIT_TEST(test_pipeline_remove_link);
  CPPUNIT_TEST(test_pipeline_add_source);
  CPPUNIT_TEST(test_pipeline_remove_source);
  CPPUNIT_TEST(test_pipeline_add_probe);
  CPPUNIT_TEST(test_pipeline_remove_probe);
  CPPUNIT_TEST(test_pipeline_shared_ports);
  CPPUNIT_TEST(test_routing_add_source);
  CPPUNIT_TEST(test_routing_remove_source);
  CPPUNIT_TEST(test_routing_add_fwd_rule_lower_priority);
  CPPUNIT_TEST(test_routing_add_rw_rule_lower_priority);
  CPPUNIT_TEST(test_routing_add_fwd_rule_higher_priority);
  CPPUNIT_TEST(test_routing_add_rw_rule_higher_priority);
  CPPUNIT_TEST(test_routing_add_rw_rule_higher_priority2);
  CPPUNIT_TEST(test_routing_add_group_rule_mid_priority);
  CPPUNIT_TEST(test_routing_add_rule_block_bounce);
  CPPUNIT_TEST(test_routing_remove_fwd_rule_lower_priority);
  CPPUNIT_TEST(test_routing_remove_rw_rule_lower_priority);
  CPPUNIT_TEST(test_routing_remove_fwd_rule_higher_priority);
  CPPUNIT_TEST(test_routing_remove_rw_rule_higher_priority);
  CPPUNIT_TEST(test_routing_remove_group_rule_mid_priority);
  CPPUNIT_TEST(test_routing_add_link);
  CPPUNIT_TEST(test_routing_remove_link);
  CPPUNIT_TEST(test_detect_loop);
  CPPUNIT_TEST(test_false_probe);
  CPPUNIT_TEST(test_true_probe);
  CPPUNIT_TEST(test_port_probe);
  CPPUNIT_TEST(test_table_probe);
  CPPUNIT_TEST(test_reachability);
  CPPUNIT_TEST(test_probe_transition_no_update_add_rule);
  CPPUNIT_TEST(test_probe_transition_no_update_remove_rule);
  CPPUNIT_TEST(test_probe_transition_with_update_add_rule1);
  CPPUNIT_TEST(test_probe_transition_with_update_add_rule2);
  CPPUNIT_TEST(test_probe_transition_with_update_remove_rule);
  CPPUNIT_TEST(test_probe_transition_add_link);
  CPPUNIT_TEST(test_probe_transition_remove_link);
  CPPUNIT_TEST(test_probe_transition_add_source);
  CPPUNIT_TEST(test_probe_transition_remove_source);
  CPPUNIT_TEST_SUITE_END();

 public:
  void setUp();
  void tearDown();
  void test_setup();
  // Test correctness of pipeline construction
  void test_pipeline_add_rule();
  void test_pipeline_remove_rule();
  void test_pipeline_add_group_rule();
  void test_pipeline_add_group_rule_mix();
  void test_pipeline_remove_group_rule();
  void test_pipeline_add_link();
  void test_pipeline_remove_link();
  void test_pipeline_add_source();
  void test_pipeline_remove_source();
  void test_pipeline_add_probe();
  void test_pipeline_remove_probe();
  void test_pipeline_shared_ports();
  // Test correctness of flow routing
  void test_routing_add_source();
  void test_routing_remove_source();
  void test_routing_add_fwd_rule_lower_priority();
  void test_routing_add_rw_rule_lower_priority();
  void test_routing_add_fwd_rule_higher_priority();
  void test_routing_add_rw_rule_higher_priority();
  void test_routing_add_rw_rule_higher_priority2();
  void test_routing_add_group_rule_mid_priority();
  void test_routing_add_rule_block_bounce();
  void test_routing_remove_fwd_rule_lower_priority();
  void test_routing_remove_rw_rule_lower_priority();
  void test_routing_remove_fwd_rule_higher_priority();
  void test_routing_remove_rw_rule_higher_priority();
  void test_routing_remove_group_rule_mid_priority();
  void test_routing_add_link();
  void test_routing_remove_link();
  // test correctness of detecting errors
  void test_detect_loop();
  void test_false_probe();
  void test_true_probe();
  void test_port_probe();
  void test_table_probe();
  void test_reachability();
  void test_probe_transition_no_update_add_rule();
  void test_probe_transition_no_update_remove_rule();
  void test_probe_transition_with_update_add_rule1();
  void test_probe_transition_with_update_add_rule2();
  void test_probe_transition_with_update_remove_rule();
  void test_probe_transition_add_link();
  void test_probe_transition_remove_link();
  void test_probe_transition_add_source();
  void test_probe_transition_remove_source();


 private:
  static log4cxx::LoggerPtr logger;
  net_plumber::NetPlumber *N;
  probe_counter_t A;
  std::vector<uint64_t> node_ids;
  void verify_pipe_stats(int stats[][4]);
  void verify_source_flow_stats(int stats[][2]);
  void check_probe_counter(probe_counter_t result, probe_counter_t expected);
};




#endif  // NET_PLUMBER_PLUMBING_UNIT_H_
