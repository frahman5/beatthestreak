/* C analogues of select functions from Researcher.py */

#include "Python.h" /* also imports stdlib, stdio, string, errno */
#include "datetime.h"   /* PyDatetime support */
#include "crhelper.h"   /* get_third_num_in_string */

#define MAXLINE 80 // boxscore line lengths seem to be < 80. MUST CHECK

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
                                     &firstName, &lastName, &boxscore)){
        return NULL; // raises an exception on its own
    }

    //open the file
    FILE *fp = fopen(boxscore, "r");
    if (fp == NULL) {
        return PyErr_Format(PyExc_IOError, "Could not open boxscore\n");
    }

    /* Get month day year. dont initalize month, day, year buffers because 
    they get printed to right away */
    char monthS[3]; // 2 digit month plus space for the sentinel
    char dayS[3];   // 2 digit day plus space for the sentinel
    char yearS[5];   // 4 digit year plus space for the sentinel
    sprintf(monthS, "%d", PyDateTime_GET_MONTH(d));
    sprintf(dayS, "%d", PyDateTime_GET_DAY(d));
    sprintf(yearS, "%d", PyDateTime_GET_YEAR(d));

    /* Create the searchD string. We strcpy the first string to assure
       that we don't concat onto garbage on the strcats */
    char *backslash = "/";
    char searchD[11]; // ten digit mm/dd/yyyy plus space for the sentinel
    char *helperArray[] = { monthS, backslash, dayS, backslash, yearS};
    strcpy(searchD, helperArray[0]);
    for (int i=1; i < 5; i++) {
        strcat(searchD, helperArray[i]);
    }

    /* Create the searchP string. We strcpy the first string so we don't
       concat onto garbage when we call strcat. The plus 2 is for breathing room*/
    unsigned long len = strlen(firstName) + strlen(lastName) + 2;
    char *searchP = (char *) malloc(len);
    if (searchP) {
        strcpy(searchP, lastName);
        strcat(searchP, " ");   
        strncat(searchP, firstName, 1); // get the first letter of firstName
    } else {
        return PyErr_Format(PyExc_SystemError, 
            "Malloc for searchP with len %lu failed", len );
    }
    char *foundIt;
    int success = -1; // search_boxscore returns 1 on success and 0 on failure
    /* Search for the line with searchD */
    success = _search_boxscore(fp, &foundIt, searchD, boxscore);
    if (success == 0) { // reached end of file
        return PyErr_Format(PyExc_EOFError, 
                "Reached end of boxcore on date search: %s\n", searchD);
    }

    /* Search for line with searchP */
    success = _search_boxscore(fp, &foundIt, searchP, boxscore);
    if (success == 0) { //reached end of file
        return PyErr_Format(PyExc_EOFError, 
            "Reached end of boxscore on player search: %s\n", searchP);
    }
    
    
    /* get the player hit info
       number of hits player had is third number from the left in 
       the returned string */
    int numHits = get_third_num_in_string(foundIt);
    if (numHits == -1) { // make sure we didn't have an error
        return PyErr_Format(PyExc_IndexError, 
            "Could not find three numbers in boxscore %s on date %s and\
 player %s", boxscore, searchD, searchP);    
    }

    //close the file
    fclose(fp);
    free(searchP);

    //return player hit info
    return (numHits > 0) ? Py_True : Py_False;
}

const char *docString= 
"PyDateTime_date char* char* char* -> int\
\n\
    date: PyDateTIME_date | the date for which we are finishing the did_get_hit search\
    firstName: char* | first name of player we are searching for\
    lastName: char* | last name of player we are searching for\
    boxscore: char* | filepath of boxscore file for player on date\
\n\
Searches the boxscore for the player's boxscore line and\
returns the number of hits he had on the given date";

/* Declares the methods in the module */
static PyMethodDef cresearcherMethods[] = {
    {"finish_did_get_hit", 
    (PyCFunction)cresearcher_finish_did_get_hit, 
    METH_KEYWORDS, 
"datetime.date str str str -> int\
\n\
    date: datetime.date | the date for which we are finishing the did_get_hit search\n\
    firstName: str | first name of player we are searching for\n\
    lastName: str | last name of player we are searching for\n\
    boxscore: str | filepath of boxscore file for player on date\n\
\n\
Searches the boxscore for the player's boxscore line and\n\
returns True if he got a hit, False if not, and an Exception if appropriate\n\
\n\
Example Usage: finish_did_get_hit(date=d1, firstName=n1, lastname=n2, boxscore=b1)\n\
where the above variables are set appropriately"},
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