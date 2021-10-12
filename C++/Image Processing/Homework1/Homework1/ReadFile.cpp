#include <string>
#include <iostream>
#include <vector>

#include "Function.h"
#include "Dirent.h"

using namespace std;
using namespace System;
using namespace System::Windows::Forms;
using namespace System::Drawing;

Bitmap^ readImage(String^ path, String^ filename) {
	return gcnew Bitmap(path + filename);
}

vector<string> getFolderFiles(string path) {

	DIR* dir = opendir(path.c_str());

	vector<string> files;
	if (dir == NULL) {
		return files;
	}

	struct dirent* entry;
	entry = readdir(dir);
	while (entry != NULL) {
		if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0) {
			// cout << entry->d_name << endl;
			files.push_back(entry->d_name);
		}
		entry = readdir(dir);
	}
	closedir(dir);

	return files;
}