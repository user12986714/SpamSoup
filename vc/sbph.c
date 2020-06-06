#include <stdio.h>
#include <stdlib.h>

#include "vcutils.h"

void sbp_hash(unsigned long *sbph_result, unsigned long *hash){
    /* This function converts an array of 5 unsigned long intergers to an array of 16 unsigned long integer hashes.
     * Arguments:
     * sbph_result shall be an array of 16 unsigned long elements;
     * hash shall be an array of 5 unsigned long elements, with all but the lower 32 bits set to 0 and insignificant,
     * that are to be sbp hashed.
     * Outcome:
     * sbph_result will be filled by 16 unsigned long integers as results. For each integer,
     * only the lower 32 bits are significant and other bits are set to 0. */
    unsigned long coef, mask;
    for (unsigned int i = 0; i < 16; i++){
        sbph_result[i] = 2 * hash[0];

        for (unsigned int j = 1; j < 5; j++){
            coef = (1 << j) + 1;
            mask = (i >> (j - 1)) - ((i >> j) << 1);
            sbph_result[i] += mask * coef * hash[j];
        }

        sbph_result[i] &= MASK_32_BITS;
    }

    return;
}

int main(){
    /* This program implements sparse binary polynomial hashing, a hashing algorithm converting a list of phrases to
     * a list of groups of 32 bits integer hashes, with hashes in each group determined by the corresponding
     * phrase and some of its previous phrases.
     * In this implementation, each group contains 16 hashes. The hashes in each group is determined by
     * the corresponding phrase and 4 previous phrases.
     * Input format:
     * Input may consist many lines, with one phrase on each line. An EOF signal shall be sent when input ends.
     * Output format:
     * Output consists many lines, with one hash on each line. Each hash is represented by a base 10 integer.
     * The number of lines in the output is 16 times of that of input. An EOF signal will be sent when output ends. */
    unsigned char *phrase;
    size_t size_phrase = 0;
    ssize_t len_phrase;
    unsigned long hash_r[5] = {0};
    unsigned long sbph_r[16];

    while ((len_phrase = getline((char **)(&phrase), &size_phrase, stdin)) != -1){
        while ((phrase[len_phrase - 1] == '\r') || (phrase[len_phrase - 1] == '\n')){
            if (len_phrase > 1){
                len_phrase--;
            }
            else{
                break;
            }
        }
        hash_r[4] = hash_r[3];
        hash_r[3] = hash_r[2];
        hash_r[2] = hash_r[1];
        hash_r[1] = hash_r[0];

        hash_r[0] = str_hash(phrase, (size_t)(len_phrase));

        sbp_hash(sbph_r, hash_r);
        for (unsigned int i = 0; i < 16; i++){
            printf("%lu\n", sbph_r[i]);
        }
    }

    free(phrase);

    return 0;
}
