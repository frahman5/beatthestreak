#include <assert.h>
#include <stdio.h>
#include "crhelper.h"
#include <string.h>

int main() {
    /* test get_third_num_in_string */
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


    /* test _search_boxscore
        A;; searchD searchP pairs are as they would in the function call, 
            a searchD search followed by a searchP call */
    char *searchD1 = "4/25/2012";
    char *answerD1 = "4/25/2012 -- Miami at New York (N)\n";
    char *searchP1 = "Thole J";
    char *answerP1 = "Thole J, c            3  0  1  0   \n";

    char *searchD2 = "4/5/2012";
    char *answerD2 = "4/5/2012 -- Atlanta at New York (D)\n";
    char *searchP2 = "Constanza J";
    char *answerP2 = "Constanza J, lf       1  0  0  0   Ramirez R, p          0  0  0  0   \n";

    char *searchD3 = "9/27/2012";
    char *answerD3 = "9/27/2012 -- Pittsburgh at New York (D)\n";
    char *searchP3 = "Marte S";
    char *answerP3 = "Marte S, lf           3  0  0  0   Tejada R, ss          4  1  1  0   \n";

    // TEST 1
    FILE *bs1 = fopen(
        "/Users/faiyamrahman/programming/Python/beatthestreak/beatthestreak/\
datasets/retrosheet/unzipped/events2012/2012NYNB.txt", "r");
    if (bs1 == NULL) { 
        printf("failed opening the boxscore\n");
        return 0;
    }
    char *foundIt;
    _search_boxscore(bs1, &foundIt, searchD1);
    assert (strcmp(foundIt, answerD1) == 0);
    _search_boxscore(bs1, &foundIt, searchP1);
    assert (strcmp(foundIt, answerP1) == 0);
    fclose(bs1);

    // TEST 2
    FILE *bs2 = fopen(
        "/Users/faiyamrahman/programming/Python/beatthestreak/beatthestreak/\
datasets/retrosheet/unzipped/events2012/2012NYNB.txt", "r");
    if (bs2 == NULL) { 
        printf("failed opening the boxscore\n");
        return 0;
    }
    _search_boxscore(bs2, &foundIt, searchD2);
    assert (strcmp(foundIt, answerD2) == 0);
    _search_boxscore(bs2, &foundIt, searchP2);
    assert (strcmp(foundIt, answerP2) == 0);
    fclose(bs2);    

    // Test 3
    FILE *bs3 = fopen(
        "/Users/faiyamrahman/programming/Python/beatthestreak/beatthestreak/\
datasets/retrosheet/unzipped/events2012/2012NYNB.txt", "r");
    if (bs3 == NULL) { 
        printf("failed opening the boxscore\n");
        return 0;
    }
    _search_boxscore(bs3, &foundIt, searchD3);
    assert (strcmp(foundIt, answerD3) == 0);
    _search_boxscore(bs3, &foundIt, searchP3);
    assert (strcmp(foundIt, answerP3) == 0);
    fclose(bs3);

    printf("All tests passed!\n");
    return 1;
}