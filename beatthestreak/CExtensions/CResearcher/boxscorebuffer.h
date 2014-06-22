#include "uthash.h"

/* A hashtable with string keys and int values */
struct boxData {
    const char *boxscore;       /* key:  boxscore's filepath as a string */
    int lastViewedByte;         /* value1: last viewed byte on boxscore */
    int month;                  /* value2: month of last date checked */
    int day;                    /* value3: day of last date checked */
    UT_hash_handle hh;          /* makes this struct hashable */
};

/* Global boxscoreBuffer */
int bufferYear; /* year for which we are maintaining a buffer */
struct boxData *boxHashTable; /* hash table for the year */
    // indicator variable for testing
int seekPosUsed;

/* Add an item to a hash */
void addBoxscore(const char*boxscore, int lastViewedByte, int month, int day);
/* Retrieve an item from the has */
struct boxData *findBoxscore(const char*boxscore);
/* Delete the entirety of the hash table */
void deleteTable();