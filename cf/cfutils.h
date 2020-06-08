#ifndef __CFUTILS_H_INCLUDED__
#define __CFUTILS_H_INCLUDED__

#include <sys/types.h>
#include <stdint.h>
#include <stddef.h>
#include <unistd.h>

/* ! Note !
 * If the following constant is changed, it must be greater than 1.
 * Also note that this constant should be cast to long double. */
#define LOGISTIC_COEF ((long double)(1.05))

int starts_with(char *pattern, char *target);
long double logistic(unsigned long long x);

#endif
