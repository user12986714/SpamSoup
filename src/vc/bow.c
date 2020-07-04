#include <stdio.h>
#include <stdlib.h>

#include "vcutils.h"

int main(){
    /* This program implements bag-of-word hashing, a hashing algorithm converting a list of phrases to
     * a list of 32 bits integer hashes, with each hash determined by the corresponding phrase.
     * Input format:
     * Input may consist many lines, with one phrase on each line. An EOF signal shall be sent when input ends.
     * Output format:
     * Output consists many lines, with one hash on each line. Each hash is represented by a base 10 integer.
     * The number of lines in the output is the same as that of input. An EOF signal will be sent when output ends. */
    unsigned char *phrase = NULL;
    size_t size_phrase = 0;
    ssize_t len_phrase;
    uint32_t hash_result;

    while ((len_phrase = getline((char **)(&phrase), &size_phrase, stdin)) != -1){
        strip_endl(phrase, &len_phrase);

        hash_result = str_hash(phrase, (size_t)(len_phrase));

        printf("%"PRIu32"\n", hash_result);
    }

    free(phrase);

    return 0;
}
