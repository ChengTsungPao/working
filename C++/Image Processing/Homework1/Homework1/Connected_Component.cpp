#include <iostream> 
#include <vector>
#include <algorithm>
#include <queue>
#include <tuple>
#include <set>

#include "Function.h"
#include "Variable.h"

using namespace std;
using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

Bitmap^ get_connected_component(Bitmap^ originImage);
Bitmap^ colorMap(vector<vector<int>> transferImage, vector<vector<int>> color_table);
vector<vector<int>> markMap(Bitmap^ originImage);
vector<vector<int>> get_color_table(int count_region);
void dfs(int x, int y, vector<vector<int>> &originImageVector);
void bfs(int x, int y, vector<vector<int>> &originImageVector);

int count_region;

Bitmap^ connected_component(Bitmap^ originImage) {
	return get_connected_component(originImage);
}

Bitmap^ get_connected_component(Bitmap^ originImage) {

	count_region = 0;

	vector<vector<int>> markImage = markMap(originImage);

	Bitmap^ image = gcnew Bitmap(originImage->Width, originImage->Height);
	for (int y = 0; y < originImage->Height; y++) {
		for (int x = 0; x < originImage->Width; x++) {
			if (markImage[x][y] < -1) {
				// dfs(x, y, markImage); // Recursion Times Limit
				bfs(x, y, markImage);
				count_region += 1;
			} 
		}
	}

	return colorMap(markImage, get_color_table(count_region));
}

void dfs(int x, int y, vector<vector<int>> &originImageVector) {

	if (x >= (int)(originImageVector.size()) || x < 0 || y >= (int)(originImageVector[0].size()) || y < 0 || originImageVector[x][y] == -1 || originImageVector[x][y] == count_region) {
		return;
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
}

void bfs(int x, int y, vector<vector<int>> &originImageVector) {

	queue<tuple<int, int>> que;
	tuple<int, int> pos;
	set<tuple<int, int>> isVisited;

	que.push(make_tuple(x, y));

	while (que.size() > 0) {
		pos = que.front();
		que.pop();

		x = get<0>(pos);
		y = get<1>(pos);

		if (x >= (int)(originImageVector.size()) || x < 0 || y >= (int)(originImageVector[0].size()) || y < 0 || (isVisited.count(pos) && originImageVector[x][y] != -2) || originImageVector[x][y] == -1) {
			continue;
		}

		originImageVector[x][y] = count_region;

		que.push(make_tuple(x + 1, y + 0));
		que.push(make_tuple(x + 0, y + 1));
		que.push(make_tuple(x + 1, y + 1));
		que.push(make_tuple(x + 1, y - 1));
		que.push(make_tuple(x - 1, y + 1));
		que.push(make_tuple(x - 1, y - 1));
		que.push(make_tuple(x - 1, y + 0));
		que.push(make_tuple(x + 0, y - 1));

		isVisited.insert(make_tuple(x + 1, y + 0));
		isVisited.insert(make_tuple(x + 0, y + 1));
		isVisited.insert(make_tuple(x + 1, y + 1));
		isVisited.insert(make_tuple(x + 1, y - 1));
		isVisited.insert(make_tuple(x - 1, y + 1));
		isVisited.insert(make_tuple(x - 1, y - 1));
		isVisited.insert(make_tuple(x - 1, y + 0));
		isVisited.insert(make_tuple(x + 0, y - 1));

	}

}

vector<vector<int>> markMap(Bitmap^ originImage) {
	vector<vector<int>> originImageVector;
	int intGray = 0;

	for (int x = 0; x < originImage->Width; x++) {
		vector<int> arr;
		for (int y = 0; y < originImage->Height; y++) {
			intGray = originImage->GetPixel(x, y).R;
			//if (intGray != 0 && intGray != 255) {
			//	cout << intGray << endl;
			//}
			intGray = intGray > 0 ? -1 : -2; // -1 => background, -2 => foreground
			arr.push_back(intGray);
		}
		originImageVector.push_back(arr);
	}

	return originImageVector;
}

Bitmap^ colorMap(vector<vector<int>> transferImage, vector<vector<int>> color_table) {

	Bitmap^ image = gcnew Bitmap(transferImage.size(), transferImage[0].size());

	int size = color_table.size();

	for (int x = 0; x < image->Width; x++) {
		for (int y = 0; y < image->Height; y++) {
			int target = transferImage[x][y];
			if (target >= 0) {
				int intR = color_table[target % size][0];
				int intG = color_table[target % size][1];
				int intB = color_table[target % size][2];
				image->SetPixel(x, y, Color::FromArgb(intR, intG, intB));
			}
			else {
				image->SetPixel(x, y, Color::FromArgb(255, 255, 255));
			}

		}
	}

	return image;
}

vector<vector<int>> get_color_table(int count_region) {
	vector<vector<int>> table;
	int parts = (int)(count_region / 6) + 1;
	int delta = (int)(250 / parts);
	
	table.push_back({ 255,   0,   0 });
	table.push_back({   0, 255,   0 });
	table.push_back({   0,   0, 255 });
	table.push_back({ 255, 255,   0 });
	table.push_back({   0, 255, 255 });
	table.push_back({ 255,   0, 255 });

	for (int i = 0; i < 6; i++) {
		for (int j = 0; j < parts; j++) {
			vector<int> color;
			for (int k = 0; k < 3; k++) {
				if (table[i][k] == 255) {
					color.push_back(table[i][k] - delta * j);
				} else {
					color.push_back(table[i][k]);
				}

			}
			table.push_back(color);
		}
	}

	return table;
}

