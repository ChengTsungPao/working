#include "rgb_extraction_transformation.h"
#include "Variable.h"

#include <iostream>
#include <cmath>

using namespace std;
using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

Bitmap^ rotate_scale_image(Bitmap^ originImage, Bitmap^ transferImage);
double rotate_angle(int originVector[2], int tranferVector[2]);
double scale_value(int originVector[2], int tranferVector[2]);
double vector_length(int _vector[2]);


double angle;
double scale;
double difference;

// originImage -> slanted
Bitmap^ image_registration(Bitmap^ originImage, Bitmap^ transferImage, int originPos[4], int transferPos[4]) {

	int originVector[2] = { originPos[2] - originPos[0], originPos[3] - originPos[1] };
	int tranferVector[2] = { transferPos[2] - transferPos[0], transferPos[3] - transferPos[1] };
	angle = rotate_angle(originVector, tranferVector);
	scale = scale_value(originVector, tranferVector);
	difference = 0;

	return rotate_scale_image(originImage, transferImage);
}

Bitmap^ rotate_scale_image(Bitmap^ originImage, Bitmap^ transferImage) {

	// reverse rotation matrix
	double rotation_matrix[2][2] = {
		{  cos(angle), sin(angle) },
		{ -sin(angle), cos(angle) }
	};

	int originWidth = originImage->Width;
	int originHeight = originImage->Height;

	int originPosX;
	int originPosY;

	int transferWidth = transferImage->Width;
	int transferHeight = transferImage->Height;

	int intGray;

	Bitmap^ image = gcnew Bitmap(transferWidth, transferHeight);
	for (int y = 0; y < transferHeight; y++) {
		for (int x = 0; x < transferWidth; x++) {

			originPosX = (int)((rotation_matrix[1][0] * (y - transferHeight / 2) + rotation_matrix[1][1] * (x - transferWidth / 2)) / scale +  originWidth / 2);
			originPosY = (int)((rotation_matrix[0][0] * (y - transferHeight / 2) + rotation_matrix[0][1] * (x - transferWidth / 2)) / scale + originHeight / 2);

			originPosX = (int)((rotation_matrix[0][0] * (x - transferWidth / 2) + rotation_matrix[0][1] * (y - transferHeight / 2)) / scale +  originWidth / 2);
			originPosY = (int)((rotation_matrix[1][0] * (x - transferWidth / 2) + rotation_matrix[1][1] * (y - transferHeight / 2)) / scale + originHeight / 2);

			if (originPosX >= 0 && originPosX < originWidth && originPosY >= 0 && originPosY < originHeight) {
				intGray = originImage->GetPixel(originPosX, originPosY).R;
			} else {
				intGray = 0;
			}

			image->SetPixel(x, y, Color::FromArgb(intGray, intGray, intGray));
			difference += abs((transferImage->GetPixel(x, y).R) - intGray);

		}
	}
	difference /= transferWidth * transferHeight;

	return image;
}


double rotate_angle(int originVector[2], int tranferVector[2]) {
	return atan2(tranferVector[1], tranferVector[0]) - atan2(originVector[1], originVector[0]);
}

double scale_value(int originVector[2], int tranferVector[2]) {
	return (vector_length(tranferVector)) / (vector_length(originVector));
}

double vector_length(int _vector[2]) {
	return sqrt(_vector[0] * _vector[0] + _vector[1] * _vector[1]);
}





