#include "MyForm.h"
#include <iostream>
#include <string>

using namespace std;
using namespace System;
using namespace System::Windows::Forms;
[STAThread]
void main()
{
	Application::EnableVisualStyles();
	Application::SetCompatibleTextRenderingDefault(false);
	Homework1::MyForm form;
	Application::Run(%form);
}

