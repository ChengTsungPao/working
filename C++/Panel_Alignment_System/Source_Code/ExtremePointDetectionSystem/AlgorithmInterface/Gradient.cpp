#include "Gradient.h"

vector<tuple<double, double>> getGradient(Mat image_smooth, vector<Point> contour){

    Mat image_SobelX, image_SobelY;
    cvtColor(image_smooth, image_smooth, CV_BGR2GRAY);
    Sobel(image_smooth, image_SobelX, CV_64F, 1, 0, SOBELSIZE);
    Sobel(image_smooth, image_SobelY, CV_64F, 0, 1, SOBELSIZE);

    int x, y;
    vector<tuple<double, double>> image_Gradient;
    for(unsigned int i = 0; i < contour.size(); i++){
        y = contour[i].x;
        x = contour[i].y;
        image_Gradient.push_back(make_tuple(image_SobelX.at<double>(x, y), image_SobelY.at<double>(x, y)));
//        cout << "index = " << i << " " << image_SobelX.at<double>(x, y) << " " << image_SobelY.at<double>(x, y) << endl;
    }

    return image_Gradient;
}

tuple<vector<double>, vector<double>> getAngleMagnitude(vector<tuple<double, double>> image_Gradient){
    double Gx, Gy;
    vector<double> magnitude, angle;
    for(unsigned int i = 0; i < image_Gradient.size(); i++){
        Gx = get<0>(image_Gradient[i]);
        Gy = get<1>(image_Gradient[i]);
        magnitude.push_back(sqrt(Gx * Gx + Gy * Gy));
        angle.push_back(atan2(Gx, Gy));
//        cout << atan2(Gx, Gy) << endl;
    }

    return { magnitude, angle };

}

int findExtremePointByGradient(vector<tuple<double, double>> image_Gradient) {
    if(image_Gradient.size() == 0){
        return -1;
    }

    double Gx = abs(get<0>(image_Gradient[0]));
    double Gy = abs(get<1>(image_Gradient[0]));
    double minValue = abs(Gx - Gy);
    unsigned int index = 0;
    for(unsigned int i = 1; i < image_Gradient.size(); i++){
        Gx = abs(get<0>(image_Gradient[i]));
        Gy = abs(get<1>(image_Gradient[i]));
        if(abs(Gx - Gy) < minValue){
            minValue = abs(Gx - Gy);
            index = i;
        }
    }

    return index;
}

int findExtremePointByMinMax(tuple<vector<double>, vector<double>> image_angle_magnitude) {
    if(get<0>(image_angle_magnitude).size() == 0) {
        return -1;
    }

    vector<double> angle = get<1>(image_angle_magnitude);
    vector<double> magnitude = get<0>(image_angle_magnitude);

    angle = smoothAngle(angle);

    double maxAngle = angle[0];
    double minAngle = angle[0];
    for(unsigned int i = 1; i < angle.size(); i++) {
        maxAngle = max(maxAngle, angle[i]);
        minAngle = min(minAngle, angle[i]);
    }

    unsigned int index = 0;
    double midAngle = (minAngle + maxAngle) / 2;
    for(unsigned int i = 0; i < angle.size() - 1; i++) {
        if(angle[i] <= midAngle && midAngle <= angle[i + 1]) {
            index = i;
            break;
        }
    }

    return index;
}

vector<double> smoothAngle(vector<double> angle){

    vector<double> adjustAngle;

    int left, right;

    for(unsigned int mid = 0; mid < angle.size(); mid++){
        left = mid - WINDOWSIZE / 2;
        right = mid + WINDOWSIZE / 2;

        // average
        // median

        if(left < 0){
//            adjustAngle.push_back(sumVector(angle, 0, WINDOWSIZE - 1) / WINDOWSIZE);
            adjustAngle.push_back(findMedian(splitVector(angle, 0, WINDOWSIZE - 1)));
        } else if(right >= (int)angle.size()) {
//            adjustAngle.push_back(sumVector(angle, angle.size() - WINDOWSIZE, angle.size() - 1) / WINDOWSIZE);
            adjustAngle.push_back(findMedian(splitVector(angle, angle.size() - WINDOWSIZE, angle.size() - 1)));
        } else{
//            adjustAngle.push_back(sumVector(angle, left, right) / WINDOWSIZE);
            adjustAngle.push_back(findMedian(splitVector(angle, left, right)));
        }

    }

    return adjustAngle;
}

double findMedian(vector<double> arr) {
    int size = arr.size();

    if (size == 0) {
        return 0;
    }
    else {
        sort(arr.begin(), arr.end());
        if (size % 2 == 0) {
            return (arr[size / 2 - 1] + arr[size / 2]) / 2;
        } else {
            return arr[size / 2];
        }
    }
}

