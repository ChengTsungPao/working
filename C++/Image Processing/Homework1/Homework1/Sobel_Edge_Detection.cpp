#include <iostream> 
#include <algorithm>
#include <math.h>

using namespace std;
using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

Bitmap^ sobel_vertical_filter(Bitmap^ originImage);
Bitmap^ sobel_horizontal_filter(Bitmap^ originImage);
Bitmap^ sobel_edge_filter(Bitmap^ originImage);
int product(Bitmap^ originImage, int filter[3][3], int scanX, int scanY);

int vertical[3][3] = {
	{  1,  2,  1  },
	{  0,  0,  0  },
	{ -1, -2, -1  }
};

int horizontal[3][3] = {
	{  1,  0, -1  },
	{  2,  0, -2  },
	{  1,  0, -1  }
};

Bitmap^ sobel_edge_dection(Bitmap^ originImage, char kind) {

	switch (kind) {
		case 'v':
			return sobel_vertical_filter(originImage);
		case 'h':
			return sobel_horizontal_filter(originImage);
		default:
			return sobel_edge_filter(originImage);
	}

}

Bitmap^ sobel_vertical_filter(Bitmap^ originImage) {

	int kernel = sizeof(vertical[0]) / sizeof(int);

	int intGray = 0;
	int startScanX = kernel / 2;
	int startScanY = kernel / 2;
	int endScanX = (originImage->Width) - 1 - kernel / 2;
	int endScanY = (originImage->Height) - 1 - kernel / 2;

	Bitmap^ verticalImage = gcnew Bitmap(originImage->Width, originImage->Height);
	for (int y = startScanY; y < endScanY + 1; y++) {
		for (int x = startScanX; x < endScanX + 1; x++) {
			intGray = product(originImage, vertical, x, y);
			verticalImage->SetPixel(x, y, Color::FromArgb(intGray, intGray, intGray));
		}
	}

	return verticalImage;
}

Bitmap^ sobel_horizontal_filter(Bitmap^ originImage) {

	int kernel = sizeof(horizontal[0]) / sizeof(int);

	int intGray = 0;
	int startScanX = kernel / 2;
	int startScanY = kernel / 2;
	int endScanX = (originImage->Width) - 1 - kernel / 2;
	int endScanY = (originImage->Height) - 1 - kernel / 2;

	Bitmap^ horizontalImage = gcnew Bitmap(originImage->Width, originImage->Height);
	for (int y = startScanY; y < endScanY + 1; y++) {
		for (int x = startScanX; x < endScanX + 1; x++) {
			intGray = product(originImage, horizontal, x, y);
			horizontalImage->SetPixel(x, y, Color::FromArgb(intGray, intGray, intGray));
		}
	}

	return horizontalImage;
}

Bitmap^ sobel_edge_filter(Bitmap^ originImage) {

	int kernel = sizeof(horizontal[0]) / sizeof(int);

	int intGray = 0;
	int startScanX = kernel / 2;
	int startScanY = kernel / 2;
	int endScanX = (originImage->Width) - 1 - kernel / 2;
	int endScanY = (originImage->Height) - 1 - kernel / 2;

	Bitmap^ verticalImage = sobel_vertical_filter(originImage);
	Bitmap^ horizontalImage = sobel_horizontal_filter(originImage);
	Bitmap^ sobelImage = gcnew Bitmap(originImage->Width, originImage->Height);
	for (int y = startScanY; y < endScanY + 1; y++) {
		for (int x = startScanX; x < endScanX + 1; x++) {
			int Gx = Convert::ToInt32((horizontalImage->GetPixel(x, y)).R);
			int Gy = Convert::ToInt32((  verticalImage->GetPixel(x, y)).R);
			intGray = (int)(sqrt(Gx * Gx + Gy * Gy));
			intGray = intGray > 255 ? 255 : intGray;
			sobelImage->SetPixel(x, y, Color::FromArgb(intGray, intGray, intGray));
		}
	}

	return sobelImage;
}

int product(Bitmap^ originImage, int filter[3][3], int scanX, int scanY) {

	int invGray = 0;
	int kernel = sizeof(filter[0]) / sizeof(int);

	for (int y = 0; y < kernel; y++) {
		for (int x = 0; x < kernel; x++) {
			Color RGB = originImage->GetPixel(scanX - kernel / 2 + x, scanY - kernel / 2 + y);
			invGray += Convert::ToInt32(RGB.R) * filter[x][y];
		}
	}

	return min(abs(invGray), 255);
}
