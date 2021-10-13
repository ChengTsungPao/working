#pragma once
#include <iostream>
#include <string>
#include <vector>

using namespace std;
using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

String^ stringTransfer(string str);
string stringTransfer(String^ str);

Bitmap^ bitmapVectorTransfer(vector<vector<vector<int>>> image);
vector<vector<vector<int>>> bitmapVectorTransfer(Bitmap^ image);
