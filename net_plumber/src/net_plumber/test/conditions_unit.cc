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


#include "conditions_unit.h"
#include "../net_plumber_utils.h"
#include "../source_node.h"
#include "../rule_node.h"
#include <stdarg.h>

using namespace std;

void ConditionsTest::test_port() {
  printf("\n");
  list<Flow*>* flows = create_flow(make_unsorted_list(3,1,2,3),
                                  make_unsorted_list(3,100,200,300));
  PathCondition c;
  c.add_pathlet(new PortSpecifier(2));
  CPPUNIT_ASSERT(c.check(*(flows->begin())));
  c.add_pathlet(new PortSpecifier(1));
  c.add_pathlet(new EndPathSpecifier());
  CPPUNIT_ASSERT(c.check(*(flows->begin())));
  free_flow(flows);
}

void ConditionsTest::test_table() {
  printf("\n");
  list<Flow*>* flows = create_flow(make_unsorted_list(3,1,2,3),
                                  make_unsorted_list(3,100,200,300));
  PathCondition c;
  c.add_pathlet(new TableSpecifier(300));
  CPPUNIT_ASSERT(c.check(*(flows->begin())));
  c.add_pathlet(new TableSpecifier(200));
  c.add_pathlet(new EndPathSpecifier());
  CPPUNIT_ASSERT(!c.check(*(flows->begin())));
  free_flow(flows);
}

void ConditionsTest::test_port_sequence() {
  printf("\n");
  list<Flow*>* flows = create_flow(make_unsorted_list(5,1,2,3,4,5),
                                  make_unsorted_list(5,100,200,300,400,500));
  PathCondition c;
  c.add_pathlet(new PortSpecifier(4));
  c.add_pathlet(new NextPortsSpecifier(make_sorted_list(1,3)));
  CPPUNIT_ASSERT(c.check(*(flows->begin())));
  c.add_pathlet(new NextPortsSpecifier(make_sorted_list(1,1)));
  CPPUNIT_ASSERT(!c.check(*(flows->begin())));
  //printf("%s\n",c.to_string().c_str());
  free_flow(flows);
}

void ConditionsTest::test_sequence() {
  printf("\n");
  list<Flow*>* flows = create_flow(make_unsorted_list(5,1,2,3,4,5),
                                  make_unsorted_list(5,100,200,300,400,500));
  PathCondition c;
  c.add_pathlet(new PortSpecifier(4));
  c.add_pathlet(new NextTablesSpecifier(make_sorted_list(1,300)));
  CPPUNIT_ASSERT(c.check(*(flows->begin())));
  c.add_pathlet(new SkipNextSpecifier());
  c.add_pathlet(new NextTablesSpecifier(make_sorted_list(1,100)));
  CPPUNIT_ASSERT(c.check(*(flows->begin())));
  free_flow(flows);
}

void ConditionsTest::test_path_length() {
  printf("\n");
  list<Flow*>* flows1 = create_flow(make_unsorted_list(4,1,2,3,4),
                                  make_unsorted_list(4,100,200,300,400));
  list<Flow*>* flows2 = create_flow(make_unsorted_list(2,1,2),
                                  make_unsorted_list(2,100,200));
  // path of length 1
  PathCondition *c1 = new PathCondition();
  c1->add_pathlet(new SkipNextSpecifier());
  c1->add_pathlet(new EndPathSpecifier());
  // path of length 2
  PathCondition *c2 = new PathCondition();
  c2->add_pathlet(new SkipNextSpecifier());
  c2->add_pathlet(new SkipNextSpecifier());
  c2->add_pathlet(new EndPathSpecifier());
  // path of length 3
  PathCondition *c3 = new PathCondition();
  c3->add_pathlet(new SkipNextSpecifier());
  c3->add_pathlet(new SkipNextSpecifier());
  c3->add_pathlet(new SkipNextSpecifier());
  c3->add_pathlet(new EndPathSpecifier());
  // OR the three cases
  OrCondition *oc1 = new OrCondition(c1,c2);
  OrCondition c(oc1,c3);
  // flow 1 has length of 4 and doesn't pass
  CPPUNIT_ASSERT(!c.check(*(flows1->begin())));
  // flow 2 has length of 2 and does pass
  CPPUNIT_ASSERT(c.check(*(flows2->begin())));
  //printf("%s\n",c.to_string().c_str());
  free_flow(flows1);
  free_flow(flows2);
}

void ConditionsTest::test_lasts() {
  printf("\n");
  list<Flow*>* flows1 = create_flow(make_unsorted_list(4,10,2,3,4),
                                  make_unsorted_list(4,100,200,300,400));
  list<Flow*>* flows2 = create_flow(make_unsorted_list(4,11,2,3,4),
                                  make_unsorted_list(4,101,200,300,400));
  PathCondition c1;
  c1.add_pathlet(new LastPortsSpecifier(make_sorted_list(2,10,11)));
  PathCondition c2;
  c2.add_pathlet(new LastTablesSpecifier(make_sorted_list(2,100,101)));
  CPPUNIT_ASSERT(c1.check(*(flows1->begin())));
  CPPUNIT_ASSERT(c1.check(*(flows2->begin())));
  CPPUNIT_ASSERT(c2.check(*(flows1->begin())));
  CPPUNIT_ASSERT(c2.check(*(flows2->begin())));
  free_flow(flows1);
  free_flow(flows2);
}

void ConditionsTest::test_header() {
  printf("\n");
  list<Flow*>* flows = create_flow(make_unsorted_list(5,1,2,3,4,5),
                                  make_unsorted_list(5,100,200,300,400,500));
  Flow *f = *(flows->begin());
  f->processed_hs = hs_create(1);
  hs_add(f->processed_hs, array_from_str("10xxxxxx"));
  array_t *d = array_from_str("1011xxxx");
  hs_diff(f->processed_hs,d);
  free(d);

  hs *hc1_hs = hs_create(1);
  hs_add(hc1_hs, array_from_str("100xxxxx"));

  hs *hc2_hs = hs_create(1);
  hs_add(hc2_hs, array_from_str("10111xxx"));

  HeaderCondition *hc1 = new HeaderCondition(hc1_hs);
  HeaderCondition *hc2 = new HeaderCondition(hc2_hs);

  CPPUNIT_ASSERT(hc1->check(f));
  CPPUNIT_ASSERT(!hc2->check(f));

  delete hc1;
  delete hc2;
  hs_free(f->processed_hs);
  free_flow(flows);
}

list<Flow*>* ConditionsTest::create_flow(List_t ports, List_t tables) {
  list<Flow*> *result = new list<Flow*>();
  Flow *f, *prev;
  SourceNode *s = new SourceNode(NULL,1,0,hs_create(1),make_sorted_list(1,0));
  prev = (Flow *)malloc(sizeof *prev);
  prev->node = s;
  prev->in_port = 0;
  prev->p_flow = s->get_EOSFI();
  result->push_front(prev);
  for (uint32_t i = 0; i< ports.size; i++) {
    RuleNode *r = new RuleNode(NULL, 1, 0, tables.list[i],
                           make_sorted_list(1,ports.list[i]),
                           make_sorted_list(1,ports.list[i]),
                           array_create(1,BIT_X),
                           NULL,
                           NULL);
    r->is_input_layer = true;
    r->is_output_layer = true;
    f = (Flow *)malloc(sizeof *f);
    f->in_port = ports.list[i];
    f->node = r;
    f->p_flow = result->begin();
    result->push_front(f);
  }
  free(ports.list);
  free(tables.list);
  return result;
}

void ConditionsTest::free_flow(list<Flow*>* flows) {
  list<Flow *>::iterator it;
  for (it = flows->begin(); it != flows->end(); it++) {
    delete (*it)->node;
    free(*it);
  }
  delete flows;
}
