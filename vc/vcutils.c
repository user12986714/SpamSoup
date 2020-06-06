#include "vcutils.h"

unsigned long str_hash(unsigned char *str_to_hash, size_t len_str){
    /* This function converts an array of char elements to an unsigned long integer hash.
     * Arguments:
     * str_to_hash shall be an array of char elements to be hashed;
     * len_str shall be a size_t variable with value equal to numbe of elements in str_to_hash.
     * Outcome:
     * An unsigned long integer will be returned as the result. Only the lower 32 bits are significant
     * and other bits are set to 0. */
    unsigned long hash_result = 0;

    for (size_t i = 0; i < len_str; i++){
        hash_result += (hash_result << 16);
        hash_result += (unsigned long)(str_to_hash[i]);
        /* Auto truncate for unsign types, no modulo needed. */
    }

    return (hash_result & MASK_32_BITS);
}
