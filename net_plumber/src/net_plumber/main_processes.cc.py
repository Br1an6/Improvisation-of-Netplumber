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

#include "main_processes.h"
#include "rpc_handler.h"
#include "../jsoncpp/json/json.h"
#include <fstream>
#include <dirent.h>
#include <sys/time.h>
extern "C"  #include "../headerspace/array.h"


using namespace net_plumber
using namespace std

def load_netplumber_from_dir(self, json_file_path, * N, *filter):  struct timeval start, end
  rule_counter = 0
  ifstream jsfile
  Json.Value root
  Json.Reader reader
  list<long> t_list
  total_run_time = 0

  # read topology
  file_name = json_file_path + "/" + "topology.json"
  jsfile.open (file_name.c_str())
  if not jsfile.good():    printf("Error opening the file %s\n",file_name.c_str())
    return t_list

  reader.parse(jsfile,root,False)
  topology = root["topology"]
  for (i = 0; i < topology.size(); i++)    N.add_link(topology[i]["src"].asInt(),topology[i]["dst"].asInt())

  N.print_topology()
  jsfile.close()

  #read every json file.
  struct dirent *ent
  DIR *dir = opendir(json_file_path.c_str())
  if dir != NULL:    while ((ent = readdir(dir)) != NULL )      file_name = string(ent.d_name)
      if (file_name.find(".rules.json") != string.npos or
          file_name.find(".tf.json") != string.npos)        # open the json file
        file_name = json_file_path + "/" + file_name
        printf("=== Loading rule file %s to NetPlumber ===\n",file_name.c_str())
        jsfile.open (file_name.c_str())
        reader.parse(jsfile,root,False)

        # get the table id, and rules
        table_id = root["id"].asInt()
        ports = root["ports"]
        rules = root["rules"]

        # create the table
        N.add_table(table_id,val_to_list(ports))

        # add the rules
        for (i = 0; i < rules.size(); i++)          run_time = 0
          rule_counter++
          action = rules[i]["action"].asString()
          if action == "fwd" or action == "rw" '''or action == "encap"''':            array_t *match = val_to_array(rules[i]["match"])
            if filter and not array_isect(match,filter,N.get_length(),match):              run_time = 0
            } else:
              gettimeofday(&start, NULL)
              N.add_rule(table_id,
                          0,
                          val_to_list(rules[i]["in_ports"]),
                          val_to_list(rules[i]["out_ports"]),
                          match,
                          val_to_array(rules[i]["mask"]),
                          val_to_array(rules[i]["rewrite"]))
              gettimeofday(&end, NULL)
              run_time = end.tv_usec - start.tv_usec
              if run_time < 0:                run_time = 1000000 * (end.tv_sec - start.tv_sec)

              total_run_time += run_time

            t_list.push_back(run_time)
          } elif action == "multipath":            mp_rules = rules[i]["rules"]
            group = 0
            for (i = 0; i < mp_rules.size(); i++)              action = mp_rules[i]["action"].asString()
              if action == "fwd" or action == "rw" '''or action == "encap"''':                id = N.add_rule_to_group(
                                table_id,
                                0,
                                val_to_list(mp_rules[i]["in_ports"]),
                                val_to_list(mp_rules[i]["out_ports"]),
                                val_to_array(mp_rules[i]["match"]),
                                val_to_array(mp_rules[i]["mask"]),
                                val_to_array(mp_rules[i]["rewrite"]),
                                group)
                if (i == 0) group = id





        # clean up
        jsfile.close()


    #N.print_plumbing_network()

  printf("total run time is %ld us. rules: %d average: %ld us\n",total_run_time,rule_counter,total_run_time/rule_counter)
  closedir(dir)
  return t_list


def load_policy_file(self, json_policy_file, *N, *filter):  printf("Loading policy file %s\n",json_policy_file.c_str())
  time_t start, end
  ifstream jsfile
  Json.Value root
  Json.Reader reader

  # read topology
  jsfile.open (json_policy_file.c_str())
  if not jsfile.good():    printf("Error opening the file %s\n",json_policy_file.c_str())
    return

  reader.parse(jsfile,root,False)
  commands = root["commands"]
  start = clock()
  for (i = 0; i < commands.size(); i++)    type = commands[i]["method"].asString()
    if type == "add_source":      hs *tmp = val_to_hs(commands[i]["params"]["hs"], N.get_length())
      hs *h
      if filter:        h = hs_create(N.get_length())
        hs_isect_arr(h,tmp,filter)
        hs_free(tmp)
      } else:
        h = tmp

      ports = val_to_list(commands[i]["params"]["ports"])
      N.add_source(h,ports)
    } elif type == "add_source_probe":      ports = val_to_list(commands[i]["params"]["ports"])
      mode = not strcasecmp(commands[i]["params"]["mode"].asCString(), "universal")
          ? UNIVERSAL : EXISTENTIAL
      Condition *filter = val_to_cond(commands[i]["params"]["filter"], N.get_length())
      Condition *test = val_to_cond(commands[i]["params"]["test"], N.get_length())
      N.add_source_probe(ports, mode, filter, test, NULL, NULL)
    } elif type == "add_link":      from_port = commands[i]["params"]["from_port"].asUInt()
      to_port = commands[i]["params"]["to_port"].asUInt()
      N.add_link(from_port,to_port)


  end = clock()
  printf("Loaded policy file in %2lf seconds\n",(double(end - start) / CLOCKS_PER_SEC))
  jsfile.close()




