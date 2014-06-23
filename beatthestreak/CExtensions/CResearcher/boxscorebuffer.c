#include "boxscorebuffer.h"
#include <stdlib.h> /* exit, EXIT_FAILURE */
#include <stdio.h>

int bufferYear = 1;
struct boxData *boxHashTable = NULL;        /* pointer to Global Hash Table */
long seekPosUsed = -1L;           /* for testing. Nonnegative int if buffer used, -1 if never set */

/* *************** Utility functions for hashTable ***********/
/* If a key is not in the table, add it. Otherwise edit the existing
   entry in the hash */
void addReplaceBoxscore(const char*boxscore, long lastViewedByte, 
    int month, int day) {
    struct boxData *bD;

    HASH_FIND_STR(boxHashTable, boxscore, bD);
    if (bD == NULL) {
            bD = malloc(sizeof(struct boxData));
        if (bD) {
            bD->boxscore = boxscore;
            bD->lastViewedByte = lastViewedByte;
            bD->month = month;
            bD->day = day;
            /* HASH_ADD_STR(hashTable, nameOfKeyField, pointertoStructAdded) */
            HASH_ADD_STR( boxHashTable, boxscore, bD);
               /* name of field as parameter? It's a macro thing */
        } else {
            printf("bD allocation failed\n");
            exit(EXIT_FAILURE);
        }
    } else {
        bD->lastViewedByte = lastViewedByte;
        bD->month = month;
        bD->day = day;
    }
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
    struct boxData *currentBox, *tmp;

    HASH_ITER(hh, boxHashTable, currentBox, tmp) {
        HASH_DEL(boxHashTable, currentBox);     /* delete; users advances to next */
        free(currentBox);                       /* free the pointer */
    }
}
void printHashTable() {
    struct boxData *bD;
    char *indent4 = "    ";
    char *indent8 = "        ";
    
    printf("\n********** HASHTABLE *********\n");
    int i = 0;
    for (bD=boxHashTable; bD != NULL; bD=bD->hh.next) {
        i++;
        printf("Item Num: %d\n", i);
        printf(
            "%sboxscore: START%sEND\n%slastViewedByte: %ld\n%smonth: %d\n%sday: %d\n", 
            indent4, bD->boxscore, indent8, bD->lastViewedByte, 
            indent8, bD->month, indent8, bD->day);
    }
}
/* Notes:
    1) HashTable keys must NOT be modified while in use
    2) When declaring the hashtable, you MUST initalize it to NULL
    3) If experiencing errors, check if you are trying to add
       non-unique keys 
    4) structure is never moved or copied once entered into hash table. 
        So can maintain references to it */