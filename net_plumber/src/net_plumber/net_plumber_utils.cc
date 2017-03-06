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

#include "net_plumber_utils.h"
#include <stdarg.h>
#include <sstream>
#include <stdlib.h>

using namespace std;

int compare (const void * a, const void * b)
{
  return ( *(uint32_t*)a - *(uint32_t*)b );
}

List_t make_unsorted_list(uint32_t count,...) {
  va_list ports;
  va_start(ports,count);
  List_t result;
  result.size = count;
  result.shared = false;
  if (count > 0)
    result.list = (uint32_t *)malloc(count * sizeof(uint32_t));
  else
    result.list = NULL;
  for (uint32_t i = 0; i < count; i++) {
    result.list[i] = va_arg(ports,uint32_t);
  }
  va_end(ports);
  return result;
}

List_t make_sorted_list_from_array (uint32_t count, uint32_t elems[]) {
  List_t result;
  result.size = count;
  result.shared = false;
  if (count > 0)
    result.list = (uint32_t *)malloc(count * sizeof(uint32_t));
  else
    result.list = NULL;
  for (uint32_t i = 0; i < count; i++) {
    result.list[i] = elems[i];
  }
  qsort(result.list, result.size, sizeof(uint32_t), compare);
  return result;
}

List_t make_sorted_list(uint32_t count,...) {
  va_list ports;
  va_start(ports,count);
  List_t result;
  result.size = count;
  result.shared = false;
  if (count > 0)
    result.list = (uint32_t *)malloc(count * sizeof(uint32_t));
  else
    result.list = NULL;
  for (uint32_t i = 0; i < count; i++) {
    result.list[i] = va_arg(ports,uint32_t);
  }
  va_end(ports);
  qsort(result.list, result.size, sizeof(uint32_t), compare);
  return result;
}

List_t intersect_sorted_lists(List_t a, List_t b) {
  if (a.shared && b.shared && a.list == b.list) {
      List_t share_list = a;
      return share_list;
  }
  uint32_t *v = (uint32_t *)malloc(sizeof(uint32_t) * a.size);
  uint32_t i = 0;
  uint32_t j = 0;
  int count = 0;
  while(i < a.size && j < b.size) {
    if (a.list[i] == b.list[j]) {
      j++;
      v[count++] = a.list[i++];
    } else if (a.list[i] < b.list[j]) {
      i++;
    } else {
      j++;
    }
  }
  List_t result;
  result.size = count;
  result.shared = false;
  if (count > 0) {
    result.list = (uint32_t *)malloc(count * sizeof(uint32_t));
  } else {
    result.list = NULL;
  }
  memcpy(result.list, v, count * sizeof(uint32_t));
  free(v);
  return result;
}

std::string list_to_string(List_t p) {
  stringstream result;
  result << "( ";
  for (uint32_t i = 0; i < p.size; i++) {
    result << p.list[i] << " ";
  }
  result << ")";
  return result.str();
}

bool lists_has_intersection(List_t a, List_t b) {
  uint32_t i = 0;
  uint32_t j = 0;
  while(i < a.size && j < b.size) {
    if (a.list[i] == b.list[j]) {
      return true;
    } else if (a.list[i] < b.list[j]) {
      i++;
    } else {
      j++;
    }
  }
  return false;
}

List_t copy_list(List_t l) {
  List_t result = l;
  result.list = (uint32_t *)malloc(l.size * sizeof(uint32_t));
  memcpy(result.list, l.list, l.size * sizeof(uint32_t));
  return result;
}

bool elem_in_sorted_list(uint32_t elem, List_t list) {
  return bsearch(&elem, list.list, list.size, sizeof(uint32_t), compare);
}

bool elem_in_unsorted_list(uint32_t elem, List_t list) {
  for (uint32_t i = 0; i < list.size; i++) {
    if (elem == list.list[i]) return true;
  }
  return false;
}
