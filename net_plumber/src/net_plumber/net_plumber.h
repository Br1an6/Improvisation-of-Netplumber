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

#ifndef SRC_NET_PLUMBER_H_
#define SRC_NET_PLUMBER_H_
#include <map>
#include <vector>
#include <list>
#include "rule_node.h"
#include "source_node.h"
#include "log4cxx/logger.h"
#include "source_probe_node.h"

enum EVENT_TYPE {
  None = 0,
  ADD_RULE,
  REMOVE_RULE,
  ADD_LINK,
  REMOVE_LINK,
  ADD_SOURCE,
  REMOVE_SOURCE,
  ADD_SINK,
  REMOVE_SINK,
  START_SOURCE_PROBE,
  STOP_SOURCE_PROBE,
  START_SINK_PROBE,
  STOP_SINK_PROBE,
  ADD_TABLE,
  REMOVE_TABLE
};

struct Event {
  EVENT_TYPE type;
  uint64_t id1;  //node id, table id or source port.
  uint64_t id2;  // destination port.
};

std::string get_event_name(EVENT_TYPE t);

namespace net_plumber {

  class NetPlumber;

  typedef void (*global_error_callback_t)(NetPlumber *N, Flow *f, void* data);

  class NetPlumber {
   private:
    static log4cxx::LoggerPtr logger;

    //length of header
    int length;

    // last event happened in the net plumber.
    Event last_event;

    //topology
    std::map< uint32_t, std::vector<uint32_t>* > topology;

    //inverse topology
    std::map< uint32_t, std::vector<uint32_t>* > inv_topology;

    // last id used for a table id
    std::map<uint32_t,uint64_t> table_to_last_id;

    //list of nodes for table id
    std::map<uint32_t,std::list<RuleNode*>* > table_to_nodes;

    //list of ports for table id
    std::map<uint32_t,List_t > table_to_ports;

    //node_id to node
    std::map<uint64_t,Node*> id_to_node;

    //list of rules for input port
    std::map<uint32_t, std::list<Node*>* > inport_to_nodes;

    //list of rules for output port
    std::map<uint32_t, std::list<Node*>* > outport_to_nodes;

    // last id used for a source/sink/probe node
    uint32_t last_ssp_id_used;

    // list of source and sink nodes:
    std::list<Node *> flow_nodes;

    // list of probe nodes
    std::list<Node *> probes;

    uint64_t _add_rule(uint32_t table,int index, bool group, uint64_t gid,
                       List_t in_ports, List_t out_ports,
                       array_t* match, array_t *mask, array_t* rw);

   public:
    //call back function in case of a loop
    global_error_callback_t loop_callback;
    void *loop_callback_data;
    global_error_callback_t blackhole_callback;
    void *blackhole_callback_data;

    /*
     * constructor.
     * @length: length of header (L)
     */
    NetPlumber(int length);
    int get_length() { return this->length; }

    /*
     * destructor
     */
    virtual ~NetPlumber();

    /*
     * return last event happened in the net plumber network
     */
    Event get_last_event();
    void set_last_event(Event e);

    /*
     * Topology Management
     * add_link: adds a link from @from_port to @to_port
     * remove_link: remove a previously created link and update plumber.
     * get_dst_ports: get the dst end of a link whose src port is @src_port
     * get_src_ports: get the src end of a link whose dst port is @dst_port
     * print_topology: prints current link connections.
     */
    void add_link(uint32_t from_port, uint32_t to_port);
    void remove_link(uint32_t from_port, uint32_t to_port);
    std::vector<uint32_t> *get_dst_ports(uint32_t src_port);
    std::vector<uint32_t> *get_src_ports(uint32_t dst_port);
    void print_topology();

    /*
     * Table Management:
     * add_table: create a new table with @id as ID. If table already exists,
     * does nothing. (NOTE: table id should > 0). @ports are the list of ports
     * belong to this table.
     * remove_table: removes a table if exist. (and all rules in it)
     * print_table: prints the table with @id.
     */
    void add_table(uint32_t id, List_t ports);
    void remove_table(uint32_t id);
    List_t get_table_ports(uint32_t id);
    void print_table(uint32_t id);

    /*
     * Rule Management:
     * - add_rule: adds a rule to @table. if @table does not exist, skip.
     * @table: table ID
     * @index: position in table (or -1) for last entry.
     * @in_ports: sorted Ports list of input ports.
     * @out_ports: sorted Ports list of output ports.
     * @match: match array
     * @mask: mask array (or NULL)
     * @rewrite rewrite array (or NULL)
     * @return: node id or 0 if failed.
     * - add_rule_to_group: just like previous function, except that accept a
     * rule id to group with. Note: for the first element in group, use 0 as
     * group id. For later elements, the index and table is ignored and it is
     * placed next to other element of the group in the same table.
     * remove_rule: removes a rule if exist
     */
    uint64_t add_rule(uint32_t table,int index, List_t in_ports, List_t out_ports,
                  array_t* match, array_t *mask, array_t* rw);
    uint64_t add_rule_to_group(uint32_t table,int index, List_t in_ports,
                               List_t out_ports, array_t* match, array_t *mask,
                               array_t* rw, uint64_t group);
    void remove_rule(uint64_t node_id);

    /*
     * Source Flow Node Management
     * add_source: adds a source node.
     * @hs_object: the source flow
     * @ports: output ports
     */
    uint64_t add_source(hs *hs_object,List_t ports);
    void remove_source(uint64_t id);

    /*
     * Probe Management
     *
     */
    uint64_t add_source_probe(List_t ports, PROBE_MODE mode,
                              Condition *filter, Condition *test,
                              src_probe_callback_t probe_callback,
                              void *callback_data);
    void remove_source_probe(uint64_t id);
    SourceProbeNode *get_source_probe(uint64_t);

    /*
     * get list of nodes based on input port or output port.
     */
    std::list<Node*>* get_nodes_with_outport(uint32_t outport);
    std::list<Node*>* get_nodes_with_inport(uint32_t inport);

    /*
     * prints itself.
     */
    void print_plumbing_network();

    /*
     * Stats
     * - get_pipe_stats: get pipe stats for node.
     */
    void get_pipe_stats(uint64_t node_id,int &fwd_pipeline,int &bck_pipeline,
                    int &influence_on, int &influenced_by);
    void get_source_flow_stats(uint64_t node_id, int &inc, int &exc);

    void save_dependency_graph(std::string file_name);

   private:
    void free_group_memory(uint32_t table, uint64_t group);
    void free_rule_memory(RuleNode *r, bool remove_from_table=true);
    void free_table_memory(uint32_t table);
    void set_port_to_node_maps(Node *n);
    void clear_port_to_node_maps(Node *n);
    void set_table_dependency(RuleNode *r);
    void set_node_pipelines(Node *n);

  };
}

#endif  // SRC_NET_PLUMBER_H_
