#include "tryexcept.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>


#define TESTEXCEPT (1)
#define BAZ (2)

int
main(void){
    int retcode = 1;
    char test123[] = {"This is a demo of not sucky code\n"};
    char *all1 = NULL;
    char *all2 = NULL;
    
    all1 = malloc(sizeof(test123)+1);
    if (all1 == NULL){goto cleanup;}

    all2 = malloc(sizeof(test123)+1);
    if (all2 == NULL){goto cleanup;}

    memset(all1, 0, sizeof(test123)+1);
    memcpy(all1, test123, sizeof(test123));
    memset(all2, 0, sizeof(test123)+1);
    memcpy(all2, test123, sizeof(test123));
    printf("test1 %s", all1);
    printf("test2 %s", all2);
    
    TRY{
        printf("This is in the try\n");
        THROW( TESTEXCEPT );
    }
    CATCH ( TESTEXCEPT){
        printf("This is an except\n");
    }
    CATCH ( BAZ){
        printf("This is baz\n");
    }
    ENDTRY;
    retcode = 0;
cleanup:
    if (all1) {free(all1);}
    if (all2) {free(all2);}
    goto exit;
exit:
    return retcode;
}
