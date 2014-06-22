#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h> /* exit */

#include "crhelper.h"
#include "boxscoreBuffer.h"

#define MAXLINE 80


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

int _search_boxscore(FILE *fp, char **foundIt, char *search, char *boxscore) {
    /* Searches file fp for string search and stores the first occurence of
    it and the remainder of the line in *foundIt. Puts "\0" in foundIt if 
    it was not found 

    Returns if successful and 0 otherwise*/

    int startSeekPos;
    if (isdigit(search[0])) { // indicates its a date search
        startSeekPos = 0;
        // Go to last viewed place on team's boxscore
        char bufferYearString[5];
        sprintf(bufferYearString, "%d", bufferYear);   
        if (strstr(search, bufferYearString)){ // if bufferYear in search
            struct boxData *bD = findBoxscore(boxscore);
            if (bD) {// is the boxscore in the buffer?
            }
        }

    }
    char line[MAXLINE]; 
    char lineCheck[MAXLINE];

    fgets(line, MAXLINE, fp);
    while (strstr(line, search) == NULL) {
        strcpy(lineCheck, line);
        fgets(line, MAXLINE, fp);
        if (strcmp(line, lineCheck) == 0) { 
            return 0;
        }
    }
    *foundIt = strstr(line, search);
    return 1;
}