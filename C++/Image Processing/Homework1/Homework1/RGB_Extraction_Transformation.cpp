using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

Bitmap^ r_channel(Bitmap^ originImage);
Bitmap^ g_channel(Bitmap^ originImage);
Bitmap^ b_channel(Bitmap^ originImage);
Bitmap^ gray_channel(Bitmap^ originImage);

Bitmap^ rgb_extraction_transformation(Bitmap^ originImage, char kind)
{
	switch (kind){
		case 'r':
			return r_channel(originImage);
		case 'g':
			return g_channel(originImage);
		case 'b':
			return b_channel(originImage);
		default:
			return gray_channel(originImage);
	}
}

Bitmap^ r_channel(Bitmap^ originImage)
{
	Bitmap^ image = gcnew Bitmap(originImage->Width, originImage->Height);

	for (int y = 0; y < image->Height; y++) {
		for (int x = 0; x < image->Width; x++) {
			Color RGB = originImage->GetPixel(x, y);

			int invR = Convert::ToInt32(RGB.R);
			int invG = Convert::ToInt32(RGB.R);
			int invB = Convert::ToInt32(RGB.R);

			image->SetPixel(x, y, Color::FromArgb(invR, invG, invB));
		}
	}

	return image;
}

Bitmap^ g_channel(Bitmap^ originImage)
{
	Bitmap^ image = gcnew Bitmap(originImage->Width, originImage->Height);

	for (int y = 0; y < image->Height; y++) {
		for (int x = 0; x < image->Width; x++) {
			Color RGB = originImage->GetPixel(x, y);

			int invR = Convert::ToInt32(RGB.G);
			int invG = Convert::ToInt32(RGB.G);
			int invB = Convert::ToInt32(RGB.G);

			image->SetPixel(x, y, Color::FromArgb(invR, invG, invB));
		}
	}

	return image;
}

Bitmap^ b_channel(Bitmap^ originImage)
{
	Bitmap^ image = gcnew Bitmap(originImage->Width, originImage->Height);

	for (int y = 0; y < image->Height; y++) {
		for (int x = 0; x < image->Width; x++) {
			Color RGB = originImage->GetPixel(x, y);

			int invR = Convert::ToInt32(RGB.B);
			int invG = Convert::ToInt32(RGB.B);
			int invB = Convert::ToInt32(RGB.B);

			image->SetPixel(x, y, Color::FromArgb(invR, invG, invB));
		}
	}

	return image;
}

Bitmap^ gray_channel(Bitmap^ originImage)
{
	Bitmap^ image = gcnew Bitmap(originImage->Width, originImage->Height);

	for (int y = 0; y < image->Height; y++) {
		for (int x = 0; x < image->Width; x++) {
			Color RGB = originImage->GetPixel(x, y);

			int avg = (int)(RGB.R * 0.299 + RGB.G * 0.587 + RGB.B * 0.114);
			int invR = Convert::ToInt32(avg);
			int invG = Convert::ToInt32(avg);
			int invB = Convert::ToInt32(avg);

			image->SetPixel(x, y, Color::FromArgb(invR, invG, invB));
		}
	}

	return image;
}

