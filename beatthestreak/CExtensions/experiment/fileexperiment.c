/* A short script to figure out how we might access a certain line, byte
   of a stream */

#include <stdio.h>

char *testFile = "/Users/faiyamrahman/programming/Python/beatthestreak/\
beatthestreak/datasets/retrosheet/unzipped/events2013/2013ANAB.txt";

int main() {
    // open the file
    FILE *fp = fopen(testFile, "r");
    if (fp == NULL) {
        printf("file open fail\n");
        return 0;
    }

    // write a loop for 100 iterations of incrmenting the pointer and 
    // seeing what the output is
    // getc(fp);   
    for (int i = 0; i < 15; i++) {
        printf("%c ", getc(fp));
        fseek(fp, 1L, SEEK_CUR);
        printf("%lu\n", ftell(fp));
    }
    fclose(fp);

    return 1;
}