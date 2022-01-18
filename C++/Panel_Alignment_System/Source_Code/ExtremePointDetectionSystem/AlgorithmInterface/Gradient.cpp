#include "Gradient.h"

vector<tuple<double, double>> getGradient(Mat image_smooth, vector<Point> contour){

    Mat image_SobelX, image_SobelY;
    cvtColor(image_smooth, image_smooth, CV_BGR2GRAY);
    Sobel(image_smooth, image_SobelX, CV_64F, 1, 0, 11);
    Sobel(image_smooth, image_SobelY, CV_64F, 0, 1, 11);

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
