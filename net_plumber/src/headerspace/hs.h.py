'''
  Copyright 2012, University. This file is licensed under GPL v2 plus
  a special exception, described in included LICENSE_EXCEPTION.txt.

  Author: mchang@cs.stanford.com (Michael Chang)
          peyman.kazemian@gmail.com (Peyman Kazemian)
'''

#ifndef _HS_H_
#define _HS_H_

#include "array.h"

struct hs_vec  array_t **elems
  struct hs_vec *diff
  int used, alloc


struct hs  int len
  struct hs_vec list


struct hs *hs_create  (int len)
void       hs_destroy (struct hs *hs)
void       hs_free    (struct hs *hs)

void       hs_copy   (struct hs *dst, hs *src)
struct hs *hs_copy_a ( struct hs *src)

int   hs_count      ( struct hs *hs)
int   hs_count_diff ( struct hs *hs)
void  hs_print      ( struct hs *hs)
char *hs_to_str     ( struct hs *hs)


void hs_add  (struct hs *hs, *a)
void hs_diff (struct hs *hs, *a)

bool hs_compact   (struct hs *hs)
bool hs_compact_m (struct hs *hs, mask)
void hs_comp_diff (struct hs *hs)
void hs_cmpl      (struct hs *hs)
bool hs_isect     (struct hs *a, hs *b)
struct hs* hs_isect_a ( struct hs *a, hs *b)
bool hs_isect_arr (struct hs *dst, hs *src, *arr)
void hs_minus     (struct hs *a, hs *b)
void hs_rewrite   (struct hs *hs, *mask, *rewrite)
void hs_vec_append (struct hs_vec *v, *a, diff)

'''
 * rewrites diff according to mask/rewrite array and diff it from rw_hs only if
 * the following condition is met: "If diff_hs was diff'ed from orig_hs and then
 * rewritten by mask/rewrite, appears in final result"
 '''
bool hs_potponed_diff_and_rewrite ( struct hs *orig_hs, hs *rw_hs,
     array_t *diff, *mask, *rewrite)

#endif

