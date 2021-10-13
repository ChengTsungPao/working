#include <iostream>
#include <string>
#include <vector>

using namespace std;
using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

vector<vector<int>> copy_vector(vector<vector<int>> origin);

String^ stringTransfer(string str) {
	return gcnew String(str.c_str());
}

string stringTransfer(String^ str) {
	return (const char*)(System::Runtime::InteropServices::Marshal::StringToHGlobalAnsi(str).ToPointer());
}

Bitmap^ bitmapVectorTransfer(vector<vector<vector<int>>> image) {

	Bitmap^ bitmapImage = gcnew Bitmap(image.size(), image[0].size());

	for (int x = 0; x < bitmapImage->Width; x++) {
		for (int y = 0; y < bitmapImage->Height; y++) {
			vector<int> RGB = image[x][y];
			bitmapImage->SetPixel(x, y, Color::FromArgb(RGB[0], RGB[1], RGB[2]));
		}
	}

	return bitmapImage;
}

vector<vector<vector<int>>> bitmapVectorTransfer(Bitmap^ image) {
	vector<vector<vector<int>>> imageVector;
	int intGray = 0;

	for (int x = 0; x < image->Width; x++) {
		vector<vector<int>> arr;
		for (int y = 0; y < image->Height; y++) {
			Color RGB = image->GetPixel(x, y);
			arr.push_back({ RGB.R, RGB.G, RGB.B });
		}
		imageVector.push_back(copy_vector(arr));
	}

	return imageVector;
}

vector<vector<int>> copy_vector(vector<vector<int>> origin) {
	vector<vector<int>> copyVector;

	for (int i = 0; i < (int)(origin.size()); i++) {
		copyVector.push_back({ origin[i][0], origin[i][1], origin[i][2] });
	}

	return copyVector;
}