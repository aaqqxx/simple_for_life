//hello.h

//编译命令：
//g++ -shared -Wl,--kill-at,--output-def,hello.def -o hello.dll hello.cpp
#ifdef EXPORT_HELLO_DLL
#define HELLO_API __declspec(dllexport)
#else
#define HELLO_API __declspec(dllimport)
#endif

#define ARRAY_NUMBER 20
#define STR_LEN 20

struct StructTest
{
	int number;
	char* pChar;
	char str[STR_LEN];
	int iArray[ARRAY_NUMBER];
};

extern "C"
{
	//HELLO_API int IntAdd(int , int);
	HELLO_API char* GetStructInfo(struct StructTest* pStruct);
}