#pragma once
#include <map>
using namespace std;


// Connected Component
extern int count_region;

// Histogram Equalization
extern map<int, int> originImageCollection;
extern map<int, int> transferImageCollection;


// Image Registration
extern double angle;
extern double scale;
extern double difference;