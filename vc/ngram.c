#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "vcutils.h"

int main(){
    /* This program implements ngram, a hashing algorithm converting a list of phrase to
     * a list of 32 bits integer hashes, with each hash determined by the corresponding phrase
     * and some of its previous phrases.
     * In this implementation, each hash is determined by the corresponding phrase and 4 previous phrases.
     * Input format:
     * Input may consist many lines, with one phrase on each line. An EOF signal shall be sent when inputs ends.
     * Output format:
     * Output consists many lines, with one hash on each line. Each hash is represented by a base 10 integer.
     * The number of lines in the output is 4 lines less than that of input. If input is less that 5 lines
     * but greater than 0 line, output is 1 line.
     * An EOF signal will be sent when output ends. */
    unsigned char *phrase;
    size_t size_phrase = 0;
    ssize_t len_phrase;

    unsigned char *phrases[5] = {NULL};
    size_t len_phrases[5] = {0};

    unsigned char *catphrase;
    size_t len_catphrase;
    size_t ptr;
    unsigned int not_null_phrase = 4;

    unsigned long hash;

    while ((len_phrase = getline((char **)(&phrase), &size_phrase, stdin)) != -1){
        strip_endl(phrase, &len_phrase);

        free(phrases[4]);
        for (unsigned int i = 4; i > 0; i--){
            len_phrases[i] = len_phrases[i - 1];
            phrases[i] = phrases[i - 1];
        }

        len_phrases[0] = len_phrase;
        phrases[0] = malloc((len_phrase + 1) * sizeof(char));
        memcpy(phrases[0], phrase, len_phrase * sizeof(char));
        phrases[0][len_phrase] = '\0';

        if (phrases[4] && len_phrases[4]){  /* Double insurance. */
            ptr = 0;
            /* Additional 4 char for inter-phrase char '\0'. */
            len_catphrase = len_phrases[0] + len_phrases[1] + len_phrases[2] + len_phrases[3] + len_phrases[4] + 4;
            catphrase = malloc((len_catphrase + 1) * sizeof(char));

            for (unsigned int i = 0; i < 5; i++){
                memcpy(catphrase + ptr * sizeof(char), phrases[i], len_phrases[i]);
                ptr += len_phrases[i];
                catphrase[ptr++] = '\0';
            }

            hash = str_hash(catphrase, len_catphrase);
            printf("%lu\n", hash);
            
            free(catphrase);
        }
    }

    if (!phrase[4]){
        while (!phrases[not_null_phrase]){
            not_null_phrase--;
            if (not_null_phrase < 0){
                break;
            }
        }

        if (++not_null_phrase > 0){
            len_catphrase = len_phrases[0] + 1;
            for (unsigned i = 1; i < not_null_phrase; i++){
                len_catphrase += len_phrases[i] + 1;
            }

            for (unsigned int i = 0; i < not_null_phrase; i++){
                memcpy(catphrase + ptr * sizeof(char), phrases[i], len_phrases[i]);
                ptr += len_phrases[i];
                catphrase[ptr++] = '\0';
            }

            hash = str_hash(catphrase, len_catphrase);
            printf("%lu\n", hash);
            
            free(catphrase);
        }
    }

    for (unsigned int i = 0; i < 5; i++){
        free(phrases[i]);
    }
    free(phrase);

    return 0;
}
