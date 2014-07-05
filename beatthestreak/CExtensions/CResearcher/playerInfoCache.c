#include <string.h>
#include <stdio.h>
#include "playerInfoCache.h"
#include "config.h" // pInfoDir

#define MAXLINE 40 // much more than we need for adding player Data

int playerInfoCacheYear = -1; /* year for which we are maintaining a buffer */
struct playerDateData *playerInfoCache = NULL; /* Hash Table for the year */


/* delete the cache and free any items on the heap that were either in or 
   pointed to by the cache */
int deletePlayerInfoCache() {
    /* Removes all hash elements from the hash Table and 
       frees up associated memory */   
    struct playerDateData *curBucket, *tmp;

    HASH_ITER(hh, playerInfoCache, curBucket, tmp) {
        HASH_DEL(playerInfoCache, curBucket);   /* delete; advances to next */
        if (!curBucket) {
            PyErr_SetString(PyExc_LookupError, "HASH_ITER failed while deleting playerInfoCache");
            return -1;
        }
        free((void *) curBucket->lIdDashDate);  /* free the hash table key */
        free(curBucket);                        /* free the pointer */
    }
    return 0;
}
/* Retrieve an item from the hash */
struct playerDateData *findPlayerDateData(char *lahmanID, char *date) {
    /* Returns a pointer to the playerDateData with key lahmanID-date if its 
    in the hash table, or NULL if its not in it */
    struct playerDateData *pDD;

    /* HASH_FIND_STR(hashTable, pointer to key, output struct) */
       // 15: 9 for lahmanID, 1 for dash, 3 for date, 1 because
       // all arrays must be valid one spot off the end, and 1 for breathing room
    char hashKey[15];
    strcpy(hashKey, lahmanID);
    strcat(hashKey, "-");
    strcat(hashKey, date);

    HASH_FIND_STR( playerInfoCache, hashKey, pDD);
    return pDD;
}
/* Add an item to the hash table */
int addPlayerDateData(char *lahmanID) {
    /* bucket to be added to cache */
    struct playerDateData *pDD;
    /* string used to open playerHitInfoCSV
         25: 4 for the year, 2 for backslashes, 9 for the lahmanID, 4 for the 
        .txt, 1 for the sentinel. Then some 5 for breathing room */
    char filePath[strlen(pInfoDir) + 25];
    char filePathSuffix[25];
    /* A container for fgets returns */
    char line[MAXLINE];
    /* Pointers to the key and values of our cache bucket */
    char *date;
    char *hitVal;
    char *otherInfo;
    char *opPitcherERA;

    /* open the file for year playerInfoCacheYear and lahmanID */
    sprintf(filePathSuffix, "/%d/%s.txt", playerInfoCacheYear, lahmanID);
    strcpy(filePath, pInfoDir);
    strcat(filePath, filePathSuffix);
    FILE *fp = fopen(filePath, "r");
    if (!fp) {
        printf("filePath: %s\n", filePath);
        PyErr_SetString(PyExc_IOError, "could not open file\n"); // comment out to compile with gcc
        return -1;
    }

    /** Iterate through file, add a seperate bucket for each row in the file */
    /* we ignore the top line, which is column header*/
    fgets(line, MAXLINE, fp); 
       // fgets returns NULL upon EOF
    while (fgets(line, MAXLINE, fp)) {
        date = strtok(line, ",");
        hitVal = strtok(NULL, ",");
        otherInfo = strtok(NULL, ",");
        opPitcherERA = strtok(NULL, ",\n");

        /* Construct the hash key */
        // 3: 1 for the sentinel, 1 for a dash, 1 for breathing room
        char *hashKey = (char *) malloc(strlen(lahmanID) + strlen(date) + 3);
        if (!hashKey) {
            fclose(fp);
            PyErr_SetString(PyExc_SyntaxError, "Failed to allocate hashKey on the heap\n");
            return -1;
        } else {
            strcpy(hashKey, lahmanID);
            strcat(hashKey, "-");
            strcat(hashKey, date);
        }

        /* Return an error if we've already added it */
        HASH_FIND_STR(playerInfoCache, hashKey, pDD);
        if (pDD) {
            fclose(fp);
            free(hashKey);
            PyErr_SetString(PyExc_ValueError, "Tried to add Player's hit info\
to the player info hash table >= 1 times.\n");
            return -1; // we should never encounter this!
        /* Otherwise constrcut the bucke and add it */
        } else {
            pDD = (struct playerDateData *) malloc(sizeof(struct playerDateData));
            if (!pDD) {
                fclose(fp);
                free(hashKey);
                PyErr_SetString(PyExc_SystemError, 
                    "Failed to allocate playerDateData on the heap\n");
                return -1;
            }
            pDD->lIdDashDate = hashKey;
            strcpy(pDD->hitVal, hitVal);
            strcpy(pDD->otherInfo, otherInfo);
            strcpy(pDD->opPitcherERA, opPitcherERA);
            HASH_ADD_STR(playerInfoCache, lIdDashDate, pDD);
        }
    }

     // Add a indicator bucket to tell users that a player has been 
       // added to the hash 
    // 6: 3 for 1/1, 1 for the dash, 1 for the sentinel, 1 for breathing room
    char *indicatorHashKey = (char *) malloc(strlen(lahmanID) + 6);
    if (!indicatorHashKey) {
        fclose(fp);
        PyErr_SetString(PyExc_SyntaxError, "Failed to allocate hashKey on the heap\n");
        return -1;
    } else {
        strcpy(indicatorHashKey, lahmanID);
        strcat(indicatorHashKey, "-");
        strcat(indicatorHashKey, "1/1");
    }
    pDD = (struct playerDateData *) malloc(sizeof(struct playerDateData));
    if (!pDD) {
        fclose(fp);
        free(indicatorHashKey);
        PyErr_SetString(PyExc_SystemError, 
            "Failed to allocate playerDateData on the heap\n");
        return -1;
    } else {
        pDD->lIdDashDate = indicatorHashKey;
        strcpy(pDD->hitVal,"I"); // I for "Indicator"
        strcpy(pDD->otherInfo, "I"); // I for "Indicator"
        // pDD->opPitcherERA = "I";
        strcpy(pDD->opPitcherERA, "I"); // I for "Indicator"
        HASH_ADD_STR(playerInfoCache, lIdDashDate, pDD);
    }

    // fclose(fp);
    return 0;
}
/* Mostly for debugging */
void printPlayerInfoCache() {
    struct playerDateData *pD;
    char *indent4 = "    ";
    char *indent8 = "        ";
    
    printf("\n********** HASHTABLE *********\n");
    int i = 0;
    for (pD=playerInfoCache; pD != NULL; pD=pD->hh.next) {
        i++;
        printf("Item Num: %d\n", i);    
        printf(
        "%shashKey %s\n%shitVal: %s\n%sotherInfo: %s\n", 
        indent4, pD->lIdDashDate, indent8, pD->hitVal, 
        indent8, pD->otherInfo);
        }
    }
