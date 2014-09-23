//hello.cpp
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#define EXPORT_POINTER_DLL
#include "pointer_test.h"

POINTER_API char* GetPointerInfo(const int ** array)
{
    int size = 5;
    const int **tmp = (const int **)malloc(sizeof(int)*5);
//    *(*tmp) = 1;
//    *tmp[1] = 2;
    printf("**tmp is %h",**tmp);
    printf("*tmp is %h",*tmp);
    printf("tmp is %h",tmp);


    array = tmp;
    return "just OK";
}