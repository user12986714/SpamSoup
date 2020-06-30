#include <string.h>

#include "cfutils.h"

int starts_with(char *pattern, char *target){
    /* This function decides whether char array target starts with char array pattern.
     * Arguments:
     * pattern shall be an array of char and null terminated.
     * target shall be an array of char and null terminated.
     * Both array shall not contain '\0' that is not the termination char.
     * Outcome:
     * An integer is returned. If target starts with pattern, 1 is returned. Otherwise
     * 0 is returned. */
    size_t len_pattern = strlen(pattern);

    if (strlen(target) < len_pattern){
        return 0;
    }

    for (size_t i = 0; i < len_pattern; i++){
        if (target[i] != pattern[i]){
            return 0;
        }
    }

    return 1;
}
