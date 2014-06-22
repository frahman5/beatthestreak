#include "uthash.h"

/* A hashtable with string keys and int values */
struct boxData {
    const char *boxscore;       /* key:  boxscore's filepath as a string */
    int lastViewedByte;         /* value: last viewed byte on boxscore */
    UT_hash_handle hh;          /* makes this struct hashable */
};

/* Global hash table */
struct boxData *boxHashTable;

/* Add an item to a hash */
void addBoxscore(const char*boxscore, int lastViewedByte);
/* Retrieve an item from the has */
struct boxData *findBoxscore(const char*boxscore);
/* Delete the entirety of the hash table */
void deleteTable();