#include <stdio.h>
#include <stdlib.h>

#include "vcutils.h"

/* !!!!! Warning !!!!!
 * Please don't change the following two constants unless absolutely necessary.
 * If ever changed, they must satisfy the relation 2 ^ (PHRASE_PER_GROUP - 1) = OUTPUT_HASH_PER_GROUP.
 * At the same time, all documentation need to be changed correspondingly as well,
 * and all training effort will be destroyed. */
#define PHRASE_PER_GROUP (5)
#define OUTPUT_HASH_PER_GROUP (16)

void sbp_hash_mh(uint32_t *sbph_result, uint32_t *hashes){
    /* This function converts an array of 5 uint32_t intergers to an array of 16 uint32_t integer hashes.
     * Arguments:
     * sbph_result shall be an array of 16 uint32_t elements;
     * hash shall be an array of 5 uint32_t elements, with all but the lower 32 bits set to 0 and insignificant,
     * that are to be sbp hashed.
     * Outcome:
     * sbph_result will be filled by 16 uint32_t integers as results. For each integer,
     * only the lower 32 bits are significant and other bits are set to 0. */
    uint32_t coef, mask;

    for (size_t i = 0; i < OUTPUT_HASH_PER_GROUP; i++){
        sbph_result[i] = hashes[0] << 1;  /* The least term is always significant. */

        for (size_t j = 1; j < PHRASE_PER_GROUP; j++){
            coef = (1 << j) + 1;
            mask = i & (1 << (j - 1));
            sbph_result[i] += mask * coef * hashes[j];
        }
    }

    return;
}

int main(){
    /* Type 0.
     * Input: list of strings generated by a tokenizer.
     * Output: list of uint32_t representable integers in base 10.
     * The i-th line of input will generate ((i > 3) ? (2 ^ i) : (16))
     * lines of output, with i starting from 0. */
    unsigned char *phrase = NULL;
    size_t size_phrase = 0;
    ssize_t len_phrase;
    uint32_t hash_r[PHRASE_PER_GROUP] = {0};
    uint32_t sbph_r[OUTPUT_HASH_PER_GROUP];

    size_t missing_phrases = PHRASE_PER_GROUP, avai_hashes;

    while ((len_phrase = getline((char **)(&phrase), &size_phrase, stdin)) != -1){
        strip_endl(phrase, &len_phrase);

        for (size_t i = PHRASE_PER_GROUP - 1; i > 0; i--){
            hash_r[i] = hash_r[i - 1];
        }

        hash_r[0] = str_hash(phrase, (size_t)(len_phrase));
        sbp_hash_mh(sbph_r, hash_r);

        if (missing_phrases){
            avai_hashes = 1 << (PHRASE_PER_GROUP - missing_phrases);
            missing_phrases--;
        }

        for (size_t i = 0; i < avai_hashes; i++){
            printf("%"PRIu32"\n", sbph_r[i]);
        }
    }

    free(phrase);

    return 0;
}
