#include <iostream>
#include <string>

using namespace System;
using namespace std;

String^ stringTransfer(string str) {
	return gcnew String(str.c_str());
}

string stringTransfer(String^ str) {
	return (const char*)(System::Runtime::InteropServices::Marshal::StringToHGlobalAnsi(str).ToPointer());
}