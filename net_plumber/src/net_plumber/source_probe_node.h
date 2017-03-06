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

#ifndef SRC_NET_PLUMBER_SOURCE_PROBE_NODE_H_
#define SRC_NET_PLUMBER_SOURCE_PROBE_NODE_H_

#include "node.h"
#include "conditions.h"
#include <map>

/*
 * SourceProbeNode class provides a way to check conditions on source flows.
 * The probe can be instantiated in two modes: Existential and Universal.
 * The probe accepts a filter condition (@filter) and a testing condition
 * (@condition):
 * - Universal Probe: "FOR ALL flows matching @filter condition, the @test
 * condition holds.
 * - Existential Probe: "THERE EXIST a flow matching @filter condition for
 * which @test condition holds.
 *
 * Examples 1: All flows from port P1 to port P2 pass through middle box M:
 *  * Connect a SourceNode to port P1.
 *  * Connect a Universal SourceProbeNode to port P2.
 *  * Set @filter condition of probe to ".*(p=P1)$" (i.e. PathCondition with
 *  a PortSpecifier(P1) and an EndPathSpecifier())
 *  * Set @test condition of probe to ".*(t=M)" (i.e. PathCondition with a
 *  TableSpecifier(M))
 *
 *  Example 2: port P1 can communicate to port P2:
 *  * Connect a SourceNode to port P1
 *  * Connect an Existential SourceProbeNode to port P2.
 *  * Set @filter condition of probe to TrueCondition (always true)
 *  * Set @test condition of probe to ".*(p=P1)$" (i.e. a PathCondition with a
 *  PortSpecifier(P1) and an EndPathSpecifier())
 *
 *  Example 3: All traffic from edge ports to port P should pass through
 *  Middle box M1 or M2 and immediately followed by filter box F1 or F2.
 *  * Connect a SourceNode to every edge port in network.
 *  * Connect a Universal SourceProbeNode to port P.
 *  * Set @filter condition of probe to LastPortsSpecifier([set of edge ports])
 *  * Set @test condition of probe to
 *  "(.*(t=M1)(t=F1 | t = F2)) | (.*(t=M2)(t = F1 | t = F2))"
 *  (i.e. OrCondition of two path conditions below:
 *    PathCondition1: TableSpecifier(M1) --> NextTablesSpecifier([F1,F2])
 *    PathCondition2: TableSpecifier(M2) --> NextTablesSpecifier([F1,F2])
 *  )
 *
 * Example 4: All flows from edge ports to Port P are at most 3 hubs long.
 *  * Connect a SourceNode to every edge port in network.
 *  * Connect a Universal SourceProbeNode to port P.
 *  * Set @filter condition of probe to LastPortsSpecifier([set of edge ports])
 *  * Set @test condition of probe to the following:
 *  .$ | ..$ | ...$ (i.e. OrCondition of the following:
 *  PathCondition1: SkipNextSpecifier --> EndPathSpecifier
 *  PathCondition2: SkipNextSpecifier(2 times) --> EndPathSpecifier
 *  PathCondition3: SkipNextSpecifier(3 times) --> EndPathSpecifier
 */

enum PROBE_STATE {
  STOPPED = 0,
  STARTED,
  RUNNING,
};

enum PROBE_MODE {
  EXISTENTIAL,
  UNIVERSAL
};

enum PROBE_TRANSITION {
  UNKNOWN = 0,
  STARTED_TRUE,
  STARTED_FALSE,
  TRUE_TO_FALSE,
  FALSE_TO_TRUE,
  MORE_TRUE,   // in existential mode: more matching flow.
  MORE_FALSE,  // in universal mode: more violating flow.
  LESS_FALSE,  // in universal mode: less violating flow, but still false
  LESS_TRUE    // in existential mode: less matching flow, but still true
};

std::string probe_transition(PROBE_TRANSITION t);

class SourceProbeNode;

typedef void (*src_probe_callback_t)
    (void *caller, SourceProbeNode *p, Flow *f, void *data, PROBE_TRANSITION);

void default_probe_callback(void *caller, SourceProbeNode *p, Flow *f,
                            void *data, PROBE_TRANSITION t);
class SourceProbeNode : public Node {
 protected:
  PROBE_STATE state;
  PROBE_MODE mode;
  Condition *filter;
  Condition *test;
  std::map< Flow*, bool >check_results;
  int cond_count;

  /*
   * probe trigger callback
   */
  src_probe_callback_t probe_callback;
  void *probe_callback_data;

 public:
  SourceProbeNode(void *n, int length, uint64_t node_id,
                  PROBE_MODE mode, List_t ports,
                  Condition *filter, Condition *condition,
                  src_probe_callback_t probe_callback, void *callback_data);
  virtual ~SourceProbeNode();

  /*
   * source flow management functions
   */
  void process_src_flow_at_location(std::list<struct Flow*>::iterator loc,
      array_t* change);
  void process_src_flow(Flow *f);
  void absorb_src_flow(std::list<struct Flow*>::iterator s_flow, bool first);

  void update_check(Flow *f, short action);
  void start_probe();
  void stop_probe();

  /*
   * get_condition_count: for existential mode, returns number of flows meeting
   * the condition. for universal case, returns number of flows violating a
   * condition.
   */
  int get_condition_count() {return this->cond_count;}

  PROBE_MODE get_mode() {return this->mode;}

  std::list<Flow*>::iterator get_source_flow_iterator();
  std::string to_string();

};

#endif  // SRC_NET_PLUMBER_SOURCE_PROBE_NODE_H_
