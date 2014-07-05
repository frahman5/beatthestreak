#include "uthash.h"
#include "Python.h" // comment out to compile with gcc

/************ Structs and Functions for Hash Table and Cache *********/
    /* A hashtable with string keys and string values */
struct playerDateData {
    const char *lIdDashDate;    /* key:  lahmanID + date (e.g: jeterde01-4/3)*/
    char hitVal[8];             /* value1: hitval is one of ("True", "Pass", "False") */
    char otherInfo[21];         /* value2: otherInfo is one of ("n/a", "Suspended, Valid.", "Suspended, Invalid."") */
    char opPitcherERA[100];       /* value3: opPitcherERA is either of the form x.xx, x an int, or inf */
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