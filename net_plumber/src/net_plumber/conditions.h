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

#ifndef SRC_NET_PLUMBER_CONDITIONS_H_
#define SRC_NET_PLUMBER_CONDITIONS_H_

#include "node.h"
#include <string>
#include "net_plumber_utils.h"
/*
 * Language for describing policy using Conditions:
 *
 * Condition:     True OR
 *                False OR
 *                PathCondition OR
 *                HeaderCondition OR
 *                (Condition | Condition) OR
 *                (Condition & Condition) OR
 *                !Condition;
 * PathCondition: list(PathSpecifier);
 * PathSpecifier: PortSpecifier OR
 *                TableSpecifier OR
 *                NextPortsSpecifier OR
 *                NextTablesSpecifier OR
 *                LastPortsSpecifier OR
 *                LastTablesSpecifier OR
 *                SkipNextSpecifier OR
 *                EndPathSpecifier;
 *
 * Note: LastPortsSpecifier and LastTablesSpecifier are only an optimization.
 * They could be created using other specifiers, but given the wide use of these
 * specifiers, they are added here.
 */

class Condition {
 public:
  Condition() {};
  virtual ~Condition() {};
  virtual bool check(Flow *f) = 0;
  virtual std::string to_string() = 0;

};

class TrueCondition : public Condition {
  /*
   * always true
   */
 public:
  TrueCondition() {};
  virtual ~TrueCondition() {};
  bool check(Flow *f) { return true; }
  std::string to_string() { return "Always True"; }
};

class FalseCondition : public Condition {
  /*
   * always false
   */
 public:
  FalseCondition() {};
  virtual ~FalseCondition() {};
  bool check(Flow *f) { return false; }
  std::string to_string() { return "Always False"; }
};

class AndCondition : public Condition {
  /*
   * (c1 & c2)
   */
 private:
  Condition *c1;
  Condition *c2;
 public:
  AndCondition(Condition *c1, Condition *c2) : c1(c1), c2(c2) {}
  virtual ~AndCondition() {delete c1; delete c2;}
  bool check(Flow *f) {return c1->check(f) && c2->check(f);}
  std::string to_string() {
    return "(" + c1->to_string() + ") & (" + c2->to_string() + ")";
  }
};

class OrCondition : public Condition {
  /*
   * (c1 | c2)
   */
 private:
  Condition *c1;
  Condition *c2;
 public:
  OrCondition(Condition *c1, Condition *c2) : c1(c1), c2(c2) {}
  virtual ~OrCondition() {delete c1; delete c2;}
  bool check(Flow *f) {return c1->check(f) || c2->check(f);}
  std::string to_string() {
    return "(" + c1->to_string() + ") | (" + c2->to_string() + ")";
  }
};

class NotCondition : public Condition {
  /*
   * (!c)
   */
 private:
  Condition *c;
 public:
  NotCondition(Condition *c) : c(c) {}
  virtual ~NotCondition() {delete c;}
  bool check(Flow *f) {return !c->check(f);}
  std::string to_string() {return "!(" + c->to_string() + ")";}
};

class HeaderCondition : public Condition {
  /*
   * header intersect h != empty
   */
 protected:
  hs *h;
 public:
  HeaderCondition(hs *match_header) : h(match_header) {}
  ~HeaderCondition() { hs_free(h); }
  bool check(Flow *f);
  std::string to_string();
};

class PathSpecifier;
class PathCondition : public Condition {
  /*
   * the regexp obtained by concat'ing pathlets.
   */
 protected:
  std::list<PathSpecifier*> pathlets;
 public:
  PathCondition() {}
  virtual ~PathCondition();
  void add_pathlet(PathSpecifier *pathlet);
  bool check(Flow *f);
  std::string to_string();
};

class PathSpecifier {
 public:
  virtual bool check_and_move(Flow* &f) = 0;
  virtual std::string to_string() = 0;
  PathSpecifier() {}
  virtual ~PathSpecifier() {}
};

class PortSpecifier : public PathSpecifier {
  /*
   * .*(p = @port)
   */
 private:
  uint32_t port;
 public:
  PortSpecifier(uint32_t p) : port(p) {}
  ~PortSpecifier() {}
  bool check_and_move(Flow* &f);
  std::string to_string();
};

class TableSpecifier : public PathSpecifier {
  /*
   * .*(t = @table)
   */
 private:
  uint32_t table;
 public:
  TableSpecifier(uint32_t t) : table(t) {}
  ~TableSpecifier() {}
  bool check_and_move(Flow* &f);
  std::string to_string();
};

class NextPortsSpecifier : public PathSpecifier {
  /*
   * (p in @ports)
   */
 private:
  List_t ports;
 public:
  NextPortsSpecifier(List_t ports) : ports(ports) {}
  ~NextPortsSpecifier() {free(ports.list);}
  bool check_and_move(Flow* &f);
  std::string to_string();
};

class NextTablesSpecifier : public PathSpecifier {
  /*
   * (t in @tables)
   */
 private:
  List_t tables;
 public:
  NextTablesSpecifier(List_t tables) : tables(tables) {}
  ~NextTablesSpecifier() {free(tables.list);}
  bool check_and_move(Flow* &f);
  std::string to_string();
};

class LastPortsSpecifier : public PathSpecifier {
  /*
   * checks whether the last port is in @ports
   * .*(p in @ports)$
   */
 private:
  List_t ports;
 public:
  LastPortsSpecifier(List_t ports) : ports(ports) {}
  ~LastPortsSpecifier() {free(ports.list);}
  bool check_and_move(Flow* &f);
  std::string to_string();
};

class LastTablesSpecifier : public PathSpecifier {
  /*
   * checks whether the last table is in @ports
   * .*(t in @tables)$
   */
 private:
  List_t tables;
 public:
  LastTablesSpecifier(List_t tables) : tables(tables) {}
  ~LastTablesSpecifier() {free(tables.list);}
  bool check_and_move(Flow* &f);
  std::string to_string();
};

class SkipNextSpecifier : public PathSpecifier {
  /*
   * "." regexp
   */
 public:
  SkipNextSpecifier() {}
  ~SkipNextSpecifier() {}
  bool check_and_move(Flow* &f);
  std::string to_string() {return ".";}
};

class EndPathSpecifier : public PathSpecifier {
  /*
   * $ - checks if we are at the end of path.
   */
 public:
  EndPathSpecifier() {}
  ~EndPathSpecifier() {}
  bool check_and_move(Flow* &f) {return f->p_flow == f->node->get_EOSFI();}
  std::string to_string() { return "$";}
};

#endif  // SRC_NET_PLUMBER_CONDITIONS_H_
