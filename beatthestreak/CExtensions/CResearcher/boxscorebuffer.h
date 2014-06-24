#include "uthash.h"

/************ Structs and Functions for Hash Table and Buffer *********/
/* A hashtable with string keys and int values */
struct boxData {
    const char *boxscore;       /* key:  boxscore's filepath as a string */
    long lastViewedByte;         /* value1: last viewed byte on boxscore */
    int month;                  /* value2: month of last date checked */
    int day;                    /* value3: day of last date checked */
    UT_hash_handle hh;          /* makes this struct hashable */
};

/* Global boxscoreBuffer */
extern int bufferYear; /* year for which we are maintaining a buffer */
extern struct boxData *boxHashTable; /* hash table for the year */
    // indicator variable for testing
extern long seekPosUsed;

/* Add or edit an item to a hash */
int addReplaceBoxscore(char* boxscore, long lastViewedByte, 
    int month, int day);
/* Retrieve an item from the has */
struct boxData *findBoxscore(const char*boxscore);
/* Delete the entirety of the hash table */
void deleteTable();
/* print the contents of the hash table -- for debugging */
void printHashTable(int printBoxscore) ;