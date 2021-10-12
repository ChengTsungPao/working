#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;
using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

Bitmap^ mean_filter(Bitmap^ originImage, int kernel);
int sum(Bitmap^ originImage, int startScanX, int endScanX, int startScanY, int endScanY);
int adjustVal(int val);

Bitmap^ median_filter(Bitmap^ originImage, int kernel);
int findMedian(Bitmap^ originImage, int startScanX, int endScanX, int startScanY, int endScanY);


Bitmap^ smooth_filter(Bitmap^ originImage, char kind) {
	switch (kind) {
		case 'a':
			return mean_filter(originImage, 3);
		default:
			return median_filter(originImage, 3);
	}
}

Bitmap^ mean_filter(Bitmap^ originImage, int kernel) { // sliding window
	Bitmap^ image = gcnew Bitmap(originImage->Width, originImage->Height);

	int startScanX = kernel / 2;
	int startScanY = kernel / 2;
	int endScanX = (image->Width) - 1 - kernel / 2;
	int endScanY = (image->Height) - 1 - kernel / 2;

	int intGray = 0;

	intGray = sum(originImage, 0, kernel - 1, 0, kernel - 1) / (kernel * kernel);
	image->SetPixel(kernel / 2, kernel / 2, Color::FromArgb(intGray, intGray, intGray));

	for (int x = startScanX + 1; x < endScanX + 1; x++) {
		Color RGB = image->GetPixel(x - 1, kernel / 2);
		intGray = sum(originImage, x + kernel / 2, x + kernel / 2, 0, kernel - 1) / (kernel * kernel);
		intGray -= sum(originImage, x - kernel / 2 - 1, x - kernel / 2 - 1, 0, kernel - 1) / (kernel * kernel);
		intGray += Convert::ToInt32(RGB.R);
		intGray = adjustVal(intGray);
		image->SetPixel(x, kernel / 2, Color::FromArgb(intGray, intGray, intGray));
	}

	for (int y = startScanY + 1; y < endScanY + 1; y++) {
		for (int x = startScanX; x < endScanX + 1; x++) {
			Color RGB = image->GetPixel(x, y - 1);
			intGray = sum(originImage, x - kernel / 2, x + kernel / 2, y + kernel / 2, y + kernel / 2) / (kernel * kernel);
			intGray -= sum(originImage, x - kernel / 2, x + kernel / 2, y - kernel / 2 - 1, y - kernel / 2 - 1) / (kernel * kernel);
			intGray += Convert::ToInt32(RGB.R);
			intGray = adjustVal(intGray);
			image->SetPixel(x, y, Color::FromArgb(intGray, intGray, intGray));
		}
	}

	return image;
}

int adjustVal(int val) { // why ??
	if (val < 0) {
		return 0;
	} else if (val > 255) {
		return 255;
	} else {
		return val;
	}
}

int sum(Bitmap^ originImage, int startScanX, int endScanX, int startScanY, int endScanY) {

	int invGray = 0;

	for (int y = startScanY; y < endScanY + 1; y++) {
		for (int x = startScanX; x < endScanX + 1; x++) {
			Color RGB = originImage->GetPixel(x, y);
			invGray += Convert::ToInt32(RGB.R);
		}
	}

	return invGray;
}

Bitmap^ median_filter(Bitmap^ originImage, int kernel) {
	Bitmap^ image = gcnew Bitmap(originImage->Width, originImage->Height);

	int startScanX = kernel / 2;
	int startScanY = kernel / 2;
	int endScanX = (image->Width) - 1 - kernel / 2;
	int endScanY = (image->Height) - 1 - kernel / 2;

	int intGray;

	for (int y = startScanY; y < endScanY + 1; y++) {
		for (int x = startScanX; x < endScanX + 1; x++) {
			intGray = Convert::ToInt32(findMedian(originImage, x - kernel / 2, x + kernel / 2, y - kernel / 2, y + kernel / 2));
			image->SetPixel(x, y, Color::FromArgb(intGray, intGray, intGray));
		}
	}

	return image;
}

int findMedian(Bitmap^ originImage, int startScanX, int endScanX, int startScanY, int endScanY) {

	vector<int> grayVal;

	for (int y = startScanY; y < endScanY + 1; y++) {
		for (int x = startScanX; x < endScanX + 1; x++) {
			Color RGB = originImage->GetPixel(x, y);
			grayVal.push_back(Convert::ToInt32(RGB.R));
		}
	}

	sort(grayVal.begin(), grayVal.end());

	if (grayVal.size() % 2) {
		return grayVal[grayVal.size() / 2];
	} else {
		return (grayVal[grayVal.size() / 2 - 1] + grayVal[grayVal.size() / 2]) / 2;
	}
	
}