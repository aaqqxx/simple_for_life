//hello.cpp
#include <string.h>
#define EXPORT_HELLO_DLL
#include "hello.h"

HELLO_API char* GetStructInfo(struct StructTest* pStruct)
{
	for (int i = 0; i < ARRAY_NUMBER; i++)
		pStruct->iArray[i] = i;

	pStruct->pChar = "hello python!";

	strcpy (pStruct->str, "hello world!");

	pStruct->number = 100;

	return "just OK";
}