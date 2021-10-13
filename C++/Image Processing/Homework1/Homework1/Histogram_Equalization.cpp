#include "RGB_Extraction_Transformation.h"

#include <map>
#include <iostream>
#include <algorithm>

using namespace std;
using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

map<int, int> Counter(Bitmap^ image);
map<int, int> calculate(map<int, int> imageCollection);
pair<int, int> findMaxMinKey(map<int, int> imageCollection);
Bitmap^ transfer(Bitmap^ originImage, map<int, int> transferImageCollection);

map<int, int> originImageCollection;
map<int, int> transferImageCollection;

Bitmap^ histogram_equalization(Bitmap^ originImage) {

	map<int, int> mappingImageCollection;
	Bitmap^ grayImage;
	Bitmap^ transferImage;

	grayImage = gray_channel(originImage);
	originImageCollection = Counter(grayImage);
	mappingImageCollection = calculate(originImageCollection);
	transferImage = transfer(grayImage, mappingImageCollection);
	transferImageCollection = Counter(transferImage);

	return transferImage;
}

map<int, int> Counter(Bitmap^ image) {

	map<int, int> imageCollection;

	int intGray;

	for (int y = 0; y < image->Height; y++) {
		for (int x = 0; x < image->Width; x++) {
			Color RGB = image->GetPixel(x, y);

			intGray = Convert::ToInt32(RGB.R);

			if (imageCollection.find(intGray) == imageCollection.end()) {
				imageCollection[intGray] = 1;
			} else {
				imageCollection[intGray] += 1;
			}
		}
	}

	return imageCollection;
}

map<int, int> calculate(map<int, int> originImageCollection) {
	map<int, int> imageCollection;

	int preCollection = 0;
	for (int intGray = 0; intGray < 256; intGray++) {
		if (originImageCollection.find(intGray) != originImageCollection.end()) {
			originImageCollection[intGray] += preCollection;
			preCollection = originImageCollection[intGray];
		}
	}

	pair<int, int> key = findMaxMinKey(originImageCollection);
	int maxKey = key.first;
	int minKey = key.second;
	for (int intGray = 0; intGray < 256; intGray++) {
		if (originImageCollection.find(intGray) != originImageCollection.end()) {
			imageCollection[intGray] = (int)((originImageCollection[intGray] - originImageCollection[minKey]) * 255 / (originImageCollection[maxKey] - originImageCollection[minKey]));
		}
	}

	return imageCollection;
}

pair<int, int> findMaxMinKey(map<int, int> imageCollection) {
	pair<int, int> key;
	for (int intGray = 0; intGray < 256; intGray++) {
		if (imageCollection.find(intGray) != imageCollection.end()) {
			key.first = max(key.first, intGray);
			key.second = min(key.second, intGray);
		} 
	}
	return key;
}

Bitmap^ transfer(Bitmap^ originImage, map<int, int> transferImageCollection) {

	map<int, int> imageCollection;

	Bitmap^ image = gcnew Bitmap(originImage->Width, originImage->Height);
	for (int y = 0; y < image->Height; y++) {
		for (int x = 0; x < image->Width; x++) {
			Color RGB = originImage->GetPixel(x, y);
			image->SetPixel(x, y, Color::FromArgb(transferImageCollection[RGB.R], transferImageCollection[RGB.G], transferImageCollection[RGB.B]));
		}
	}

	return image;
}
