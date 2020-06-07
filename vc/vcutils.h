#ifndef __VCUTILS_H_INCLUDED__
#define __VCUTILS_H_INCLUDED__

#include <stddef.h>

#define MASK_32_BITS 4294967295

void strip_endl(unsigned char *str_to_strip, size_t *len_str);
unsigned long str_hash(unsigned char *str_to_hash, size_t len_str);

#endif
