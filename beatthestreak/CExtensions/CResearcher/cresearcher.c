/* C analogues of select functions from Researcher.py */

#include "Python.h" /* also imports stdlib, stdio, string, errno */
#include "datetime.h" 
#include "crhelper.h"

#define MAXLINE 80 // boxscore line lengths seem to be < 80. MUST CHECK

/* Left to do 
    -> test | DONE
    -> install error handling
    -> test for speed
    -> divide into seperate functions if so desired
    -> test for speed
    -> determine if you want to install hash-based lookups for increased performance */
/* did_get_hit method */
static PyObject *cresearcher_finish_did_get_hit(
          PyObject *self, PyObject *args, PyObject *kwargs) {
    
    /* Get the keyword values into local variables */
    PyDateTime_Date* d;
    char* firstName;
    char* lastName;
    char* boxscore;
    char* keywords[] = {"date", "firstName", "lastName", "boxscore", NULL}; 
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Osss", keywords, &d, 
                                     &firstName, &lastName, &boxscore))
        return NULL; 

    //open the file
    FILE *fp;
    fp = fopen(boxscore, "r");
    assert(fp != NULL);

    /* Construct the searchD string */
    char *backslash = "/";
    char searchD[11]; // ten digit mm/dd/yyyy plus space for the sentinel

    char monthS[3]; // 2 digit month plus space for the sentinel
    sprintf(monthS, "%d", PyDateTime_GET_MONTH(d));
    char dayS[3];   // 2 digit day plus space for the sentinel
    sprintf(dayS, "%d", PyDateTime_GET_DAY(d));
    char yearS[5];   // 4 digit year plus space for the sentinel
    sprintf(yearS, "%d", PyDateTime_GET_YEAR(d));

    char *helperArray[] = {monthS, backslash, dayS, backslash, yearS};
    for (int i=0; i < 5; i++) {
        strcat(searchD, helperArray[i]);
    }

    /* Search for the line with searchD and print that line */
    char line[MAXLINE];
    char *foundIt = NULL;
    while (!foundIt) {
        fgets(line, MAXLINE, fp);
        foundIt = strstr(line, searchD);
    }

    char *searchP = (char *) malloc(strlen(firstName) + strlen(lastName) + 2);
    if (searchP) {
        strcat(searchP, lastName);
        strcat(searchP, " ");   
        strncat(searchP, firstName, 1); // get the first letter of firstName
        printf("searchP : %s\n", searchP);
    } else {
        printf("Malloc failed");
        return 0; // returning a non-python value raises an error
    }
    char *foundIt2 = NULL;
    while (!foundIt2) {
        fgets(line, MAXLINE, fp);
        foundIt2 = strstr(line, searchP);
    }
    
    /* get the player hit info
       number of hits player had is third number from the left in 
       the returned string */
    int numHits = get_third_num_in_string(foundIt2);
    assert (numHits != -1); // make sure we didn't have an error
    //close the file and free searchP
    free(searchP);
    fclose(fp);

    // printf("player: %s %s, numHits: %d\n", firstName, lastName, numHits);
    //return player hit info
    if (numHits > 0) { return Py_True; } 
    else { return Py_False; }
}

// char const* docString= 
// "PyDateTime_date char* char* char* -> int\

//     date: PyDateTIME_date | the date for which we are finishing the did_get_hit search\
//     firstName: char* | first name of player we are searching for\
//     lastName: char* | last name of player we are searching for\
//     boxscore: char* | filepath of boxscore file for player on date\

// Searches the boxscore for the player's boxscore line and\
// returns the number of hits he had on the given date";

/* Declares the methods in the module */
static PyMethodDef cresearcherMethods[] = {
    {"finish_did_get_hit", cresearcher_finish_did_get_hit, 
      METH_KEYWORDS, "FILL IN LATER"}, 
    {NULL, NULL, 0, NULL} /* sentinel */
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




/* On References: 
   An important situation where this arises is in objects that are passed as 
   arguments to C functions in an extension module that are called from Python;
    the call mechanism guarantees to hold a reference to every argument for the
    duration of the call. */

/* Good Refactors:
-> figure out max line length of boxscores */