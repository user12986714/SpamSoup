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
     * but greater than 0 line, output is 1 line. An EOF signal will be sent when output ends. */
    unsigned char *phrase;
    size_t size_phrase = 0;
    ssize_t len_phrase;

    unsigned char *phrase_list[5] = {NULL};
    size_t len_phrase_list[5] = {0};

    unsigned char *catphrase;
    size_t len_catphrase;
    size_t ptr;  /* Pointer used when concatenating phrases. */
    unsigned int not_null_phrase = 0;

    unsigned long hash;

    while ((len_phrase = getline((char **)(&phrase), &size_phrase, stdin)) != -1){
        strip_endl(phrase, &len_phrase);

        free(phrase_list[0]);
        for (unsigned int i = 0; i < 4; i++){
            len_phrase_list[i] = len_phrase_list[i + 1];
            phrase_list[i] = phrase_list[i + 1];
        }

        len_phrase_list[4] = len_phrase;
        phrase_list[4] = malloc((len_phrase + 1) * sizeof(char));
        memcpy(phrase_list[4], phrase, len_phrase * sizeof(char));
        phrase_list[4][len_phrase] = '\0';

        if (phrase_list[0] && len_phrase_list[0]){  /* Double insurance. */
            len_catphrase = 0;
            for (unsigned int i = 0; i < 5; i++){
                len_catphrase += len_phrase_list[i] + 1;
            }
            catphrase = malloc(len_catphrase-- * sizeof(char));

            ptr = 0;
            for (unsigned int i = 0; i < 5; i++){
                memcpy(catphrase + ptr * sizeof(char), phrase_list[i], len_phrase_list[i]);
                ptr += len_phrase_list[i];
                catphrase[ptr++] = '\0';
            }

            hash = str_hash(catphrase, len_catphrase);
            printf("%lu\n", hash);
            
            free(catphrase);
        }
    }

    if (!phrase_list[0]){
        while (!phrase_list[not_null_phrase]){
            not_null_phrase++;
            if (not_null_phrase > 4){
                break;
            }
        }

        if (not_null_phrase < 5){
            len_catphrase = 0;
            for (unsigned i = not_null_phrase; i < 5; i++){
                len_catphrase += len_phrase_list[i] + 1;
            }
            catphrase = malloc(len_catphrase-- * sizeof(char));

            ptr = 0;
            for (unsigned int i = not_null_phrase; i < 5; i++){
                memcpy(catphrase + ptr * sizeof(char), phrase_list[i], len_phrase_list[i]);
                ptr += len_phrase_list[i];
                catphrase[ptr++] = '\0';
            }

            hash = str_hash(catphrase, len_catphrase);
            printf("%lu\n", hash);
            
            free(catphrase);
        }
    }

    for (unsigned int i = 0; i < 5; i++){
        free(phrase_list[i]);
    }
    free(phrase);

    return 0;
}
