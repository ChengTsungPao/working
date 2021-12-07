#include "TestResult.h"
#include <iostream>
#include <time.h>

void test_all_data(){
    cout << "This is test result function !!!" << endl;

    string str;
    vector<string> paths;
    Point result;

    ifstream file("../../Test Image_20210913/all_image_path.txt");
    while (getline(file, str)){
        paths.push_back(str);
    }

    double start = clock();
    for(unsigned int i = 0; i < paths.size(); i++){
        result = getExtremePoint(paths[i] + "L.png", 'L');
        cout << paths[i] + "L.png" << ": " << result << endl;
        result = getExtremePoint(paths[i] + "R.png", 'R');
        cout << paths[i] + "R.png" << ": " << result << endl;
    }
    cout << "Time: " << clock() - start << endl;
}
