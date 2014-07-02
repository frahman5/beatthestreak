/* C analogues of select functions from Researcher.py */
#include "Python.h"
// #include "Python.h" /* also imports stdlib, stdio, string, errno */
#include "datetime.h"   /* PyDatetime support */
#include "crhelper.h"   /* get_third_num_in_string, _search_boxscore */
#include "playerInfoCache.h"

#define cfinishDidGetHitDocString "datetime.date string string string -> bool\
\n\
    date: datetime.date | the date for which we are finishing the did_get_hit search\n\
    firstName: string | first name of player we are searching for\n\
    lastName: string | last name of player we are searching for\n\
    boxscore: string | filepath of boxscore file for player on date\n\
\n\
Searches the boxscore for the player's boxscore line and returns True if he had a hit, False otherwise\n\
\n\
Example Usage: finish_did_get_hit(date=d1, firstName=n1, lastname=n2, boxscore=b1)\n\
where the above variables are set appropriately"

#define cgetHitInfoDocString "datetime.date string -> string|bool, string|None\
\n\
        lahmanID: string | lahmanID of player of interest\n\
        date: datetime.date | date of interest\n\
\n\
    Produces (hitResult, otherInfo) for player on given date.\n\
    Possible values of (hitResult, otherInfo):\n\
        1) (True, None) # player got a hit on date date\n\
        2) (False, None) # player did not get a hit on date date\n\
        3) ('pass', 'Suspended, Invalid.'): # player played in a suspended, invalid game on date date\n\
        4) (True, 'Suspended, Valid.'): # player got a hit in a suspended, valid game on date date\n\
        5) (False, 'Suspended, Valid.'): # player did not get a hit in a suspended, valid game on date date\n\
\n\
    Technically, this should also account for case 6 below, but because it is exceedingly rare,\n\
    we do not account for it. This effectively makes our simulation slightly MORE conservative--i.e \n\
    more likely to reset a streak--than it should be, making us confident that at the worst, \n\
    playing for real should give us better results than our simulation\n\
        6) ('pass', 'Screwy ABs'): # player played in a valid game on date date but all his at bats were \n\
               either base on balls, hit batsman, defensive interference, defensive obstruction, \n\
               or sacrifice bunt\n\
\n\
    Relies on player Hit Info csv's located in results/playerInfo"
#define cdidStartDocString "datetime.date string -> bool\
\n\
            date: datetime.date | date of interest\n\
            lahmanID: string | lahmanID of player of interest\n\
\n\
        Returns: True if player started a game on the given date, False otherwise"

/* Return Py_True if player started, Py_False otherwise */
static PyObject *cdid_start(
          PyObject *self, PyObject *args, PyObject *kwargs) {
    struct playerDateData *pDD;

    /* Get the keyword values into local variables */
    PyDateTime_Date *d;
    char *lahmanID;
    char *keywords[] = {"date", "lahmanID", NULL}; 
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Os:cdid_start", 
                                     keywords, &d, &lahmanID)){
        return NULL; // ParseTupleAndKeywords sets the exception for me
    }

    /* Get month, day and create month/day*/
    char monthS[4];         // 2 digit month plus space for the sentinel and one for writeoff
    char dayS[4];           // 2 digit day plus space for the sentinel and one for writeoff
    char yearS[6];          // 4 digit year plus space for the sentinel and one for writeoff
    char monthSlashDay[7];   // 2 digit month/2 digit day plus space for the sentinel and one for writeoff
    sprintf(monthS, "%d", PyDateTime_GET_MONTH(d));
    sprintf(dayS, "%d", PyDateTime_GET_DAY(d));
    sprintf(yearS, "%d", PyDateTime_GET_YEAR(d));
    strcpy(monthSlashDay, monthS);
    strcat(monthSlashDay, "/");
    strcat(monthSlashDay, dayS);
 
    /* Check if the cache is for this year or not */
    int yearInt = atoi(yearS);
    if (playerInfoCacheYear != yearInt) {
        playerInfoCacheYear = yearInt;
        if (deletePlayerInfoCache() == -1) {
            return NULL;
        }
    }

    /* See if the player is in the cache, if not, add him 
       lahmanID-1/1 is the indicator hashkey that we use to see if a 
       player has been added to the cache or not */
    if (!findPlayerDateData(lahmanID, "1/1")) {
        // should raise error if the key is already in there
        if (addPlayerDateData(lahmanID) == -1) { return NULL; } 
    }

    pDD = findPlayerDateData(lahmanID, monthSlashDay);

    if (pDD) {
        Py_INCREF(Py_True);
        return Py_True;
    } else {
        Py_INCREF(Py_False);
        return Py_False;
    }

}

/* Return Py_True if player got a hit, Py_False otherwise */
static PyObject *cfinish_did_get_hit(
          PyObject *self, PyObject *args, PyObject *kwargs) {
    
    /* Get the keyword values into local variables */
    PyDateTime_Date *d;
    char *firstName;
    char *lastName;
    char *boxscore;
    char *keywords[] = {"date", "firstName", "lastName", "boxscore", NULL}; 
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Osss:finish_did_get_hit", 
                                     keywords, &d, &firstName, &lastName, &boxscore)){
        return NULL; // ParseTupleAndKeywords sets the exception for me
    }

    /* open the file */ 
    FILE *fp = fopen(boxscore, "r");
    if (!fp) {
        return PyErr_Format(PyExc_IOError, "Could not open boxscore\n");
    }

    /* Get month, day,  year. */
    char monthS[4];         // 2 digit month plus space for the sentinel and one for writeoff
    char dayS[4];           // 2 digit day plus space for the sentinel and one for writeoff
    char yearS[6];          // 4 digit year plus space for the sentinel and one for writeoff
    sprintf(monthS, "%d", PyDateTime_GET_MONTH(d));
    sprintf(dayS, "%d", PyDateTime_GET_DAY(d));
    sprintf(yearS, "%d", PyDateTime_GET_YEAR(d));
    // printf("In finish_did_get_hit: months: %s\n", monthS);

    /* Create the searchD string */
    char *backslash = "/";
    char searchD[11];       // ten digit mm/dd/yyyy plus space for the sentinel
    char *helperArray[] = { monthS, backslash, dayS, backslash, yearS };
    /* strcpy the first string so we don't concat onto garbage during strcats */
    strcpy(searchD, helperArray[0]);
    for (int i = 1; i < 5; i++) { strcat(searchD, helperArray[i]); }

    /* Create the searchP string. */
    unsigned long len = strlen(firstName) + strlen(lastName) + 2; // + 2 for sentinels on firtsName and lastName
    char *searchP = (char *) malloc(len);
    /* strcpy the first string so we don't concat onto garbage during strcats */
    if (searchP) {
        strcpy(searchP, lastName);
        strcat(searchP, " ");   
        strncat(searchP, firstName, 1); // get the first letter of firstName
    } else {
        fclose(fp);
        return PyErr_Format(PyExc_SystemError, 
                            "Malloc for searchP with len %lu failed", len );
    }
    // printf("In cfinish_did_get_hit: searchP: %s\n", searchP);
    char *foundIt;
    int success = -1; // search_boxscore returns 0 on success and -1 on failure

    /* Search for the line with searchD */
    success = _search_boxscore(fp, &foundIt, searchD, boxscore);
    if (success == -1) {
        fclose(fp);
        free(searchP);
        return NULL;
    }

    /* Search for line with searchP */
    success = _search_boxscore(fp, &foundIt, searchP, boxscore);
    if (success == -1) { // reached end of file
        fclose(fp);
        free(searchP);
        return NULL;
    }
    
    
    /* get the player hit info
       Number of hits player had is third number from the left in 
       the returned string */
    int numHits = get_third_num_in_string(foundIt);
    if (numHits == -1) {        // make sure we didn't have an error
        fclose(fp);
        free(searchP);
        return NULL;  
    }

    // close the file, free the memory
    fclose(fp);
    free(searchP);

    /* return player hit info. Calling function now owns a reference to
       Py_True or Py_False */
    if (numHits > 0) { 
        Py_INCREF(Py_True);
        return Py_True;
    } else {
        Py_INCREF(Py_False);
        return Py_False;
    }
}

/* Returns hitVal, otherInfo for player with lahmanID on given date */
static PyObject *cget_hit_info(PyObject *self, PyObject *args, 
                               PyObject *kwargs) {

    /* Get the keyword values into local variables */
    PyDateTime_Date* d;
    char* lahmanID;
    char* keywords[] = {"date", "lahmanID", NULL}; 
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Os:cget_hit_info", 
                                     keywords, &d, &lahmanID)) {
        return NULL; // ParseTupleAndKeywords sets the exception for me
    }

    /* Get month, day, year. */
    char monthS[3];         // 2 digit month plus space for the sentinel
    char dayS[3];           // 2 digit day plus space for the sentinel
    char yearS[5];          // 4 digit year plus space for sentinel
    sprintf(monthS, "%d", PyDateTime_GET_MONTH(d));
    sprintf(dayS, "%d", PyDateTime_GET_DAY(d));
    sprintf(yearS, "%d", PyDateTime_GET_YEAR(d));

    /* Get the date string */
    char *backslash = "/";
    char date[7];       // 5 digit mm/dd/ plus space for the sentinel and 1 breathing spot
    /* strcpy the first string so we don't concat onto garbage during strcats */
    strcpy(date, monthS);
    strcat(date, backslash);
    strcat(date, dayS);

    /* Check if the cache is for this year or not */
    int yearInt = atoi(yearS);
    if (playerInfoCacheYear != yearInt) {
        playerInfoCacheYear = yearInt;
        if (deletePlayerInfoCache() == -1) {
            return NULL;
        }
    }

    /* Get the player's info, or add it if its not there yet */
    struct playerDateData *pDD;
    pDD = findPlayerDateData(lahmanID, date);
    if (!pDD) {
        // should raise error if the key is already in there
        // should set error if there is one
        if (addPlayerDateData(lahmanID) == -1) {
            return NULL;
        } 
        // printf("we got the player's info\n");
        pDD = findPlayerDateData(lahmanID, date);
        if (!pDD) {
            return NULL;
        }
    }

    // else
    char *hitVal = pDD->hitVal;
    char *otherInfo = pDD->otherInfo;
    // this will return None to the interpreter
    if (strcmp(otherInfo, "n/a") == 0) { otherInfo = NULL; }
    if (strcmp(hitVal, "pass") == 0) {
        return Py_BuildValue("ss", hitVal, otherInfo);
    } else {
        if (strcmp(hitVal, "True") == 0) {
            return Py_BuildValue("Os", Py_True, otherInfo);
        }
        else {
            assert (strcmp(hitVal, "False") == 0);
            return Py_BuildValue("Os", Py_False, otherInfo);
        }
    }
}
/* Declares the methods in the module */
static PyMethodDef cresearcherMethods[] = {
    { "cfinish_did_get_hit", (PyCFunction) cfinish_did_get_hit, 
      METH_KEYWORDS, cfinishDidGetHitDocString }, 
    { "cget_hit_info", (PyCFunction) cget_hit_info, 
      METH_KEYWORDS, cgetHitInfoDocString }, 
    { "cdid_start", (PyCFunction) cdid_start, 
      METH_KEYWORDS, cdidStartDocString },    
    { NULL, NULL, 0, NULL} /* sentinel */
};

/* Called by main to initialize the module */
void initcresearcher(void) {
    /* puts to a pointer to a C struct in PyDateTimeAPI for datetime operations */
    PyDateTime_IMPORT;    
    /* Creates module object and inserts it in sys.modules dictionary.
       Inserts built-in function objects into module based on cresearcherMethods
       Returns a pointer to the new module object */
    Py_InitModule("cresearcher", cresearcherMethods);
}