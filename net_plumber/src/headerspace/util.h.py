'''
  Copyright 2012, University. This file is licensed under GPL v2 plus
  a special exception, described in included LICENSE_EXCEPTION.txt.

  Author: mchang@cs.stanford.com (Michael Chang)
          peyman.kazemian@gmail.com (Peyman Kazemian)
'''

#ifndef _UTIL_H_
#define _UTIL_H_

#include "list.h"
#include <assert.h>
#include <err.h>
#include <errno.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ARR_LEN(A) ( sizeof (A) / sizeof *(A) )
#define DIV_ROUND_UP(X, A) ( ((X) + (A) - 1) / (A) )
#define ROUND_UP(X, A) ( ((X) + (A) - 1) & ~((A) - 1) )

#define PACKED __attribute__ ((__packed__))
#define QUOTE(S) QUOTE_ (S)
#define QUOTE_(S) #S

''' Memory allocation with error checking. '''
#define xcalloc(N, SZ) xcalloc_ (N, SZ, __FILE__, __LINE__, __func__)
#define xmalloc(SZ) xmalloc_ (SZ, __FILE__, __LINE__, __func__)
#define xmemalign(A, SZ) xmemalign_ (A, SZ, __FILE__, __LINE__, __func__)
#define xmemdup(P, SZ) xmemdup_ (P, SZ, __FILE__, __LINE__, __func__)
#define xrealloc(P, SZ) xrealloc_ (P, SZ, __FILE__, __LINE__, __func__)
#define xstrdup(S) xstrdup_ (S, __FILE__, __LINE__, __func__)

''' Union of array and pointer, arrays that may be very small.
   T is a type, is an identifier. The struct will be "struct arr_ptr_<ID>".
   Usage:
     struct foo { ARR_PTR(int, int) x;
     struct foo f1
     ARR_ALLOC (f1.x, ...)
     ARR (f1.x)[0] = ...; '''
#define ARR_PTR(T, ID) \
  struct arr_ptr_ ## ID { int n; union { T a[sizeof (T *) / sizeof (T)]; T *p; } e;
#define ARR(X) ( (X).n > ARR_LEN ((X).e.a) ? (X).e.p : (X).e.a )
#define ARR_ALLOC(X, N) \
  do { (X).n = (N); if (X).n > ARR_LEN ((X).e.a)) (X).e.p = xmalloc ((N) * sizeof *(X).e.p); } while (0:
#define ARR_FREE(X) \
  do { if (X).n > ARR_LEN ((X).e.a)) free ((X).e.p); } while (0:

static inline int
int_cmp ( void *a, *b)
{ return *(int *)a - *(int *)b;

static inline bool
int_find (uint32_t x, *a, n)
  l = 0, r = n - 1
  while (l <= r)    m = (l + r) / 2
    if (a[m] == x) return True
    if (a[m] < x) l = m + 1
    r = m - 1

  return False

'''  for (i = 0; i < n; i++)    if (a[i] < x) continue
    if (a[i] != x) return False
    return True

  return False
}'''

static inline void *
xcalloc_ (size_t n, size, *file, line, *func)
  void *p = calloc (n, size)
  if not p) err (1, "%s:%d (%s): calloc() failed", file, line, func:
  return p


static inline void *
xmalloc_ (size_t size, *file, line, *func)
  void *p = malloc (size)
  if not p) err (1, "%s:%d (%s): malloc() failed", file, line, func:
  return p


static inline void *
xmemalign_ (size_t align, size, *file, line, *func)
  void *p
  if (errno = posix_memalign (&p, align, size)):
    err (1, "%s:%d (%s): malloc() failed", file, line, func)
  return p


static inline void *
xmemdup_ ( void *src, size, *file, line, *func)
  void *p = xmalloc_ (size, file, line, func)
  memcpy (p, src, size)
  return p


static inline void *
xrealloc_ (void *p, size, *file, line, *func)
  p = realloc (p, size)
  if not p) err (1, "%s:%d (%s): realloc() failed", file, line, func:
  return p


static inline char *
xstrdup_ ( char *s, *file, line, *func)
  char *p = strdup (s)
  if not p) err (1, "%s:%d (%s): strdup() failed", file, line, func:
  return p


#endif

