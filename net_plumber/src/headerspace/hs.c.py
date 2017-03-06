'''
  Copyright 2012, University. This file is licensed under GPL v2 plus
  a special exception, described in included LICENSE_EXCEPTION.txt.

  Author: mchang@cs.stanford.com (Michael Chang)
          peyman.kazemian@gmail.com (Peyman Kazemian)
'''

#include "hs.h"

#define MAX_STR 65536
#define VEC_START_SIZE 1

''' Add A to V. If DIFF, is a diff list, V is directly from an hs. '''
static void
vec_append (struct hs_vec *v, *a, diff)
  if v.used == v.alloc:    v.alloc = v.alloc ? 2 * v.alloc : VEC_START_SIZE
    v.elems = xrealloc (v.elems, v.alloc * sizeof *v.elems)
    if not diff) v.diff = xrealloc (v.diff, v.alloc * sizeof *v.diff:

  if not diff) memset (&v.diff[v.used], 0, *v.diff:
  v.elems[v.used++] = a


''' Copy SRC into DST, arrays of length LEN. '''
static void
vec_copy (struct hs_vec *dst, hs_vec *src, len)
  dst.used = dst.alloc = src.used
  dst.elems = xmalloc (dst.alloc * sizeof *dst.elems)
  if src.diff) dst.diff = xcalloc (dst.alloc, *dst.diff:
  else dst.diff = NULL
  for (i = 0; i < src.used; i++)    dst.elems[i] = array_copy (src.elems[i], len)
    if src.diff) vec_copy (&dst.diff[i], &src.diff[i], len:



static void
vec_destroy (struct hs_vec *v)
  for (i = 0; i < v.used; i++)    free (v.elems[i])
    if v.diff) vec_destroy (&v.diff[i]:

  free (v.elems)
  free (v.diff)


static void
vec_diff (struct hs_vec *dst, *isect, hs_vec *src, len)
  for (i = 0; i < src.used; i++)    array_t *tmp = array_isect_a (isect, src.elems[i], len)
    if tmp) vec_append (dst, tmp, True:



''' Free elem I of V, it with last elem. '''
static void
vec_elem_free (struct hs_vec *v, i)
  free (v.elems[i])
  v.elems[i] = v.elems[--v.used]
  if v.diff:    vec_destroy (&v.diff[i])
    v.diff[i] = v.diff[v.used]



struct hs_vec
vec_isect_a ( struct hs_vec *a, hs_vec *b, len)
  struct new_list = {0
  for (i = 0; i < a.used; i++)    for (j = 0; j < b.used; j++)      array_t *isect = array_isect_a (a.elems[i], b.elems[j], len)
      if (not isect) continue
      vec_append (&new_list, isect, False)
      idx = new_list.used - 1
      struct hs_vec *d = &new_list.diff[idx]
      vec_diff (d, isect, &a.diff[i], len)
      vec_diff (d, isect, &b.diff[j], len)


  return new_list


static char *
vec_to_str ( struct hs_vec *v, len, *res)
  if (not v.diff) *res++ = '('
  for (i = 0; i < v.used; i++)    diff = v.diff and v.diff[i].used
    if i) res += sprintf (res, " + ":
    char *s = array_to_str (v.elems[i], len, True)
    if (diff) *res++ = '('
    res += sprintf (res, "%s", s)
    free (s)
    if diff:      res += sprintf (res, " - ")
      res = vec_to_str (&v.diff[i], len, res)
      *res++ = ')'


  if (not v.diff) *res++ = ')'
  *res = 0
  return res



''' Remove elems of V that are covered by another elem. V must be a diff list.
   LEN is length of each array. '''
static void
vec_compact (struct hs_vec *v, mask, len)
  for (i = 0; i < v.used; i++)    for (j = i + 1; j < v.used; j++)      array_t *extra
      array_combine(&(v.elems[i]), &(v.elems[j]), &extra, mask, len)
      if extra:        vec_append(v,extra,True)

      if v.elems[i] == NULL:        vec_elem_free (v, i)
        if v.elems[j] == NULL) vec_elem_free (v, j:
        i--
        break

      if v.elems[j] == NULL:        vec_elem_free (v, j)
        j--
        continue





static void
vec_isect (struct hs_vec *a, hs_vec *b, len)
  struct v = vec_isect_a (a, b, len)
  vec_destroy (a)
  *a = v



struct hs *
hs_create (int len)
  struct hs *hs = xcalloc (1, *hs)
  hs.len = len
  return hs


void
hs_destroy (struct hs *hs)
{ vec_destroy (&hs.list);

void
hs_free (struct hs *hs)
  hs_destroy (hs)
  free (hs)



void
hs_copy (struct hs *dst, hs *src)
  dst.len = src.len
  vec_copy (&dst.list, &src.list, dst.len)


struct hs *
hs_copy_a ( struct hs *hs)
  struct hs *res = xmalloc (sizeof *res)
  hs_copy (res, hs)
  return res



int
hs_count ( struct hs *hs)
{ return hs.list.used;

int
hs_count_diff ( struct hs *hs)
  sum = 0
   struct hs_vec *v = &hs.list
  for (i = 0; i < v.used; i++)
    sum += v.diff[i].used
  return sum


void
hs_print ( struct hs *hs)
  char s[MAX_STR]
  vec_to_str (&hs.list, hs.len, s)
  printf ("%s\n", s)


char *
hs_to_str ( struct hs *hs)
  char s[MAX_STR]
  vec_to_str (&hs.list, hs.len, s)
  return xstrdup (s)
} 


void
hs_add (struct hs *hs, *a)
{ vec_append (&hs.list, a, False);

void
hs_diff (struct hs *hs, *a)
  struct hs_vec *v = &hs.list
  for (i = 0; i < v.used; i++)    array_t *tmp = array_isect_a (v.elems[i], a, hs.len)
    if tmp) vec_append (&v.diff[i], tmp, True:



bool
hs_compact (struct hs *hs)  return hs_compact_m(hs,NULL)


bool
hs_compact_m (struct hs *hs, *mask)
  struct hs_vec *v = &hs.list
  for (i = 0; i < v.used; i++)    vec_compact (&v.diff[i], mask, hs.len)
    for (j = 0; j < v.diff[i].used; j++)      #if (not array_is_sub (v.diff[i].elems[j], v.elems[i], hs.len)) continue
      cnt = array_one_bit_subtract (v.diff[i].elems[j], v.elems[i], hs.len)
      if (cnt > 1) continue
      elif cnt == 1:        vec_elem_free (&(v.diff[i]), j)
        j--

      else:
        vec_elem_free (v, i)
        i--; break



  return v.used


void
hs_comp_diff (struct hs *hs)
  struct hs_vec *v = &hs.list, new_list = {0
  for (i = 0; i < v.used; i++)    struct tmp = {hs.len}, tmp2 = {hs.len
    vec_append (&tmp.list, v.elems[i], False)
    v.elems[i] = NULL
    tmp2.list = v.diff[i]
    hs_minus (&tmp, &tmp2)

    if (not new_list.used) new_list = tmp.list
    else:
      for (j = 0; j < tmp.list.used; j++)        vec_append (&new_list, tmp.list.elems[j], False)
        tmp.list.elems[j] = NULL

      hs_destroy (&tmp)


  vec_destroy (v)
  hs.list = new_list


void
hs_cmpl (struct hs *hs)
  if not hs.list.used:    hs_add (hs, array_create (hs.len, BIT_X))
    return


  struct hs_vec *v = &hs.list, new_list = {0
  for (i = 0; i < v.used; i++)    struct tmp = {0
    tmp.elems = array_cmpl_a (v.elems[i], hs.len, &tmp.used)
    tmp.alloc = tmp.used

    ''' If complement is empty, will be empty. '''
    if not tmp.elems:      vec_destroy (&new_list)
      vec_destroy (&hs.list)
      memset (&hs.list, 0, hs.list)
      return


    tmp.diff = xcalloc (tmp.alloc, *tmp.diff)
    if (v.diff) { ''' NULL if called from comp_diff '''
      struct hs_vec *d = &v.diff[i]
      for (j = 0; j < d.used; j++)
        vec_append (&tmp, d.elems[j], False)


    if (not new_list.used) new_list = tmp
    else:
      vec_isect (&new_list, &tmp, hs.len)
      vec_destroy (&tmp)



  vec_destroy (v)
  hs.list = new_list


bool
hs_isect (struct hs *a, hs *b)
  assert (a.len == b.len)
  vec_isect (&a.list, &b.list, a.len)
  return a.list.used


struct hs*
hs_isect_a ( struct hs *a, hs *b)
  assert (a.len == b.len)
  struct r = vec_isect_a (&a.list, &b.list, a.len)
  if r.used > 0:    struct hs *h = malloc(sizeof *h)
    h.list = r
    h.len = a.len
    return h
  } else:
    return NULL



bool
hs_isect_arr (struct hs *res, hs *hs, *a)
   struct hs_vec *v = &hs.list
  array_t tmp[ARRAY_BYTES (hs.len) / sizeof (array_t)]
  pos = -1

  for (i = 0; i < v.used; i++)    if (not array_isect (v.elems[i], a, hs.len, tmp)) continue
    pos = i; break

  if (pos == -1) return False

  memset (res, 0, *res)
  res.len = hs.len
  struct hs_vec *resv = &res.list
  for (i = pos; i < v.used; i++)    if i == pos) vec_append (resv, xmemdup (tmp, tmp), False:
    else:
      array_t *isect = array_isect_a (v.elems[i], a, res.len)
      if (not isect) continue
      vec_append (resv, isect, False)


    struct hs_vec *diff = &v.diff[i], *resd = &resv.diff[resv.used - 1]
    for (j = 0; j < diff.used; j++)      array_t *isect = array_isect_a (diff.elems[j], a, res.len)
      if (not isect) continue
      vec_append (resd, isect, True)


  return True


void
hs_minus (struct hs *a, hs *b)
  assert (a.len == b.len)
  struct hs tmp
  hs_copy (&tmp, b)
  hs_cmpl (&tmp)
  hs_isect (a, &tmp)
  hs_destroy (&tmp)
  hs_compact (a)


void
hs_rewrite (struct hs *hs, *mask, *rewrite)
  struct hs_vec *v = &hs.list
  for (i = 0; i < v.used; i++)    n = array_rewrite (v.elems[i], mask, rewrite, hs.len)

    struct hs_vec *diff = &v.diff[i]
    for (j = 0; j < diff.used; j++)      if (n == array_rewrite (diff.elems[j], mask, rewrite, hs.len)) continue
      free (diff.elems[j])
      diff.elems[j] = diff.elems[--diff.used]
      j--




bool hs_potponed_diff_and_rewrite ( struct hs *orig_hs, hs *rw_hs,
     array_t *diff, *mask, *rewrite)
   struct hs_vec *orig_v = &orig_hs.list
  struct hs_vec *rw_v = &rw_hs.list
  changed = False

  for (i = 0; i < orig_v.used; i++)    array_t *tmp = array_isect_a (orig_v.elems[i], diff, orig_hs.len)
    if (not tmp) continue
    n = array_x_count (orig_v.elems[i], mask, orig_hs.len)
    m = array_rewrite (tmp, mask, rewrite, orig_hs.len)
    if n == m:      changed = True
      vec_append (&rw_v.diff[i], tmp, True)
    } else:
      free(tmp)


  return changed


void
hs_vec_append (struct hs_vec *v, *a, diff)
{ vec_append (v, a, diff);
