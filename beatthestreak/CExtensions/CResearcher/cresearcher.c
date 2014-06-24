/* C analogues of select functions from Researcher.py */

#include "Python.h" /* also imports stdlib, stdio, string, errno */
#include "datetime.h"   /* PyDatetime support */
#include "crhelper.h"   /* get_third_num_in_string, _search_boxscore */

#define finishDidGetHitDocString "datetime.time string string string -> bool\
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

/* Return Py_True if player got a hit, Py_False otherwise */
static PyObject *cresearcher_finish_did_get_hit(
          PyObject *self, PyObject *args, PyObject *kwargs) {
    
    /* Get the keyword values into local variables */
    PyDateTime_Date* d;
    char* firstName;
    char* lastName;
    char *boxscore;
    char* keywords[] = {"date", "firstName", "lastName", "boxscore", NULL}; 
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
    char monthS[3];         // 2 digit month plus space for the sentinel
    char dayS[3];           // 2 digit day plus space for the sentinel
    char yearS[5];          // 4 digit year plus space for the sentinel
    sprintf(monthS, "%d", PyDateTime_GET_MONTH(d));
    sprintf(dayS, "%d", PyDateTime_GET_DAY(d));
    sprintf(yearS, "%d", PyDateTime_GET_YEAR(d));

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
    char *foundIt;
    int success = -1; // search_boxscore returns 0 on success and -1 on failure
    
    /* Search for the line with searchD */
    success = _search_boxscore(fp, &foundIt, searchD, boxscore);
    if (success == -1) { // reached end of file
        fclose(fp);
        free(searchP);
        return PyErr_Format(PyExc_EOFError, 
                "Reached end of boxcore on date search: %s\n", searchD);
    }

    /* Search for line with searchP */
    success = _search_boxscore(fp, &foundIt, searchP, boxscore);
    if (success == -1) { // reached end of file
        fclose(fp);
        free(searchP);
        return PyErr_Format(PyExc_EOFError, 
                            "Reached end of boxscore on player search: %s\n", 
                            searchP);
    }
    
    
    /* get the player hit info
       Number of hits player had is third number from the left in 
       the returned string */
    int numHits = get_third_num_in_string(foundIt);
    if (numHits == -1) {        // make sure we didn't have an error
        fclose(fp);
        free(searchP);
        return PyErr_Format(PyExc_IndexError, 
                            "Could not find three numbers in boxscore %s on date %s and\
 player %s", boxscore, searchD, searchP);    
    }

    // close the file, free the memory
    fclose(fp);
    free(searchP);

    //return player hit info
    return (numHits > 0) ? Py_True : Py_False;
}

/* Declares the methods in the module */
static PyMethodDef cresearcherMethods[] = {
    { "finish_did_get_hit", (PyCFunction) cresearcher_finish_did_get_hit, 
      METH_KEYWORDS, finishDidGetHitDocString },     
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