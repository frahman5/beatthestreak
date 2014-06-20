/* C analogues of select functions from Researcher.py */

#include "Python.h" /* also imports stdlib, stdio, string, errno */
#include "datetime.h" 

/* did_get_hit method */
static PyObject* cresearcher_finish_did_get_hit(
          PyObject* self, PyObject* args, PyObject* kwargs) {
    
    /* Get the keyword values into local variables */
    PyDateTime_Date* d;
    char* firstName;
    char* lastName;
    char* boxscore;
    char* keywords[] = {"date", "firstName", "lastName", "boxscore", NULL}; 
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Osss", keywords, &d, 
                                     &firstName, &lastName, &boxscore))
        return NULL; 

    /* check that we extracted it correctly */
    int year = PyDateTime_GET_YEAR(d);
    int month = PyDateTime_GET_MONTH(d);
    int day = PyDateTime_GET_DAY(d);
    printf("The year is: %d\n", year);
    printf("The month is %d\n", month);
    printf("The day is %d\n", day);

    printf("The firstname is %s\n", firstName);
    printf("The lastname is %s\n", lastName);
    printf("The boxscore path is %s\n", boxscore);  

    return Py_False;
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

/* Will need to import datetime.date from python */
/* How do I play nicely with player objects? */
/* Excess Notes: "hi" is a string literal 
     C compiler automatically allocates sufficient space in memory
     Type of this expression is 'const char *' */

/* ALL functions must return PyObject* */

/* On References: 
   An important situation where this arises is in objects that are passed as 
   arguments to C functions in an extension module that are called from Python;
    the call mechanism guarantees to hold a reference to every argument for the
    duration of the call. */

/*ToDo:
-make did_get_hit return a bool | DONE
-get datetime in here | DONE
-get player names in here | DONE
-read CPython API intro
*/