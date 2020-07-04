#include <stdio.h>
#include <stdlib.h>

#include "vcutils.h"

/* !!!!! Warning !!!!!
 * Please don't change the following two constants unless absolutely necessary.
 * If ever changed, they must satisfy the relation 2 ^ (PHRASE_PER_GROUP - 1) = OUTPUT_HASH_PER_GROUP.
 * At the same time, all documentation need to be changed correspondingly as well,
 * and all training effort will be destroyed. */
#define PHRASE_PER_GROUP 5
#define OUTPUT_HASH_PER_GROUP 16

void sbp_hash(unsigned long *sbph_result, unsigned long *hashes){
    /* This function converts an array of 5 unsigned long intergers to an array of 16 unsigned long integer hashes.
     * Arguments:
     * sbph_result shall be an array of 16 unsigned long elements;
     * hash shall be an array of 5 unsigned long elements, with all but the lower 32 bits set to 0 and insignificant,
     * that are to be sbp hashed.
     * Outcome:
     * sbph_result will be filled by 16 unsigned long integers as results. For each integer,
     * only the lower 32 bits are significant and other bits are set to 0. */
    unsigned long coef, mask;

    for (size_t i = 0; i < OUTPUT_HASH_PER_GROUP; i++){
        sbph_result[i] = 2 * hashes[0];  /* The least term is always significant. */

        for (size_t j = 1; j < PHRASE_PER_GROUP; j++){
            coef = (1 << j) + 1;
            mask = i & (1 << (j - 1));
            sbph_result[i] += mask * coef * hashes[j];
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
     * For first four lines of input, there will be 2 ^ (i - 1) output lines for i-th input line.
     * For later lines, there will be 16 output lines for each input line. */
    unsigned char *phrase = NULL;
    size_t size_phrase = 0;
    ssize_t len_phrase;
    unsigned long hash_r[PHRASE_PER_GROUP] = {0};
    unsigned long sbph_r[OUTPUT_HASH_PER_GROUP];

    size_t missing_phrases = PHRASE_PER_GROUP, avai_hashes;

    while ((len_phrase = getline((char **)(&phrase), &size_phrase, stdin)) != -1){
        strip_endl(phrase, &len_phrase);

        for (size_t i = PHRASE_PER_GROUP - 1; i > 0; i--){
            hash_r[i] = hash_r[i - 1];
        }

        hash_r[0] = str_hash(phrase, (size_t)(len_phrase));
        sbp_hash(sbph_r, hash_r);

        if (missing_phrases){
            avai_hashes = 1 << (PHRASE_PER_GROUP - missing_phrases);
            missing_phrases--;
        }

        for (size_t i = 0; i < avai_hashes; i++){
            printf("%lu\n", sbph_r[i]);
        }
    }

    free(phrase);

    return 0;
}
