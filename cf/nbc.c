#include <stdio.h>
#include <math.h>

#include "cfutils.h"

/* !!! Notice !!!
 * If the following constant is changed, it must be a prime.
 * At the same time, all learning data for this program need to be migrated. */
#define FOLD_TO 8388617

/* !!!!!!! IMPORTANT !!!!!!!
 * The following two constants are NOT TO BE CHANGED without original developer's review.
 * Run a git blame and find out who is responsible for this constant value.
 * Bugs guaranteed for failures in following this advice. */
#define BYTES_PER_RECORD 4
#define SAMPLE_COUNTER_BYTES 8

void bayes_learn(FILE *data_file, char category){
    /* This function increases the counter, corresponding to the category, of hashes
     * inputted from stdin in the specified data file.
     * Arguments:
     * data_file shall be a FILE pointer opened as "r+b".
     * category shall be a char and equal to either 'T' or 'F'.
     * Outcome:
     * The corresponding counter will be increased. */
    unsigned long hash;
    long offset, sc_offset;
    uint32_t hash_counter;
    uint64_t sample_counter;

    sc_offset = 2 * BYTES_PER_RECORD * (long)(FOLD_TO);
    sc_offset += (category == 'T') ? 0 : SAMPLE_COUNTER_BYTES;

    fseek(data_file, sc_offset, SEEK_SET);
    fread(&sample_counter, SAMPLE_COUNTER_BYTES, 1, data_file);

    while (scanf("%lu", &hash) != -1){
        offset = 2 * BYTES_PER_RECORD * (long)(hash % FOLD_TO);
        offset += (category == 'T') ? 0 : BYTES_PER_RECORD;

        fseek(data_file, offset, SEEK_SET);
        fread(&hash_counter, BYTES_PER_RECORD, 1, data_file);

        hash_counter++;
        if ((uint32_t)(hash_counter + 1)){
            sample_counter++;
            if (!(uint64_t)(sample_counter + 1)){
                fprintf(stderr, "Sample %c counter overflowed.\n", category);
                break;  /* No more learning can happen. */
            }

            fseek(data_file, offset, SEEK_SET);
            fwrite(&hash_counter, BYTES_PER_RECORD, 1, data_file);
        }
        else{
            fprintf(stderr, "Hash %lu as %c counter overflowed.\n", hash, category);
        }
    }

    if (!(uint64_t)(sample_counter + 1)){
        sample_counter--;
    }
    fseek(data_file, sc_offset, SEEK_SET);
    fwrite(&sample_counter, SAMPLE_COUNTER_BYTES, 1, data_file);

    return;
}

char bayes_classify(FILE *data_file){
    /* This function performs Bayesian classification on the group of hashes inputted
     * from stdin, using the learned data in the specified dat file.
     * Arguments:
     * data_file shall be a FILE pointer opened as "rb".
     * Outcome:
     * A char will be returned that is either 'T' or 'F', representing true or false
     * positive. */
    unsigned long hash;
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

    while (scanf("%lu", &hash) != -1){
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

    fprintf(stderr, "Log spam ratio: %Lf", log_posterior_ratio);
    if (log_posterior_ratio > 0){
        return 'T';
    }
    else{
        return 'F';
    }
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
     * Output consist one line, with one char on each line. The char is either 'T' or 'F'.
     * Arguments:
     * Two arguments shall be passed via command line.
     * The first shall be either "--learn" or "--classify".
     * If "--learn" is passed, it shall be either "--learn=T" or "--learn=F". "--learn=T" instructs
     * this program to learn the group of hashes as a true postive, and "--learn=F" instructs this
     * program to learn the group of hashes as a false positive. In both case, the output will be
     * the same as what this program is instructed to learn. "--classify" instructs this program to
     * classify the group of hashes as either true positive or false positive. The output will be
     * what this program classifies the group of hashes.
     * The second shall be "--data".
     * "--data" shall be in the format "--data=/path/to/data/file", where "/path/to/data/file" is
     * the path, absolute or relative, to a valid data file this program uses to store learning
     * result. This arguments instruct this program what data file to use for learning and classfying. */
    char category;
    FILE *data_file;

    /* Following magic numbers are from program specifiation. */
    if (starts_with("--learn", argv[1])){
        category = argv[1][8];
        data_file = fopen(&(argv[2][7]), "r+b");
        bayes_learn(data_file, category);
    }
    else{
        data_file = fopen(&(argv[2][7]), "rb");
        category = bayes_classify(data_file);
    }

    printf("%c\n", category);

    fclose(data_file);
    return 0;
}
