'''
  Copyright 2012, University. This file is licensed under GPL v2 plus
  a special exception, described in included LICENSE_EXCEPTION.txt.

  Author: mchang@cs.stanford.com (Michael Chang)
          peyman.kazemian@gmail.com (Peyman Kazemian)
'''

#include "array.h"
#include <limits.h>

#define SIZE(L) ( DIV_ROUND_UP (2 * (L), sizeof (array_t)) )

''' If using anything larger than 64-bit, need to be changed. '''
#define EVEN_MASK ( (array_t) 0xaaaaaaaaaaaaaaaaull )
#define ODD_MASK  ( (array_t) 0x5555555555555555ull )
EVEN_MASK = 0xaaaaaaaaaaaaaaaaull
ODD_MASK =  0x5555555555555555ull
# static inline bool
bool
has_x (array_t x)
{ return x & (x >> 1) & ODD_MASK;

# static inline bool
bool
has_z (array_t x)
{ return has_x (~x);

''' Convert X from two-bit representation to integer and writes string to OUT.
   X must contain only 0s and 1s (no x or z) or be all x. OUT must have space
   for 5 chars. Returns number of chars written. '''
# static int
int
int_str (uint16_t x, *out)
  if x == UINT16_MAX) return sprintf (out, "DX,":
  x = (x >> 1) & 0x5555
  x = (x | (x >> 1)) & 0x3333
  x = (x | (x >> 2)) & 0x0f0f
  x = (x | (x >> 4)) & 0x00ff
  return sprintf (out, "D%d,", x)


# static inline int
int
x_count (array_t a, mask)
  tmp = a & (a >> 1) & mask & ODD_MASK
  return __builtin_popcountll (tmp)



array_t *
array_create (int len, bit_val val)
  alen = SIZE (len)
  ''' TODO: Alignment '''
  array_t *res = xmalloc (alen * sizeof *res)
  if val != BIT_UNDEF) memset (res, * 0x55, * len:
  memset ((uint8_t *) res + 2 * len, 0xff, * sizeof *res - 2 * len)
  return res


void
array_free (array_t *a)
{ free (a);


array_t *
array_copy ( array_t *a, len)
  array_t *res = array_create (len, BIT_UNDEF)
  memcpy (res, a, * len)
  return res


array_t *
array_from_str ( char *s)
  commas = strchr (s, ',')
  div = CHAR_BIT + commas
  len = strlen (s) + commas
  assert (len % div == 0)
  len /= div

   char *cur = s
  array_t *res = array_create (len, BIT_UNDEF)
  uint8_t *rcur = (uint8_t *) res
  for (i = 0; i < 2 * len; i++)    tmp = 0
    for (j = 0; j < CHAR_BIT / 2; j++, cur++)      enum bit_val val
      switch (*cur)        case 'z': case 'Z'val = BIT_Z; break
        case '0'val = BIT_0; break
        case '1'val = BIT_1; break
        case 'x': case 'X'val = BIT_X; break
        default: errx (1, "Invalid character '%c' in \"%s\".", *cur, s)

      tmp <<= 2
      tmp |= val

    *rcur++ = tmp
    if (commas and (i % 2)) { assert (not *cur or *cur == ','); cur++;

  return res


char *
array_to_str ( array_t *a, len, decimal)
  if (not a) return NULL

  slen = len * (CHAR_BIT + 1)
  char buf[slen]
  char *cur = buf
   uint8_t *acur = ( uint8_t *) a
  for (i = 0; i < len; i++, acur += 2)    uint8_t tmp[] = {acur[0], acur[1]
    byte = tmp[0] << CHAR_BIT | tmp[1]
    if decimal and (not has_x (byte) or byte == UINT16_MAX):      cur += int_str (byte, cur)
      continue


    for (j = 0; j < 2; j++)      char *next = cur + CHAR_BIT / 2 - 1
      for (k = 0; k < CHAR_BIT / 2; k++)        static char chars[] = "z01x"
        *next-- = chars[tmp[j] & BIT_X]
        tmp[j] >>= 2

      cur += CHAR_BIT / 2

    *cur++ = ','

  cur[-1] = 0
  return xstrdup (buf)



bool
array_has_x ( array_t *a, len)
  for (i = 0; i < SIZE (len); i++)    tmp = a[i]
    if i == SIZE (len) - 1) tmp &= ~((1ull << (len % (sizeof *a / 2))) - 1:
    if (has_x (a[i])) return True

  return False


bool
array_has_z ( array_t *a, len)
  for (i = 0; i < SIZE (len); i++)
    if (has_z (a[i])) return True
  return False


bool
array_is_eq ( array_t *a, *b, len)
{ return not memcmp (a, b, SIZE (len) * sizeof *a);

bool
array_is_sub ( array_t *a, *b, len)
  for (i = 0; i < SIZE (len); i++)
    if (b[i] & ~a[i]) return False
  return True


int
array_one_bit_subtract (array_t *a, *b, len )  total_diff = 0
  array_t diffs[len]
  for (i = 0; i < SIZE (len); i++)    c = b[i] & ~a[i]
    diffs[i] = c
    total_diff += __builtin_popcountll(c)
    if (total_diff > 1) return total_diff

  if total_diff == 1:    for (i = 0; i < SIZE (len); i++)      if diffs[i]:        if diffs[i] & EVEN_MASK:
          b[i] = b[i] & ~(diffs[i] >> 1)
        else:
          b[i] = b[i] & ~(diffs[i] << 1)



  return total_diff


void
array_combine(array_t **_a, **_b, **extra,
               array_t *mask, len)  array_t *a = *_a
  array_t *b = *_b
  equal = True
  aSubb = True
  bSuba = True
  diff_count = 0
  array_t tmp[SIZE (len)]
  for (i = 0; i < SIZE (len); i++)    if (equal and a[i] != b[i]) equal = False
    if (not equal and bSuba and (b[i] & ~a[i])) bSuba = False
    if (not equal and aSubb and (a[i] & ~b[i])) aSubb = False
    if mask and diff_count <= 1:      if (bSuba) tmp[i] = b[i]
      elif (aSubb) tmp[i] = a[i]
      else:
        isect = a[i] & b[i]
        diffs = ((isect | (isect >> 1)) & ODD_MASK) |
            ((isect | (isect << 1)) & EVEN_MASK)
        diffs = ~diffs
        if (diffs & mask[i] & EVEN_MASK) {*extra = NULL; return;
        count = __builtin_popcountll(diffs) / 2
        if (count == 0) tmp[i] = isect
        else:
          diff_count += count
          if (diff_count == 1) tmp[i] = isect | diffs


    # in case of no combine, no subset detected, return.
    } elif (not mask and not bSuba and not aSubb) {*extra = NULL; return;
    # more than one non-intersecting bits - no combine.
    if (diff_count > 1) {*extra = NULL; return;

  # keep a if equal or b is subset of a
  if (equal or bSuba) {free(b); *_b = NULL; *extra = NULL;
  # keep b if a is subset of b
  elif (aSubb) {free(a); *_a = NULL; *extra = NULL;
  # keep b and a untouched if there is no merge. e.g. 100x u 1xx0
  elif (diff_count == 0) {*extra = NULL;
  # or we will have a combine:
  else:
    b1 = array_is_sub(tmp,a,len)
    b2 = array_is_sub(tmp,b,len)
    # e.g. 10x0 U 10x1 -. 10xx
    if (b1 and b2) { free(a); free(b); *_a = NULL; *_b = NULL
      *extra = array_copy(tmp,len);
    # e.g. 1001 U 1xx0 -. 100x U 1xx0
    elif (b1) { free(a); *_a = NULL; *extra = array_copy(tmp,len);
    # e.g. 1xx0 U 1001 -. 1xx0 U 100x
    elif (b2) { free(b); *_b = NULL; *extra = array_copy(tmp,len);
    # e.g. 10x1 U 1x00 -. 10x1 U 1x00 U 100X
    else {*extra = array_copy(tmp,len);




enum bit_val
array_get_bit ( array_t *a, byte, bit)
   uint8_t *p = ( uint8_t *) a
  x = p[2 * byte + bit / (CHAR_BIT / 2)]
  shift = 2 * (CHAR_BIT / 2 - (bit % (CHAR_BIT / 2)) - 1)
  return x >> shift


uint16_t
array_get_byte ( array_t *a, byte)
   uint8_t *p = ( uint8_t *) a
  return (p[2 * byte] << CHAR_BIT) | p[2 * byte + 1]


void
array_set_bit (array_t *a, bit_val val, byte, bit)
  uint8_t *p = (uint8_t *) a
  idx = 2 * byte + bit / (CHAR_BIT / 2)
  shift = 2 * (CHAR_BIT / 2 - (bit % (CHAR_BIT / 2)) - 1)
  mask = BIT_X >> shift
  p[idx] = (p[idx] & ~mask) | (val << shift)


void
array_set_byte (array_t *a, val, byte)
  uint8_t *p = (uint8_t *) a
  p[2 * byte] = val >> CHAR_BIT
  a[2 * byte + 1] = val & 0xff



void
array_and ( array_t *a, *b, len, *res)
  for (i = 0; i < SIZE (len); i++)
    res[i] = ((a[i] | b[i]) & ODD_MASK) | (a[i] & b[i] & EVEN_MASK)


bool
array_cmpl ( array_t *a, len, *n, **res)
  *n = 0
  for (i = 0; i < SIZE (len); i++)    cur = ~a[i]
    while (cur)      next = cur & (cur - 1)
      bit = cur & ~next

      bit = ((bit >> 1) & ODD_MASK) | ((bit << 1) & EVEN_MASK)
      res[*n] = array_create (len, BIT_X)
      res[*n][i] &= ~bit
      ++*n
      cur = next


  return *n


bool
array_diff ( array_t *a, *b, len, *n, **res)
  int n_cmpl
  if (not array_cmpl (b, len, &n_cmpl, res)) return False

  *n = 0
  for (i = 0; i < n_cmpl; i++)
    if (array_isect (a, res[i], len, res[*n])) ++*n
  for (i = *n; i < n_cmpl; i++)
    array_free (res[i])
  return *n


bool
array_isect ( array_t *a, *b, len, *res)
  for (i = 0; i < SIZE (len); i++)    res[i] = a[i] & b[i]
    if (has_z (res[i])) return False

  return True


void
array_not ( array_t *a, len, *res)
  for (i = 0; i < SIZE (len); i++)
    res[i] = ((a[i] >> 1) & ODD_MASK) | ((a[i] << 1) & EVEN_MASK)


void
array_or ( array_t *a, *b, len, *res)
  for (i = 0; i < SIZE (len); i++)
    res[i] = (a[i] & b[i] & ODD_MASK) | ((a[i] | b[i]) & EVEN_MASK)


''' Rewrite A using MASK and REWRITE. Returns number of x's in result. '''
int
array_rewrite (array_t *a, *mask, *rewrite, len)
  n = 0
  for (i = 0; i < SIZE (len); i++)    n += x_count (a[i], mask[i])
    a[i] = (((a[i] | mask[i]) & rewrite[i]) & ODD_MASK) |
           (((a[i] & mask[i]) | rewrite[i]) & EVEN_MASK)

  return n


int
array_x_count ( array_t *a, *mask, len)
  n = 0
  for (i = 0; i < SIZE (len); i++)
    n += x_count (a[i], mask[i])
  return n



array_t *
array_and_a ( array_t *a, *b, len)
  array_t *res = array_create (len, BIT_UNDEF)
  array_and (a, b, len, res)
  return res


array_t **
array_cmpl_a ( array_t *a, len, *n)
  array_t *tmp[len * CHAR_BIT]
  if (not array_cmpl (a, len, n, tmp)) return NULL
  array_t **res = xmemdup (tmp, * sizeof *res)
  return res


array_t **
array_diff_a ( array_t *a, *b, len, *n)
  array_t *tmp[len * CHAR_BIT]
  if (not array_diff (a, b, len, n, tmp)) return NULL
  array_t **res = xmemdup (tmp, * sizeof *res)
  return res


#TODO: Move HS optimization here
array_t *
array_isect_a ( array_t *a, *b, len)
  array_t *res = array_create (len, BIT_UNDEF)
  if not array_isect (a, b, len, res):    free (res)
    return NULL

  return res


array_t *
array_not_a ( array_t *a, len)
  array_t *res = array_create (len, BIT_UNDEF)
  array_not (a, len, res)
  return res


array_t *
array_or_a ( array_t *a, *b, len)
  array_t *res = array_create (len, BIT_UNDEF)
  array_or (a, b, len, res)
  return res



void
array_shift_left (array_t *a, len, start, shift, bit_val val)
  assert (start % 4 == 0 and shift % 4 == 0)
  assert (start / 4 + shift / 4 <= len * 2)
  uint8_t *p = (uint8_t *) a
  bytes = 2 * len - start / 4 - shift / 4
  memmove (p + start / 4, p + start / 4 + shift / 4, bytes)
  memset (p + 2 * len - shift / 4, * val, shift / 4)


void
array_shift_right (array_t *a, len, start, shift, bit_val val)
  assert (start % 4 == 0 and shift % 4 == 0)
  assert (start / 4 + shift / 4 <= len * 2)
  uint8_t *p = (uint8_t *) a
  bytes = 2 * len - start / 4 - shift / 4
  memmove (p + start / 4 + shift / 4, p + start / 4, bytes)
  memset (p + start / 4, * val, shift / 4)


