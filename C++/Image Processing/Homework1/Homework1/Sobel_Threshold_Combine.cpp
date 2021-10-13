#include "Define_Thresholding.h"
#include "Sobel_Edge_Detection.h"

using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

Bitmap^ combine_image(Bitmap^ originImage, Bitmap^ transferImage);


Bitmap^ sobel_threshold_combine(Bitmap^ originImage, int threshold) {

	Bitmap^ sobelImage = sobel_edge_dection(originImage, 'c');
	Bitmap^ thresholdImage = define_thresholding(sobelImage, threshold);

	return combine_image(originImage, thresholdImage);
}


Bitmap^ combine_image(Bitmap^ originImage, Bitmap^ transferImage) {

	Bitmap^ image = gcnew Bitmap(originImage->Width, originImage->Height);

	for (int y = 0; y < originImage->Height; y++) {
		for (int x = 0; x < originImage->Width; x++) {
			Color originRGB = originImage->GetPixel(x, y);
			Color transferRGB = transferImage->GetPixel(x, y);
			if (transferRGB.R == 255) {
				image->SetPixel(x, y, Color::FromArgb(0, 255, 0));
			} else {
				image->SetPixel(x, y, Color::FromArgb(originRGB.R, originRGB.G, originRGB.B));
			}
		}
	}

	return image;
}