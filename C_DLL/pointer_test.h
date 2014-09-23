//pointer_test.h

//编译命令：
//g++ -shared -Wl,--kill-at,--output-def,hello.def -o hello.dll hello.cpp
#ifdef EXPORT_POINTER_DLL
#define POINTER_API __declspec(dllexport)
#else
#define POINTER_API __declspec(dllimport)
#endif

extern "C"
{
	//HELLO_API int IntAdd(int , int);
	POINTER_API char* GetPointerInfo(struct StructTest* pStruct);
}