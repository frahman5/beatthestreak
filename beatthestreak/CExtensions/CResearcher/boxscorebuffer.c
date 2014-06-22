#include "uthash.h"
#include <stdlib.h> /* exit, EXIT_FAILURE */
#include <stdio.h>

/* A hashtable with string keys and int values */
struct boxData {
    const char *boxscore;       /* key:  boxscore's filepath as a string */
    int lastViewedByte;         /* value1: last viewed byte on boxscore */
    int month;                  /* value2: month of last date checked */
    int day;                    /* value3: day of last date checked */
    UT_hash_handle hh;          /* makes this struct hashable */
};


int bufferYear = 1;
struct boxData *boxHashTable = NULL;        /* pointer to Global Hash Table */
int seekPosUsed = -1; // for testing

/* *************** Utility functions for hashTable ***********/
/* Add an item to a hash */
void addBoxscore(const char*boxscore, int lastViewedByte, 
    int month, int day) {
    struct boxData *bD;

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
    struct boxData *currentBox, *tmp;

    HASH_ITER(hh, boxHashTable, currentBox, tmp) {
        HASH_DEL(boxHashTable, currentBox);     /* delete; users advances to next */
        free(currentBox);                       /* free the pointer */
    }
}

/* Notes:
    1) HashTable keys must NOT be modified while in use
    2) When declaring the hashtable, you MUST initalize it to NULL
    3) If experiencing errors, check if you are trying to add
       non-unique keys 
    4) structure is never moved or copied once entered into hash table. 
        So can maintain references to it */