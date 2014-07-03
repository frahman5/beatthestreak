#include <assert.h>
#include <stdio.h>
#include <string.h>

#include "crhelper.h"
#include "boxscoreBuffer.h"
#include "playerInfoCache.h"
#include "config.h"

#define ARRAY_SIZE(array) sizeof(array)/sizeof(array[0])

void test_get_third_num_in_string();

int test__search_boxscore();

void test_structure_boxscore_buffer();

void test_functionality_boxscore_buffer();

void test_structure_playerInfo_cache();

int main() {
    test_get_third_num_in_string();
    test__search_boxscore();
    test_structure_boxscore_buffer();
    test_functionality_boxscore_buffer();
    test_structure_playerInfo_cache();
    printf("All tests passed!\n");
}


void test_functionality_boxscore_buffer() {
    /* tests that boxscore buffer is functional */

    /****** CHECK 1: If a team's info is not on the buffer, then startSeekPos
            is 0 and boxscore buffer is updated *********/

        /* Check 1.1: If it's a new year, startSeekPos = 0 and boxscore 
            buffer is set to [year, {'team': lastByteChecked}] */
       // Put 2010 on the buffer and clear the hashTable
    bufferYear = 2010;
    deleteTable();
        /* Run the finish_did_get_portion of R.did_get_hit(date(2012, 6, 17), 
        Player("Albert", "Pujols")) */
    char boxscore1[200];
    strcpy(boxscore1, rootDir);
    strcat(boxscore1, "datasets/retrosheet/unzipped/events2012/2012ANAB.txt");
    FILE *fp = fopen(boxscore1, "r");
    assert (fp);
    char *foundIt;
    char searchD[] = "6/17/2012";
    char searchP[] = "Pujols A";
    _search_boxscore(fp, &foundIt, searchD, boxscore1);
    assert (seekPosUsed == 0); // we only do seeking on date searches
    _search_boxscore(fp, &foundIt, searchP, boxscore1);
    /* Check that the buffer has the right values */
    assert (bufferYear == 2012);
    struct boxData *boxData1 = findBoxscore(boxscore1);
    assert (strcmp(boxData1->boxscore, boxscore1) == 0);
    assert (boxData1->month = 6);
    assert (boxData1->day = 17);
    assert (boxData1->lastViewedByte == 53216);
    fclose(fp);

       /* Check 1.2: If its the same year but the team's boxscore has not
           yet been opened, startSeekPos = 0 and team is added to 
           boxscoreBuffer[1].keys */

        /* Run the __search_boxscore portion of R.did_get_hit(date(2012, 6, 15),
        Player("Jose", "Reyes", 2012, debut="6/10/2003")) */
    char boxscore2[200];
    strcpy(boxscore2, rootDir);
    strcat(boxscore2, "datasets/retrosheet/unzipped/events2012/2012TBAB.txt");
//     char *boxscore2 = "/Users/faiyamrahman/programming/Python/beatthestreak/\
// beatthestreak/datasets/retrosheet/unzipped/events2012/2012TBAB.txt";
    fp = fopen(boxscore2, "r");
    assert (fp);
    char *foundIt2;
    char searchD2[] = "6/15/2012";
    char searchP2[] = "Reyes J";
    _search_boxscore(fp, &foundIt2, searchD2, boxscore2);
    assert (seekPosUsed == 0);
    _search_boxscore(fp, &foundIt2, searchP2, boxscore2);
    /* Check that the buffer has the right values */
    assert (bufferYear == 2012);
       // first added boxscore
    assert (strcmp(boxData1->boxscore, boxscore1) == 0);
    assert (boxData1->month = 6);
    assert (boxData1->day = 17);
    assert (boxData1->lastViewedByte == 53216);
       // newly added boxscore
    struct boxData *boxData2 = findBoxscore(boxscore2);
    assert (strcmp(boxData2->boxscore, boxscore2) == 0);
    assert (boxData2->month == 6);
    assert (boxData2->day == 15);
    assert (boxData2->lastViewedByte == 57626);
    fclose(fp);

    /**** CHECK 2: if a team's boxscore info is on the buffer, then their
          info is examined on the buffer *****/
        
        /* Check 2.1: If date is GREATER than date on buffer, startSeekPos 
           = boxscoreBuffer[1][team][1] and buffer's last byte checked 
          is updated */
         /* Run the __search_boxscore portion of R.did_get_hit(date(2012, 8, 9), 
          Player("Colby", "Rasmus", 2012) */
    char *boxscore3 = boxscore2;
    fp = fopen(boxscore3, "r");
    assert (fp);
    char *foundIt3;
    char searchD3[] = "8/9/2012";
    char searchP3[] = "Rasmus C";
    _search_boxscore(fp, &foundIt3, searchD3, boxscore3);
    assert (seekPosUsed == 57626);
    _search_boxscore(fp, &foundIt3, searchP3, boxscore3);
     /* Check that the buffer has the right values */
    assert (bufferYear == 2012);
        // first added boxscore
    assert (strcmp(boxData1->boxscore, boxscore1) == 0);
    assert (boxData1->month = 6);
    assert (boxData1->day = 17);
    assert (boxData1->lastViewedByte == 53216);
        // second added boxscore
    assert (strcmp(boxData2->boxscore, boxscore2) == 0);
    assert (boxData2->month == 8);
    assert (boxData2->day == 9);
    assert (boxData2->lastViewedByte == 101668);
    fclose(fp);

       /* CHECK 2.2: if date is less than date on buffer, startSeekPos = 0
          and last byte checked is updated */
    char *boxscore4 = boxscore3;
    fp = fopen(boxscore4, "r");
    assert (fp);
    char *foundIt4;
    char searchD4[] = "6/15/2012";
    char searchP4[] = "Reyes J";
    _search_boxscore(fp, &foundIt4, searchD4, boxscore4);
    assert (seekPosUsed == 0); // boxscore used correctly?
    _search_boxscore(fp, &foundIt4, searchP4, boxscore4);
        // check boxscore updated correctly
    assert (bufferYear == 2012);
        // first added boxscore
    assert (strcmp(boxData1->boxscore, boxscore1) == 0);
    assert (boxData1->month = 6);
    assert (boxData1->day = 17);
    assert (boxData1->lastViewedByte = 53216);
        // second added boxscore
    assert (strcmp(boxData2->boxscore, boxscore2) == 0);
    assert (boxData2->month == 6);
    assert (boxData2->day == 15);
    assert (boxData2->lastViewedByte == 57626);
    fclose(fp);

    /* Check 2.3: If date is EQUAL to date on buffer, startSeekPos = 0
             and last byte checked is the SAME */
    fp = fopen(boxscore4, "r");
    assert (fp);
    _search_boxscore(fp, &foundIt4, searchD4, boxscore4);
    assert (seekPosUsed == 0); // boxscore used correctly?
    _search_boxscore(fp, &foundIt4, searchP4, boxscore4);
        // check boxscore updated correctly
    assert (bufferYear == 2012);
        // first added boxscore
    assert (strcmp(boxData1->boxscore, boxscore1) == 0);
    assert (boxData1->month = 6);
    assert (boxData1->day = 17);
    assert (boxData1->lastViewedByte = 53216);
        // second added boxscore
    assert (strcmp(boxData2->boxscore, boxscore2) == 0);
    assert (boxData2->month == 6);
    assert (boxData2->day == 15);
    assert (boxData2->lastViewedByte == 57626);
    fclose(fp);

    deleteTable();

}

void test_structure_boxscore_buffer() {
    /* Tests that the hash table and basic structure of the boxscore
        buffer works */
    struct boxData *bD;

    /* Test that we can retrieve and set the boxscorebuffer year */
    bufferYear = 7;
    assert (bufferYear == 7);

    /* Test..... */
    deleteTable();
    assert (HASH_COUNT(boxHashTable) == 0);
        /* adding */
    addReplaceBoxscore("boxscore1", 10L, 5, 3);
    assert (HASH_COUNT(boxHashTable) == 1);
        /* finding */
    struct boxData *boxData1 = findBoxscore("boxscore1");
    assert (strcmp(boxData1->boxscore, "boxscore1") == 0);
    assert (boxData1->lastViewedByte == 10L);
    assert (boxData1->month == 5);
    assert (boxData1->day == 3);
        /* replacing an already hashed key */
    addReplaceBoxscore("boxscore1", 55L, 7, 2);
    assert(HASH_COUNT(boxHashTable) == 1); 
      // also do a manual count to guard against nonunique keys
    int i = 0;
    for (bD=boxHashTable; bD != NULL; bD=bD->hh.next) { i++; }
    assert (i == 1);
    assert (strcmp(boxData1->boxscore,"boxscore1") == 0);
    assert (boxData1->lastViewedByte == 55L);
    assert (boxData1->month == 7);
    assert (boxData1->day == 2);
        /* deleting */
    deleteTable(); // frees memory
    assert (HASH_COUNT(boxHashTable) == 0);

    /* Another test to gaurd against nonunique keys. Motivated by a bug */
    char *bs2 = "/Users/faiyamrahman/programming/Python/beatthestreak/\
beatthestreak/datasets/retrosheet/unzipped/events2010/2010ANAB.txt";
    char *bs3 = "/Users/faiyamrahman/programming/Python/beatthestreak/\
beatthestreak/datasets/retrosheet/unzipped/events2010/2010ANAB.txt";
    // printf("\n\nBefore first addition:");
    // printHashTable(0);
    addReplaceBoxscore(bs2, 48L, 4, 4);
    // printf("After first addition:");
    // printHashTable(0);
    assert (HASH_COUNT(boxHashTable) == 1);
       // manual count
    i = 0;
    for (bD=boxHashTable; bD != NULL; bD=bD->hh.next) { i++; }
    assert (i == 1);
    addReplaceBoxscore(bs3, 50L, 4, 5);
    // printf("\nAfter second addition:");
    // printHashTable(0);
    assert (HASH_COUNT(boxHashTable) == 1);
       // manual count
    i = 0;
    for (bD=boxHashTable; bD != NULL; bD=bD->hh.next) { i++; }
    assert (i == 1);

}
void test_get_third_num_in_string() {

    /* basic funtion tests */
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

    // char *errorTestString1 = "Inge B, 3b            4  1";
    // /* error handling tests */
    //    // If there are <= 2 numbers in the test string, func should
    //    // return -1 and set a global exception
    // assert (get_third_num_in_string(errorTestString1) == -1);
    //    // Get global exception
    // assert(PyErr_GivenExceptionMatches(PyErr_Occurred(),PyExc_ValueError));


}

int test__search_boxscore() {
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
    char bs1Path[150];
    strcpy(bs1Path, rootDir);
    strcat(bs1Path, "datasets/retrosheet/unzipped/events2012/2012NYNB.txt");
    FILE *bs1 = fopen(bs1Path, "r");
    if (bs1 == NULL) { 
        printf("failed opening the boxscore\n");
        return 0;
    }
    char *foundIt;
    _search_boxscore(bs1, &foundIt, searchD1, bs1Path);
    assert (strcmp(foundIt, answerD1) == 0);
    _search_boxscore(bs1, &foundIt, searchP1, bs1Path);
    assert (strcmp(foundIt, answerP1) == 0);
    fclose(bs1);

    // TEST 2
    char *bs2Path = bs1Path;
    FILE *bs2 = fopen(bs2Path, "r");
    if (bs2 == NULL) { 
        printf("failed opening the boxscore\n");
        return 0;
    }
    _search_boxscore(bs2, &foundIt, searchD2, bs2Path);
    assert (strcmp(foundIt, answerD2) == 0);
    _search_boxscore(bs2, &foundIt, searchP2, bs2Path);
    assert (strcmp(foundIt, answerP2) == 0);
    fclose(bs2);    

    // Test 3
    char *bs3Path = bs1Path;
    FILE *bs3 = fopen(bs3Path, "r");
    if (bs3 == NULL) { 
        printf("failed opening the boxscore\n");
        return 0;
    }
    _search_boxscore(bs3, &foundIt, searchD3, bs3Path);
    assert (strcmp(foundIt, answerD3) == 0);
    _search_boxscore(bs3, &foundIt, searchP3, bs3Path);
    assert (strcmp(foundIt, answerP3) == 0);
    fclose(bs3);

    
    return 1;
}

void test_structure_playerInfo_cache() {
    /* Tests that the hash table and basic structure of the playerInfoCache works */
    char *MarkLorettaDates2001[] = 
        {"5/19", "5/20", "5/22", "5/23", "5/24", "5/25", "5/28", "5/29", "5/30", 
        "5/31", "6/1", "6/2", "6/3", "6/5", "6/6", "6/8", "6/9", "6/10", "6/12", 
        "6/13", "6/14", "6/15", "6/17", "6/18", "6/19", "6/22", "6/23", "6/24", 
        "6/25", "6/26", "6/27", "6/29", "6/30", "7/1", "7/3", "7/4", "7/5", 
        "7/6", "7/7", "7/13", "7/14", "7/15", "7/16", "7/18", "7/19", "7/20", 
        "7/21", "7/23", "7/24", "7/25", "7/27", "7/28", "7/29", "7/31", "8/1", 
        "8/2", "8/3", "8/4", "8/9", "8/10", "8/11", "8/12", "8/14", "8/15", 
        "8/16", "8/17", "8/18", "8/19", "8/20", "8/22", "8/23", "8/24", "8/25", 
        "8/26", "8/27", "8/28", "8/29", "8/31", "9/1", "9/2", "9/3", "9/4", 
        "9/5", "9/6", "9/7", "9/8", "9/9", "9/10", "9/17", "9/18", "9/21", 
        "9/22", "9/25", "9/26", "9/27", "9/29"};
    char *MarkLorettaHitVals2001[] = 
        {"False", "True", "True", "True", "True", "True", "True", "True", 
        "True", "True", "True", "True", "True", "True", "True", "True", "True", 
        "False", "True", "False", "True", "pass", "True", "True", "True", 
        "False", "True", "True", "True", "False", "False", "True", "True", 
        "True", "True", "False", "True", "False", "True", "True", "True", 
        "False", "False", "True", "True", "True", "True", "True", "True", 
        "True", "True", "True", "True", "False", "False", "True", "True", 
        "False", "True", "True", "True", "True", "True", "True", "False", 
        "True", "True", "True", "False", "True", "True", "True", "True", 
        "True", "True", "True", "True", "True", "True", "True", "True", 
        "True", "False", "True", "True", "True", "True", "True", "True", 
        "False", "True", "True", "True", "True", "False", "True"};
    char *MarkLorettaOtherInfos2001[] = 
        {"n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", 
        "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", 
        "n/a", "Suspended-Invalid.", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a",
         "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a",
        "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a",
        "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a",
        "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", 
        "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", 
        "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", 
        "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a", "n/a"};
    char *MarkLorettaOpPitcherEras2001[] = 
        {"4.1", "9.32", "3.19", "2.32", "0.84", "4.94", "2.69", "1.65", "6.29", 
         "4.45", "4.2", "3.64", "3.3", "4.15", "4.36", "3.31", "4.44", "5.32", 
         "5.15", "4.33", "2.92", "4.4", "5.37", "5.79", "10.19", "3.71", "4.65",
         "4.71", "2.7", "4.37", "6.75", "4.66", "2.87", "3.91", "5.64", "3.44", 
         "3.42", "5.74", "3.27", "3.58", "3.73", "4.91", "4.7", "inf", "inf", 
         "1.29", "4.07", "inf", "9.0", "4.33", "4.01", "5.11", "5.05", "4.23", 
         "5.24", "0.0", "4.29", "2.47", "3.47", "5.96", "3.07", "4.22", "3.08", 
         "4.51", "2.98", "4.82", "4.55", "3.82", "3.29", "3.79", "4.01", "5.06", 
         "4.67", "5.26", "5.07", "3.1", "5.45", "4.99", "4.55", "3.83", "inf", 
         "5.65", "4.55", "4.55", "3.65", "4.91", "2.68", "3.07", "3.75", "4.52", 
         "4.99", "6.27", "4.58", "3.41", "2.4", "4.98"};

    /* Test that we can retrieve and set the playerInfoCacheyear */
    playerInfoCacheYear = 7;
    assert (playerInfoCacheYear == 7);
    playerInfoCacheYear = 809;
    assert (playerInfoCacheYear == 809);

    /* Test..... */
    deletePlayerInfoCache();
    assert (HASH_COUNT(playerInfoCache) == 0);
    //     /* adding */
    playerInfoCacheYear = 2006;
    assert (addPlayerDateData("jeterde01") == 0); // should add Derek Jeter"s hitInfos from 2006
    // printPlayerInfoCache();
    assert (HASH_COUNT(playerInfoCache) == 150); // 149 dates, and one indicator hash
        /* finding */
    struct playerDateData *pD = findPlayerDateData("jeterde01", "6/28");
    assert (strcmp(pD->lIdDashDate, "jeterde01-6/28") == 0);
    assert (strcmp(pD->hitVal, "True") == 0);
    assert (strcmp(pD->otherInfo, "n/a") == 0);
    assert (strcmp(pD->opPitcherERA, "3.89") == 0);
        /* finding on steroids: make sure EVERY elem of the hash table fpr
           a player is correct */
    playerInfoCacheYear = 2001;
       // includes a suspended game
    addPlayerDateData("loretma01"); // should add Mark Loretta's hitInfos from 2001
    assert (ARRAY_SIZE(MarkLorettaDates2001) == 96);
    assert (ARRAY_SIZE(MarkLorettaHitVals2001) == 96);
    assert (ARRAY_SIZE(MarkLorettaOtherInfos2001) == 96);
    assert (ARRAY_SIZE(MarkLorettaOpPitcherEras2001) == 96);
    struct playerDateData *pD1;
    for (int i = 0; i < 96; i++) {
        pD1 = findPlayerDateData("loretma01", MarkLorettaDates2001[i]);
        assert (strcmp(pD1->hitVal, MarkLorettaHitVals2001[i]) == 0);
        assert (strcmp(pD1->otherInfo, MarkLorettaOtherInfos2001[i]) == 0);
        assert (strcmp(pD1->opPitcherERA, MarkLorettaOpPitcherEras2001[i]) == 0);
    }
        /* test delete */
    deletePlayerInfoCache();
    assert (HASH_COUNT(playerInfoCache) == 0);

}