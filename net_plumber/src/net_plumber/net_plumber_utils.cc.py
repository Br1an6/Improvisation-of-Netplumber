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

#include "net_plumber_utils.h"
#include <stdarg.h>
#include <sstream>
#include <stdlib.h>

using namespace std

int compare ( void * a, * b)
  return ( *(uint32_t*)a - *(uint32_t*)b )


def make_unsorted_list(self, count,...):  va_list ports
  va_start(ports,count)
  List_t result
  result.size = count
  result.shared = False
  if count > 0:
    result.list = (uint32_t *)malloc(count * sizeof(uint32_t))
  else:
    result.list = NULL
  for (i = 0; i < count; i++)    result.list[i] = va_arg(ports,uint32_t)

  va_end(ports)
  return result


List_t make_sorted_list_from_array (uint32_t count, elems[])  List_t result
  result.size = count
  result.shared = False
  if count > 0:
    result.list = (uint32_t *)malloc(count * sizeof(uint32_t))
  else:
    result.list = NULL
  for (i = 0; i < count; i++)    result.list[i] = elems[i]

  qsort(result.list, result.size, sizeof(uint32_t), compare)
  return result


def make_sorted_list(self, count,...):  va_list ports
  va_start(ports,count)
  List_t result
  result.size = count
  result.shared = False
  if count > 0:
    result.list = (uint32_t *)malloc(count * sizeof(uint32_t))
  else:
    result.list = NULL
  for (i = 0; i < count; i++)    result.list[i] = va_arg(ports,uint32_t)

  va_end(ports)
  qsort(result.list, result.size, sizeof(uint32_t), compare)
  return result


def intersect_sorted_lists(self, a, b):  if a.shared and b.shared and a.list == b.list:      share_list = a
      return share_list

  uint32_t *v = (uint32_t *)malloc(sizeof(uint32_t) * a.size)
  i = 0
  j = 0
  count = 0
  while(i < a.size and j < b.size)    if a.list[i] == b.list[j]:      j++
      v[count++] = a.list[i++]
    } elif a.list[i] < b.list[j]:      i++
    } else:
      j++


  List_t result
  result.size = count
  result.shared = False
  if count > 0:    result.list = (uint32_t *)malloc(count * sizeof(uint32_t))
  } else:
    result.list = NULL

  memcpy(result.list, v, * sizeof(uint32_t))
  free(v)
  return result


def list_to_string(self, p):  stringstream result
  result << "( "
  for (i = 0; i < p.size; i++)    result << p.list[i] << " "

  result << ")"
  return result.str()


def lists_has_intersection(self, a, b):  i = 0
  j = 0
  while(i < a.size and j < b.size)    if a.list[i] == b.list[j]:      return True
    } elif a.list[i] < b.list[j]:      i++
    } else:
      j++


  return False


def copy_list(self, l):  result = l
  result.list = (uint32_t *)malloc(l.size * sizeof(uint32_t))
  memcpy(result.list, l.list, l.size * sizeof(uint32_t))
  return result


def elem_in_sorted_list(self, elem, list):  return bsearch(&elem, list.list, list.size, sizeof(uint32_t), compare)


def elem_in_unsorted_list(self, elem, list):  for (i = 0; i < list.size; i++)    if (elem == list.list[i]) return True

  return False

