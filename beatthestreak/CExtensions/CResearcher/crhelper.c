#include <stdio.h>
#include <stdlib.h>
#include "crhelper.h"
#include <string.h>
// #include "python.h"
#define MAXLINE 130

int get_third_num_in_string(char *bsline) {
    /* char *string -> int *num
       Returns the the third int in the string bsline. Assumes bslines has
       at least 3 numbers in it. Helper function for finish_did_get_hit

       If three numbers not found in string, returns -1 

       Ints are only counted if there are followed by
       white space. e.g: 2 is counted but 2b is not. */

    int numNums = 0;
    char num[3]; // handles 1-2two digits number strings e.g 57, 5

    while (bsline++ != '\0') {
        // scroll until we see a digit
        while ((bsline[0] < 48) || (bsline[0] > 57)) { bsline++; } 

        // get the number (or e.g something like 2b) into num
        int i = 0;
        while ((bsline[0] >= 48) & (bsline[0] <=57)) {
            num[i++] = bsline[0];
            bsline++;
        }
        num[i] = '\0'; /* sentinel */

        /* If num is actually a number, increment numNum */
        if (bsline[0] == ' ') { numNums++; }
        
        // If it's the third number, then return it as an int
        if (numNums == 3) { return atoi(num); }
        }
    printf("Reached the end of the input string and did not find three numbers!\n");
    return -1; // function should always return a positive value
}

void _search_boxscore(FILE *fp, char **foundIt, char *search) {
    printf("*********NEW CALL***********\n");
    char line[MAXLINE]; 
    char lineCheck[MAXLINE];

    fgets(line, MAXLINE, fp);
    while (strstr(line, search) == NULL) {
        strcpy(lineCheck, line);
        fgets(line, MAXLINE, fp);
        printf("next line: %s", line);
        if (strcmp(line, lineCheck) == 0) {
            printf("END OF FILE..\n");
            *foundIt = "\0";
        }
    }
    *foundIt = strstr(line, search);
    printf("Reached end of function, here's foundIt: %sEND\n", *foundIt);
}