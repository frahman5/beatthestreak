/* C analogues of select functions from Researcher.py */

#include "Python.h" /* also imports stdlib, stdio, string, errno */

/* did_get_hit method */
static PyObject* cresearcher_did_get_hit(PyObject* self, PyObject* args) {
    return Py_False;
    /* other object: Py_True */
}

/* Declares the methods in the module */
static PyMethodDef cresearcherMethods[] = {
    {"did_get_hit", cresearcher_did_get_hit, METH_NOARGS, 
    "FILL IN DOC LATER"}, 
    {NULL, NULL, 0, NULL} /* sentinel */
};

/* Called by main to initialize the module */
void initcresearcher(void) {
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
-get datetime in here
-get player names in here
-read CPython API intro
*/