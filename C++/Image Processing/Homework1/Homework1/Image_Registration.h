#pragma once

using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

Bitmap^ image_registration(Bitmap^ originImage, Bitmap^ transferImage, int originPos[4], int transferPos[4]);