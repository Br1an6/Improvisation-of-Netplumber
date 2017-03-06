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

#ifndef SRC_NET_PLUMBER_TEST_CONDITIONS_UNIT_H_
#define SRC_NET_PLUMBER_TEST_CONDITIONS_UNIT_H_

#include "cppunit/TestCase.h"
#include "cppunit/TestFixture.h"
#include <cppunit/extensions/HelperMacros.h>
#include "../conditions.h"

class ConditionsTest : public CppUnit::TestFixture {
  CPPUNIT_TEST_SUITE(ConditionsTest);
  CPPUNIT_TEST(test_port);
  CPPUNIT_TEST(test_table);
  CPPUNIT_TEST(test_port_sequence);
  CPPUNIT_TEST(test_sequence);
  CPPUNIT_TEST(test_path_length);
  CPPUNIT_TEST(test_lasts);
  CPPUNIT_TEST(test_header);
  CPPUNIT_TEST_SUITE_END();

 public:
  void test_port();
  void test_table();
  void test_port_sequence();
  void test_sequence();
  void test_path_length();
  void test_lasts();
  void test_header();

  static std::list<Flow*>* create_flow(List_t ports, List_t tables);
  static void free_flow(std::list<Flow*>* flows);
};

#endif  // SRC_NET_PLUMBER_TEST_CONDITIONS_UNIT_H_
