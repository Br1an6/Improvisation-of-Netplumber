'''
  Copyright 2012, University. This file is licensed under GPL v2 plus
  a special exception, described in included LICENSE_EXCEPTION.txt.

  Author: mchang@cs.stanford.com (Michael Chang)
          peyman.kazemian@gmail.com (Peyman Kazemian)
'''

#ifndef _ARRAY_H_
#define _ARRAY_H_

#include "util.h"

#if __x86_64 or __amd64 or _M_X64
typedef uint64_t array_t
#else:
typedef uint32_t array_t
#endif

enum bit_val { BIT_Z = 0, BIT_0, BIT_1, BIT_X, BIT_UNDEF

#define ARRAY_BYTES(L) ( ROUND_UP (2 * (L), sizeof (array_t)) )

array_t *array_create   (int len, bit_val val)
void     array_free     (array_t *a)

array_t *array_copy     ( array_t *a, len)
array_t *array_from_str ( char *s)
char    *array_to_str   ( array_t *a, len, decimal)

bool array_has_x  ( array_t *a, len)
bool array_has_z  ( array_t *a, len)
bool array_is_eq  ( array_t *a, *b, len)
''' True if B is a subset of A. '''
bool array_is_sub ( array_t *a, *b, len)

enum bit_val array_get_bit  ( array_t *a, byte, bit)
uint16_t     array_get_byte ( array_t *a, byte)
void         array_set_bit  (array_t *a, bit_val val, byte, bit)
void         array_set_byte (array_t *a, val, byte)

void array_and     ( array_t *a, *b, len, *res)
bool array_cmpl    ( array_t *a, len, *n, **res)
bool array_diff    ( array_t *a, *b, len, *n, **res)
bool array_isect   ( array_t *a, *b, len, *res)
void array_not     ( array_t *a, len, *res)
void array_or      ( array_t *a, *b, len, *res)
int  array_rewrite (array_t *a, *mask, *rewrite, len)
int  array_x_count ( array_t *a, *mask, len);  # counts number of X bits in positions masked by a 0

array_t  *array_and_a   ( array_t *a, *b, len)
array_t **array_cmpl_a  ( array_t *a, len, *n)
array_t **array_diff_a  ( array_t *a, *b, len, *n)
array_t  *array_isect_a ( array_t *a, *b, len)
array_t  *array_not_a   ( array_t *a, len)
array_t  *array_or_a    ( array_t *a, *b, len)

void array_shift_left  (array_t *a, len, start, shift, bit_val val)
void array_shift_right (array_t *a, len, start, shift, bit_val val)

'''
 * combines a and b into 1, or 3 wc expressions.
 * the results will be save in place in a, or extra.
 * The goal is to generate all wc expressions that are covering a U b. The
 * result will be non-redundant in the sense that the expressions are not subset
 * of each other.
 '''
void array_combine(array_t **_a, **_b, **extra,
                    array_t* mask, len)
int
array_one_bit_subtract (array_t *a, *b, len )

#endif

