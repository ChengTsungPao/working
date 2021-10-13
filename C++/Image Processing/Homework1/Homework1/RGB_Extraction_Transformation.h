#pragma once;
using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

Bitmap^ rgb_extraction_transformation(Bitmap^ originImage, char kind);
Bitmap^ gray_channel(Bitmap^ originImage);