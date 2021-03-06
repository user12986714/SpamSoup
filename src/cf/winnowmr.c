#include <stdio.h>
#include <math.h>

#include "cfutils.h"

#define FOLD_TO (67108957)
#define BYTES_PER_RECORD (1)

#ifndef THRES
#define THRES (2147483649)  /* 2 ^ 31 + 1 */
#endif

#ifndef LOG_LEARN_THRES
#define LOG_LEARN_THRES (0.15)
#endif

void winnow_learn_mr(FILE *data_file, uint8_t category){
    /* This function, depending on what category is, adjusts the corresponding
     * counters to the input.
     * If category is 1, or the post is a true positive, those counters are
     * all set to 0;
     * otherwise they are increased by 1.
     * Arguments:
     * data_file shall be a FILE pointer opened as "r+b".
     * category shall be either 1, if is true positive, or 0 otherwise.
     * Outcome:
     * Corresponding counters will be adjusted. */
    uint32_t hash;
    long offset;

    uint8_t current_record;

    while (scanf("%"PRIu32, &hash) != -1){
        offset = BYTES_PER_RECORD * (long)(hash % FOLD_TO);

        fseek(data_file, offset, SEEK_SET);
        fread(&current_record, BYTES_PER_RECORD, 1, data_file);

        if (current_record == 0){
            continue;
        }

        if (category){  /* 'T' */
            current_record = 0;
            fseek(data_file, offset, SEEK_SET);
            fwrite(&current_record, BYTES_PER_RECORD, 1, data_file);
        }
        else{
            if (++current_record){
                fseek(data_file, offset, SEEK_SET);
                fwrite(&current_record, BYTES_PER_RECORD, 1, data_file);
            }
            else{
                fprintf(stderr, "Hash %"PRIu32" weight overflowed.\n", hash);
            }
        }
    }

    return;
}

long double winnow_classify_mr(FILE *data_file){
    /* This function calculates the weight of a post with the data file provided.
     * Arguments:
     * data_file shall be a FILE pointer opened as "rb".
     * Outcome:
     * A long double will be returned representing the confidence of the classification. */
    uint32_t hash;
    long offset;

    uint8_t current_record;
    uint64_t current_score;

    uint64_t total_score;

    total_score = 1;
    while (scanf("%"PRIu32, &hash) != -1){
        offset = BYTES_PER_RECORD * (long)(hash % FOLD_TO);

        fseek(data_file, offset, SEEK_SET);
        fread(&current_record, BYTES_PER_RECORD, 1, data_file);

        if (current_record > 64){
            total_score = -1;  /* Max score; auto wrap for unsigned types */
            break;
        }
        else if (current_record == 0){
            continue;
        }

        current_score = 1 << (current_record - 1);
        if (current_score > (uint64_t)(-1 - total_score)){
            total_score = -1;
            break;
        }

        total_score += current_score;
    }

    /* Negative sign as the larger total_score is, the more likely
     * the post is not true positive, as the learning is reversed. */
    return -log2l((long double)(total_score) / (long double)(THRES));
}

int main(int argc, char *argv[]){
    /* Type 2 executable.
     * Input: list of uint32_t representable integers in base 10.
     * Output: endpoint. */
    long double log_weight;
    FILE *data_file;

    if ((argv[1][0] == 'T') || (argv[1][0] == 'F')){
        data_file = fopen(argv[2], "r+b");
        winnow_learn_mr(data_file, !(argv[1][0] == 'F'));
        printf("%c\n", argv[1][0]);
    }
    else{
        data_file = fopen(argv[2], "rb");
        log_weight = winnow_classify_mr(data_file);
        if ((argv[1][0] == 't') || (argv[1][0] == 'f')){
            if ((log_weight * (1 - 2 * !!(argv[1][0] == 'f'))) < LOG_LEARN_THRES){
                printf("LEARN\n");
            }
            else{
                printf("NOLEARN (%Lf)\n", log_weight);
            }
        }
        else{
            printf("%c (%Lf)\n", ((log_weight > 0) ? 'T' : 'F'), log_weight);
        }
    }

    fclose(data_file);
    return 0;
}
