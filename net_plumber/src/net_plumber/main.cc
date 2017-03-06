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

#include "test/net_plumber_basic_unit.h"
#include "test/net_plumber_plumbing_unit.h"
#include "test/conditions_unit.h"
#include <string.h>
#include "main_processes.h"
#include "net_plumber.h"
// For UnitTesting
#include <cppunit/ui/text/TestRunner.h>
#include <cppunit/extensions/TestFactoryRegistry.h>
#include <cppunit/CompilerOutputter.h>
#include <cppunit/TestResult.h>
#include <cppunit/TestResultCollector.h>
#include <cppunit/BriefTestProgressListener.h>
// For Logging
#include <log4cxx/logger.h>
#include "log4cxx/propertyconfigurator.h"
#include <log4cxx/basicconfigurator.h>

#include "rpc_handler.h"
#include <csignal>

using namespace log4cxx;
using namespace log4cxx::helpers;
using namespace::std;
using namespace net_plumber;

static bool server_stop;

static void sig_stop(int) {
  server_stop = true;
}

void run_server(string ip, int port, NetPlumber *N) {
  server_stop = false;
  signal(SIGINT, sig_stop);
  signal(SIGTERM, sig_stop);

  net_plumber::RpcHandler handler(N);
  Json::Rpc::TcpServer server(ip, port);

  if (!networking::init()) errx(1, "Couldn't initialize networking.");
  handler.initServer(server);
  if (!server.Bind()) errx(1, "bind(0.0.0.0:%d) failed.", port);
  if (!server.Listen()) errx(1, "listen() failed.");

  printf("Server listening on port %d.\n", port);
  while (!server_stop) server.WaitMessage(1000);

  server.Close();
  networking::cleanup();

}

void run_tests() {
  CPPUNIT_TEST_SUITE_REGISTRATION( NetPlumberBasicTest );
  CPPUNIT_TEST_SUITE_REGISTRATION( NetPlumberPlumbingTest );
  CPPUNIT_TEST_SUITE_REGISTRATION( ConditionsTest );

  // informs test-listener about testresults
  CPPUNIT_NS::TestResult testresult;

  // register listener for collecting the test-results
  CPPUNIT_NS::TestResultCollector collectedresults;
  testresult.addListener (&collectedresults);

  // register listener for per-test progress output
  CPPUNIT_NS::BriefTestProgressListener progress;
  testresult.addListener (&progress);

  // insert test-suite at test-runner by registry
  CPPUNIT_NS::TestRunner testrunner;
  testrunner.addTest (CPPUNIT_NS :: TestFactoryRegistry :: getRegistry ().
                      makeTest ());
  testrunner.run (testresult);

  // output results in compiler-format
  CPPUNIT_NS::CompilerOutputter compileroutputter(&collectedresults, std::cerr);
  compileroutputter.write ();
}

int main(int argc, char* argv[]) {
  bool do_run_server = false;
  bool do_run_test = false;
  bool do_load_json_files = false;
  bool do_load_policy = false;

  string log_config_file = "";
  string json_files_path = "";
  string policy_json_file = "";
  int hdr_len = 1;
  string server_ip;
  int server_port;
  array_t *filter = NULL;

  for (int i = 1; i < argc; i++) {
    if ( strcmp(argv[i] , "--help") == 0 ) {
      printf("Usage: net_plumber [run option(s)][settings]\n");
      printf("  run options:\n");
      printf("\t --test  runs all the unit tests.\n");
      printf("\t --server <ip> <port> : runs net_plumber as a server listening for updates on address <ip> and port <port>.\n");
      printf("\t --load <path> : load the rules from json files in the <path>.\n");
      printf("\t --policy <file> : loads the source and probe nodes from a json policy <file>.\n");
      printf("\t --filter <filter-wc> : cluster based on <wc-filter>.\n");

      printf("  settings:\n");
      printf("\t --log4j-config <config file> : path to <log4j config> file.\n");
      printf("\t --hdr-len <length> : <length> of packet header (default is 1 byte).\n");
      break;
    }
    if ( strcmp(argv[i],"--server") == 0 ) {
      if (i + 2 >= argc) {
        printf("Please specify IP and port for server.\n");
        return -1;
      }
      server_ip = argv[++i];
      server_port = atoi(argv[++i]);
      do_run_server = true;
    }
    if ( strcmp(argv[i],"--test") == 0 ) {
      do_run_test = true;
    }

    if ( strcmp(argv[i],"--policy") == 0)  {
      if (i+1 >= argc) {
        printf("Please specify policy file after --policy.\n");
        return -1;
      }
      do_load_policy = true;
      policy_json_file = string(argv[++i]);
    }

    if ( strcmp(argv[i],"--load") == 0)  {
      if (i+1 >= argc) {
        printf("Please specify path to json files after --load.\n");
        return -1;
      }
      do_load_json_files = true;
      json_files_path = string(argv[++i]);
    }

    if ( strcmp(argv[i],"--filter") == 0)  {
      if (i+1 >= argc) {
        printf("Please specify a header after --filter.\n");
        return -1;
      }
      filter = array_from_str(argv[++i]);
    }

    if ( strcmp(argv[i],"--log4j-config") == 0 ) {
      if (i+1 >= argc) {
        printf("Please specify config file name after --log4j-config.\n");
        return -1;
      }
      log_config_file = string(argv[++i]);
    }

    if ( strcmp(argv[i],"--hdr-len") == 0 ) {
      if (i+1 >= argc) {
        printf("Please specify length of header after --hdr-len.\n");
        return -1;
      }
      hdr_len = atoi(argv[++i]);
    }
  }
  //configure log4cxx.
  if (log_config_file != "") {
    PropertyConfigurator::configure("Log4cxxConfig.conf");
  } else {
    BasicConfigurator::configure();
  }

  if (do_run_test) {
    run_tests();
  }

  NetPlumber *N = new NetPlumber(hdr_len);

  if (do_load_json_files) {
    //list<long> l =
    load_netplumber_from_dir(json_files_path, N, NULL);
    /*ofstream myfile;
    char buf[70];
    myfile.open ("tmp.txt",ios::app);
    list<long>::iterator it;
    for (it = l.begin(); it != l.end(); it++) {
      myfile << *it <<  ", ";
    }
    myfile << endl;*/
  }

  if (do_load_policy) {
    load_policy_file(policy_json_file,N,filter);
  }

  if (do_run_server) {
    run_server(server_ip, server_port,N);
  } else {
    printf("Done! Cleaning up the NetPlumber\n");
    //delete N;
  }
  return 0;

}

