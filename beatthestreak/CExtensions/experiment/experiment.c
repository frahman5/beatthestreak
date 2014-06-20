/* Test File to try using c code from Python */

#include "Python.h" /* imports stdlib, stdio, string, errno */

/* A sample method */
static PyObject* experiment_foo(PyObject* self, PyObject* args) {
    return PyInt_FromLong(42L);
}

/* Declares the methods in the module */
static PyMethodDef experimentMethods[] = {
    {"foo", experiment_foo, METH_NOARGS, "Return the meaning of everything"}, 
    {NULL, NULL, 0, NULL} /* sentinel */
};

/* Called by main to initialize the module */
void initexperiment(void) {
    /* Creates a "module object" and inserts it in dictionary sys.modules
    with key "experiment". Inserts built-in function objects into experiment
    module based on experimentMethods Table. Returns a pointer to the
    new module object */
    printf("Initializing\n");   
    PyObject *m;
    m = Py_InitModule("experiment", experimentMethods);
    if (m == NULL)
        printf("initializing experiment module did not work!\n");
        return;
}

/* Excess Notes: "hi" is a string literal 
     C compiler automatically allocates sufficient space in memory
     Type of this expression is 'const char *' */

/* ALL functions must return PyObject* */