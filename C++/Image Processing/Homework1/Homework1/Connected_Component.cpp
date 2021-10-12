#include <iostream> 
#include <vector>
#include <algorithm>

using namespace std;
using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

Bitmap^ get_connected_component(Bitmap^ originImage);
int dfs(int x, int y, vector<vector<int>> &originImageVector);

// Not just transfer between vector and bitmap
Bitmap^ vector_to_bitmap(vector<vector<int>> originImageVector, vector<vector<int>> color_table);
vector<vector<int>> bitmap_to_vector(Bitmap^ originImage);
vector<int> copy_vector(vector<int> origin);

vector<vector<int>> get_color_table(int count_region);


int count_region;

Bitmap^ connected_component(Bitmap^ originImage) {
	return get_connected_component(originImage);
}

Bitmap^ get_connected_component(Bitmap^ originImage) {
	count_region = 0;

	vector<vector<int>> originImageVector = bitmap_to_vector(originImage);

	Bitmap^ image = gcnew Bitmap(originImage->Width, originImage->Height);
	for (int y = 0; y < originImage->Height; y++) {
		for (int x = 0; x < originImage->Width; x++) {
			if (originImageVector[x][y] < -1) {
				dfs(x, y, originImageVector);
				count_region += 1;
			} 
		}
	}

	vector<vector<int>> color_table = get_color_table(count_region);
	return vector_to_bitmap(originImageVector, color_table);
}

int dfs(int x, int y, vector<vector<int>> &originImageVector) {

	if (x >= (int)(originImageVector.size()) || x < 0 || y >= (int)(originImageVector[0].size()) || y < 0 || originImageVector[x][y] == -1 || originImageVector[x][y] == count_region) {
		return 0;
	}
	originImageVector[x][y] = count_region;

	dfs(x + 1, y + 0, originImageVector);
	dfs(x + 0, y + 1, originImageVector);
	dfs(x + 1, y + 1, originImageVector);
	dfs(x + 1, y - 1, originImageVector);
	dfs(x - 1, y + 1, originImageVector);
	dfs(x - 1, y - 1, originImageVector);
	dfs(x - 1, y + 0, originImageVector);
	dfs(x + 0, y - 1, originImageVector);

	return 1;
}

vector<vector<int>> bitmap_to_vector(Bitmap^ originImage) {
	vector<vector<int>> originImageVector;
	int intGray = 0;

	for (int x = 0; x < originImage->Width; x++) {
		vector<int> arr;
		for (int y = 0; y < originImage->Height; y++) {
			intGray = originImage->GetPixel(x, y).R;
			intGray = intGray > 0 ? -1 : -2; // -1 => background, -2 => foreground
			arr.push_back(intGray);
		}
		originImageVector.push_back(copy_vector(arr));
	}

	return originImageVector;
}

Bitmap^ vector_to_bitmap(vector<vector<int>> originImageVector, vector<vector<int>> color_table) {

	Bitmap^ originImage = gcnew Bitmap(originImageVector.size(), originImageVector[0].size());

	int size = color_table.size();

	for (int x = 0; x < originImage->Width; x++) {
		for (int y = 0; y < originImage->Height; y++) {
			int target = originImageVector[x][y];
			if (target >= 0) {
				int intR = color_table[target % size][0];
				int intG = color_table[target % size][1];
				int intB = color_table[target % size][2];
				originImage->SetPixel(x, y, Color::FromArgb(intR, intG, intB));
			} else {
				originImage->SetPixel(x, y, Color::FromArgb(255, 255, 255));
			}
			
		}
	}

	return originImage;
}

vector<int> copy_vector(vector<int> origin) {
	vector<int> copyVector;

	for (int i = 0; i < (int)(origin.size()); i++) {
		copyVector.push_back(origin[i]);
	}

	return copyVector;
}

vector<vector<int>> get_color_table(int count_region) {
	vector<vector<int>> table;
	int delta = 200 / count_region / 3;
	
	table.push_back({ 255,   0,   0 });
	table.push_back({   0, 255,   0 });
	table.push_back({   0,   0, 255 });
	table.push_back({ 255, 255,   0 });
	table.push_back({   0, 255, 255 });
	table.push_back({ 255,   0, 255 });

	return table;
}

