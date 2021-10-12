using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;


Bitmap^ define_thresholding(Bitmap^ originImage, int threshold) {

	Bitmap^ image = gcnew Bitmap(originImage->Width, originImage->Height);

	int intGray;

	for (int y = 0; y < originImage->Height; y++) {
		for (int x = 0; x < originImage->Width; x++) {
			Color RGB = originImage->GetPixel(x, y);
			intGray = (RGB.R >= threshold) ? 255 : 0;
			image->SetPixel(x, y, Color::FromArgb(intGray, intGray, intGray));
		}
	}

	return image;
}
