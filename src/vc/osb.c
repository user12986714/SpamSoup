#include <stdio.h>
#include <stdlib.h>

#include "vcutils.h"

/* !!! Notice !!!
 * Please don't change the following constant without good reasons.
 * If changed, some training effort will be less effective;
 * at the same time, all documentation need to be changed correspondingly. */
#define PHRASE_PER_GROUP (5)

int main(){
    /* Type 0.
     * Input: list of strings generated by a tokenizer.
     * Output: list of uint32_t representable integers in base 10.
     * The i-th line of input will generate ((i > 3) ? i : (16)) lines of output,
     * with i starting from 0. */
    unsigned char *phrase = NULL;
    size_t size_phrase = 0;
    ssize_t len_phrase;
    uint32_t hash_r[PHRASE_PER_GROUP] = {0};
    uint32_t osb_r;

    size_t missing_phrases = PHRASE_PER_GROUP;

    while ((len_phrase = getline((char **)(&phrase), &size_phrase, stdin)) != -1){
        strip_endl(phrase, &len_phrase);

        for (size_t i = PHRASE_PER_GROUP - 1; i > 0; i--){
            hash_r[i] = hash_r[i - 1];
        }

        hash_r[0] = str_hash(phrase, (size_t)(len_phrase));

        if (missing_phrases){
            missing_phrases--;
        }

        for (size_t i = 1; i < (PHRASE_PER_GROUP - missing_phrases); i++){
            osb_r = (hash_r[0] << 1) + (hash_r[i] << i) + hash_r[i];
            printf("%"PRIu32"\n", osb_r);
        }
    }

    free(phrase);

    return 0;
}
