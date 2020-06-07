#include "vcutils.h"

void strip_endl(unsigned char *str_to_strip, size_t *len_str){
    /* This function strips trailing line end chars.
     * Arguments:
     * str_to_strip shall be an array of char elements to be stripped;
     * len_str shall be a size_t variable with value equal to number of elements in str_to_strip.
     * Outcome:
     * len_str will be modyfied to the value equal to number of elements in stripped str_to_strip.
     * Note that str_to_strip will not change by calling this function. */
    while ((str_to_strip[*len_str - 1] == '\r') || (str_to_strip[*len_str - 1] == '\n')){
        /* Operator *, -- and ! are of the same precedence, but at that level of precedence
         * the associativity is right-to-left. */
        (*len_str)--;
        if (!*len_str){
            break;
        }
    }

    return;
}

unsigned long str_hash(unsigned char *str_to_hash, size_t len_str){
    /* This function converts an array of char elements to an unsigned long integer hash.
     * Arguments:
     * str_to_hash shall be an array of char elements to be hashed;
     * len_str shall be a size_t variable with value equal to number of elements in str_to_hash.
     * Outcome:
     * An unsigned long integer will be returned as the result. Only the lower 32 bits are significant
     * and other bits are set to 0. */
    unsigned long hash_result = 0;

    for (size_t i = 0; i < len_str; i++){
        /* Note: (2 ^ 16 + 1) was picked simply because it is a prime, with no other reasons. */
        hash_result += (hash_result << 16);  /* hash_result *= (2 ^ 16 + 1) */
        hash_result += (unsigned long)(str_to_hash[i]);
        /* Auto truncate for unsign types, no modulo needed. */
    }

    return (hash_result & MASK_32_BITS);
}
