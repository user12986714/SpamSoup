#include <stdio.h>
#include <stdlib.h>

#include "vcutils.h"

/* !!! Notice !!!
 * Please don't change the following constant without good reasons.
 * If changed, some training effort will be less effective;
 * at the same time, all documentation need to be changed correspondingly. */
#define PHRASE_PER_GROUP (5)

int main(){
    /* This program implements orthogonal sparse binary hashing, a hashing algorithm converting a list of phrases to
     * a list of groups of 32 bits integer hashes, with hashes in each group determined by the corresponding
     * phrase and some of its previous phrase.
     * In this implementation, each group contains 4 hashes. The hashes in each group is determined by
     * the corresponding phrase and 4 previous phrases.
     * Input format:
     * Input may consist many lines, with one phrase on each line. An EOF signal shall be sent when input ends.
     * Output format:
     * Output consists many lines, with one hash on each line. Each hasah is represented by a base 10 interger.
     * For first four lines of input, there will be i - 1 output lines for i-th input line.
     * For later lines, there will be 4 output lines for each input line. */
    unsigned char *phrase;
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
