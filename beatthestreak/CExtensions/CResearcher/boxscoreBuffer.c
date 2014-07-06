/* A cache for remembering the most recently viewed place on team boxscores */
#include "boxscoreBuffer.h" // also imports python.h
#include <stdlib.h> /* exit, EXIT_FAILURE */
#include <stdio.h> /* fprintf, printf, etc */

int bufferYear = 1;
struct boxData *boxHashTable = NULL;        /* pointer to Global Hash Table */
long seekPosUsed = -1L;                     /* for testing. Nonnegative int if buffer used, -1 if never set */

/* *************** Utility functions for hashTable ***********/

/* If a key is not in the table, add it. Otherwise edit the existing
   entry in the hash. Return 0 if successful, else -1 */
int addReplaceBoxscore(char *boxscore, long lastViewedByte, 
    int month, int day) {
    struct boxData *bD;

    // We need to dynamically allocate space for the hash table key, so
    // hash table keys are independent of eachother. 
    char *updateBoxscore = (char *) malloc(strlen(boxscore) + 1);
    if (!updateBoxscore) {
        PyErr_SetString(PyExc_SystemError, "Failed to allocate updateBoxscore on the stack\n");
        return -1;
    } else {
        strcpy(updateBoxscore, boxscore);
    }

    /* Add or Replace the hash element */
    HASH_FIND_STR(boxHashTable, boxscore, bD);
    if (bD == NULL) {
            bD = (struct boxData *) malloc(sizeof(struct boxData));
        if (bD) {
            bD->boxscore = updateBoxscore;
            bD->lastViewedByte = lastViewedByte;
            bD->month = month;
            bD->day = day;
            HASH_ADD_STR( boxHashTable, boxscore, bD);
               /* name of field as parameter? It's a macro thing */
        } else {
            PyErr_SetString(PyExc_SystemError, "Failed to allocate boxData on the stack\n");
            return -1;
        }
    } else {
        bD->lastViewedByte = lastViewedByte;
        bD->month = month;
        bD->day = day;
    }
    return 0;
}

struct boxData *findBoxscore(const char*boxscore) {
    /* Returns a pointer to the boxData with key boxscore if its in the hash table, 
    or NULL if its not in it */
    struct boxData *bD;
    /* HASH_FIND_STR(hashTable, pointer to key, output struct) */

    HASH_FIND_STR( boxHashTable, boxscore, bD);
    return bD;
}

void deleteTable() {
    /* Removes all hash elements from the hash Table and 
       frees up associated memory */
    // printf("delete table called\n");    
    struct boxData *currentBox, *tmp;

    HASH_ITER(hh, boxHashTable, currentBox, tmp) {
        HASH_DEL(boxHashTable, currentBox);     /* delete; users advances to next */
        free((void *)currentBox->boxscore);     /* free the hash table key */
        free(currentBox);                       /* free the pointer */
    }
}
void printHashTable(int printBoxscore) {
    struct boxData *bD;
    char *indent4 = "    ";
    char *indent8 = "        ";
    
    printf("\n********** HASHTABLE *********\n");
    int i = 0;
    for (bD=boxHashTable; bD != NULL; bD=bD->hh.next) {
        i++;
        if (printBoxscore) {
            printf("Item Num: %d: ", i);
            printf("%sboxscore: START%sEND\n%slastViewedByte: %ld\n%sboxscoreAddy: %p\n", 
                indent4, bD->boxscore, indent8, bD->lastViewedByte, 
                indent8, (bD->boxscore));
        }
        else {
            printf("Item Num: %d\n", i);    
            printf(
            "%sboxscore: START%sEND\n%slastViewedByte: %ld\n%smonth: %d\n%sday: %d\n", 
            indent4, bD->boxscore, indent8, bD->lastViewedByte, 
            indent8, bD->month, indent8, bD->day);
        }
    }
}
/* Notes:
    1) HashTable keys must NOT be modified while in use
    2) When declaring the hashtable, you MUST initalize it to NULL
    3) If experiencing errors, check if you are trying to add
       non-unique keys 
    4) structure is never moved or copied once entered into hash table. 
        So can maintain references to it */
