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

#ifndef NET_PLUMBER_UTILS_H_
#define NET_PLUMBER_UTILS_H_

#include <string>
extern "C" {
  #include "../headerspace/util.h"
}

struct PACKED List_t {
  uint32_t size;
  uint32_t *list;
  bool shared;
};

List_t      make_sorted_list (uint32_t count,...);
List_t      make_sorted_list_from_array (uint32_t count, uint32_t elems[]);
List_t      make_unsorted_list (uint32_t count,...);
List_t      intersect_sorted_lists (List_t a, List_t b);
std::string list_to_string (List_t p);
bool        elem_in_sorted_list (uint32_t elem, List_t list);
bool        elem_in_unsorted_list (uint32_t elem, List_t list);
bool        lists_has_intersection(List_t a, List_t b);
List_t      copy_list (List_t l);


#endif  // NET_PLUMBER_UTILS_H_
