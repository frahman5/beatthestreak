#include <assert.h>
#include <stdio.h>
#include "crhelper.h"

int main() {
    char *testString1 = " Jose Reyes 5 6 8 10";
    char *testString2 = "asdfasdfasccc 78 sergserg 56 srgserg 90 sergserg 21 srgserg 54";
    char *testString3 = "Butler B, cf          4  0  2  0   Kelly R, cf           4  0  0  0  ";
    char *testString4 = "Kelly R, cf           5  1  3  0";
    char *testString5 = "Butler B, cf          41  15  22  71  Kelly R, cf           49  61  70  24  ";
    char *testString6 = "Altuve J, 2b          5  0  2  2   Buck J, c             4  0  1  0";  
    char *testString7 = "Granderson C, cf      4  0  1  0   Figgins C, 3b         4  1  1  0";   
    char *testString8 = "Polanco P, 2b         4  0  0  1   Cabrera O, ss         4  1  1  1";   
    char *testString9 = "Rodriguez I, c        4  1  2  0   Guerrero V, rf        4  0  0  0";   
    char *testString10 = "Ordonez M, rf         4  2  3  1   Anderson G, lf        4  0  0  1";   
    char *testString11 = "Guillen C, ss         3  0  0  0   Salmon T, dh          4  0  0  0   ";
    char *testString12 = "Shelton C, 1b         4  0  1  1   Erstad D, cf          2  0  1  0   ";
    char *testString13 = "Infante O, dh         4  0  0  0   Kotchman C, 1b        3  0  0  0   ";
    char *testString14 = "Monroe C, lf          3  1  1  0   Mathis J, c           3  0  0  0   ";
    char *testString15 = "Inge B, 3b            4  1  1  1   Kennedy A, 2b         3  0  0  0 ";
    assert (get_third_num_in_string(testString1) == 8);
    assert (get_third_num_in_string(testString2) == 90);
    assert (get_third_num_in_string(testString3) == 2);
    assert (get_third_num_in_string(testString4) == 3);
    assert (get_third_num_in_string(testString5) == 22);
    assert (get_third_num_in_string(testString6) == 2);
    assert (get_third_num_in_string(testString7) == 1);
    assert (get_third_num_in_string(testString8) == 0);
    assert (get_third_num_in_string(testString9) == 2);
    assert (get_third_num_in_string(testString10) == 3);
    assert (get_third_num_in_string(testString11) == 0);
    assert (get_third_num_in_string(testString12) == 1);
    assert (get_third_num_in_string(testString13) == 0);
    assert (get_third_num_in_string(testString14) == 1);
    assert (get_third_num_in_string(testString15) == 1);

    printf("All tests passed!\n");
    return 1;
}