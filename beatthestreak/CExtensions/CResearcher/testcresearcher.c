#include <assert.h>
#include <stdio.h>
#include "crhelper.h"

int main() {
    char *testString1 = " Jose Reyes 5 6 8 10";
    char *testString2 = "asdfasdfasccc 78 sergserg 56 srgserg 90 sergserg 21 srgserg 54";
    char *testString3 = "Butler B, cf          4  0  2  0   Kelly R, cf           4  0  0  0  ";
    char *testString4 = "Kelly R, cf           5  1  3  0";
    char *testString5 = "Butler B, cf          41  15  22  71  Kelly R, cf           49  61  70  24  ";

    assert (get_third_num_in_string(testString1) == 8);
    assert (get_third_num_in_string(testString2) == 90);
    assert (get_third_num_in_string(testString3) == 2);
    assert (get_third_num_in_string(testString4) == 3);
    assert (get_third_num_in_string(testString5) == 22);

    printf("All tests passed!\n");
    return 1;
}