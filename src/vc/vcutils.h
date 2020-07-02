#ifndef __VCUTILS_H_INCLUDED__
#define __VCUTILS_H_INCLUDED__

#include <stddef.h>
#include <unistd.h>
#include <inttypes.h>

void strip_endl(unsigned char *str_to_strip, ssize_t *len_str);
uint32_t str_hash(unsigned char *str_to_hash, size_t len_str);

#endif
