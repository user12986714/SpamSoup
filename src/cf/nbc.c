#include <stdio.h>
#include <math.h>

#include "cfutils.h"

/* !!! Notice !!!
 * If the following constant is changed, it must be a prime.
 * At the same time, all learning data for this program need to be migrated. */
#define FOLD_TO (8388617)

/* !!!!!!! IMPORTANT !!!!!!!
 * The following two constants are NOT TO BE CHANGED without original developer's review.
 * Run a git blame and find out who is responsible for this constant value.
 * Bugs guaranteed for failures in following this advice. */
#define BYTES_PER_RECORD (4)
#define SAMPLE_COUNTER_BYTES (8)

void bayes_learn(FILE *data_file, uint8_t category){
    /* This function increases the counter, corresponding to the category, of hashes
     * inputted from stdin in the specified data file.
     * Arguments:
     * data_file shall be a FILE pointer opened as "r+b".
     * category shall be a char and equal to either 'T' or 'F'.
     * Outcome:
     * The corresponding counter will be increased. */
    uint32_t hash;
    long offset, sc_offset;
    uint32_t hash_counter;
    uint64_t sample_counter;

    sc_offset = 2 * BYTES_PER_RECORD * (long)(FOLD_TO);
    sc_offset += category * SAMPLE_COUNTER_BYTES;

    fseek(data_file, sc_offset, SEEK_SET);
    fread(&sample_counter, SAMPLE_COUNTER_BYTES, 1, data_file);

    while (scanf("%"PRIu32, &hash) != -1){
        offset = 2 * BYTES_PER_RECORD * (long)(hash % FOLD_TO);
        offset += category * BYTES_PER_RECORD;

        fseek(data_file, offset, SEEK_SET);
        fread(&hash_counter, BYTES_PER_RECORD, 1, data_file);

        hash_counter++;
        if ((uint32_t)(hash_counter + 1)){
            sample_counter++;
            if (!(uint64_t)(sample_counter + 1)){
                fprintf(stderr, "Sample %c counter overflowed.\n", (category ? 'F' : 'T'));
                break;  /* No more learning can happen. */
            }

            fseek(data_file, offset, SEEK_SET);
            fwrite(&hash_counter, BYTES_PER_RECORD, 1, data_file);
        }
        else{
            fprintf(stderr, "Hash %"PRIu32" as %c counter overflowed.\n", hash, (category ? 'F' : 'T'));
        }
    }

    if (!(uint64_t)(sample_counter + 1)){
        sample_counter--;
    }
    fseek(data_file, sc_offset, SEEK_SET);
    fwrite(&sample_counter, SAMPLE_COUNTER_BYTES, 1, data_file);

    return;
}

long double bayes_classify(FILE *data_file){
    /* This function performs Bayesian classification on the group of hashes inputted
     * from stdin, using the learned data in the specified dat file.
     * Arguments:
     * data_file shall be a FILE pointer opened as "rb".
     * Outcome:
     * A char will be returned that is either 'T' or 'F', representing true or false
     * positive. */
    uint32_t hash;
    long offset;

    uint32_t tp_count, fp_count;
    long double log_tp_count, log_fp_count;

    uint64_t sample_tp, sample_fp;
    long double log_sample_tp, log_sample_fp;
    long double log_sample_bias;

    long double log_posterior_ratio;

    offset = 2 * BYTES_PER_RECORD * (long)(FOLD_TO);

    fseek(data_file, offset, SEEK_SET);
    fread(&sample_tp, SAMPLE_COUNTER_BYTES, 1, data_file);
    fread(&sample_fp, SAMPLE_COUNTER_BYTES, 1, data_file);

    sample_tp++;
    sample_fp++;

    log_sample_tp = log2l((long double)(sample_tp));
    log_sample_fp = log2l((long double)(sample_fp));

    log_sample_bias = log_sample_tp - log_sample_fp;

/* Handle special prior bias macro. */
#ifdef LOG_PRIOR_BIAS
    log_posterior_ratio = LOG_PRIOR_BIAS;
#else
    log_posterior_ratio = log_sample_bias;
#endif

    while (scanf("%"PRIu32, &hash) != -1){
        offset = 2 * BYTES_PER_RECORD * (long)(hash % FOLD_TO);

        fseek(data_file, offset, SEEK_SET);
        fread(&tp_count, BYTES_PER_RECORD, 1, data_file);
        fread(&fp_count, BYTES_PER_RECORD, 1, data_file);

        tp_count++;
        fp_count++;

        log_tp_count = log2l(tp_count);
        log_fp_count = log2l(fp_count);

        log_posterior_ratio += log_tp_count - log_fp_count - log_sample_bias;
    }

    return log_posterior_ratio;
}

int main(int argc, char *argv[]){
    /* This program implements naive Bayesian classifier, a classification algorithm classifying
     * a group of hash to certain categories.
     * In this implementation, a group of hash will be classified as either true positive or
     * false positive.
     * Input format:
     * Input may consist many lines, with one hash on each line. Each hash shall be represented
     * by a base 10 integer, and shall be in the range [0, 2 ^ 32 - 1].
     * An EOF signal shall be sent when input ends.
     * Output format:
     * Output consist one line.
     * If the classifier is learning, the format is "%c". "%c" is 'T' if the post is learned as
     * true positive, or 'F' otherwise.
     * If the classifier is classifying, the format "%c (%Lf)". "%c" is 'T' if the post is classified
     * as true positive, or 'F' otherwise. "%Lf" is a long double equal to the base 2 logarithm
     * of the fraction true positive probability over false positive probability.
     * Arguments:
     * Two arguments shall be passed via command line.
     * The first shall be a single character.
     * 'T' instructs this program to learn the group of hashes as a true postive, and 'F' instructs this
     * program to learn the group of hashes as a false positive. In both case, the output will be the
     * same as what this program is instructed to learn. Any other character instructs this program to
     * classify the group of hashes as either true positive or false positive. The output will be
     * what this program classifies the group of hashes.
     * The second shall be a string to the path of the data file, absolute or relative, which will be used
     * to store learning result or as the data for classifying. */
    long double log_posterior_ratio;
    FILE *data_file;

    if ((argv[1][0] == 'T') || (argv[1][0] == 'F')){
        data_file = fopen(argv[2], "r+b");
        bayes_learn(data_file, !!(argv[1][0] == 'F'));  /* Not a typo: 0 for T, 1 for F */
        printf("%c\n", argv[1][0]);
    }
    else{
        data_file = fopen(argv[2], "rb");
        log_posterior_ratio = bayes_classify(data_file);
        printf("%c (%Lf)\n", ((log_posterior_ratio > 0) ? 'T' : 'F'), log_posterior_ratio);
    }

    fclose(data_file);
    return 0;
}
