#include <string>
#include <iostream>
#include <vector>

using namespace std;
using namespace System;
using namespace System::Drawing;
using namespace System::Windows::Forms;

Bitmap^ readImage(String^ path, String^ filename);
vector<string> getFolderFiles(string path);
