#include "uthash.h"

/************ Structs and Functions for Hash Table and Cache *********/
    /* A hashtable with string keys and string values */
struct playerDateData {
    const char *lIdDashDate;    /* key:  lahmanID + date (e.g: jeterde01-4/3)*/
    char *hitVal;
    char *otherInfo;
    UT_hash_handle hh;          /* makes this struct hashable */
};


/* Global playerInfoCache */
extern int playerInfoCacheYear; /* year for which we are maintaining a buffer */
extern struct playerDateData *playerInfoCache; /* Hash Table for the year */


/* delete the cache and free any items on the heap that were either in or 
   pointed to by the cache */
int deletePlayerInfoCache();
/* Retrieve an item from the hash */
struct playerDateData *findPlayerDateData(char*lahmanID, char*date);
/* Add an item to the hash table */
int addPlayerDateData(char *lahmanID);
/* Mostly for debugging */
void printPlayerInfoCache();