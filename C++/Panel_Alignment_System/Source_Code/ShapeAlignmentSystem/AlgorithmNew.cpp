#include <QFileDialog>
#include <QJsonObject>
#include <QJsonDocument>
#include <QJsonArray>
#include <QFile>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <vector>
#include <tuple>
#include <Canny_Ben.h>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <math.h>
//#include <opencv2/core/mat.hpp>

using namespace std;
using namespace cv;

Mat Image_Load(QString left_image_filename ,QString right_image_filename);
vector<Point> findBestContour(vector<vector<Point>> contours);
vector<Point> orderContour(vector<Point> contour, int x, int y);
void Find_Contour_Button(Mat left_image, Mat right_image);
vector<tuple<double, double>> getGradient(Mat image_smooth, vector<Point> contour);
tuple<vector<double>, vector<double>> getAngleMagnitude(vector<tuple<double, double>> image_Gradient);

Mat Image_Load(QString left_image_filename ,QString right_image_filename){

        Mat g_InImg1 = cv::imread(left_image_filename.toStdString());
        Mat g_InImg2 = cv::imread(right_image_filename.toStdString());

}

vector<Point> findBestContour(vector<vector<Point>> contours){
    vector<Point> ans = contours[0];

    for(unsigned int i = 1; i < contours.size(); i++){
        if(contours[i].size() > ans.size()){
            ans = contours[i];
        }
    }
    return ans;
}

template<int M, template<typename> class F = std::less>
struct TupleCompare
{
    template<typename T>
    bool operator()(T const &t1, T const &t2)
    {
        return F<typename tuple_element<M, T>::type>()(std::get<M>(t1), std::get<M>(t2));
    }
};

vector<Point> orderContour(vector<Point> contour, int x, int y){
    int x_, y_;
    float angle;
    vector<tuple<float, Point>> data;
    for(unsigned int i = 0; i < contour.size(); i++){
        x_ = contour[i].x;
        y_ = contour[i].y;
        angle = atan2((x - x_), (y - y_));
        data.push_back(make_tuple(angle, Point(x_, y_)));
    }

    sort(data.begin(), data.end(), TupleCompare<0>());

    cout << get<0>(data[0]) << " " << get<0>(data[100]) << " " << get<0>(data[200]) << endl;
    cout << get<0>(data[300]) << " " << get<0>(data[400]) << " " << get<0>(data[500]) << endl;

    vector<Point> ans;
    for(unsigned int i = 0; i < data.size(); i++){
        ans.push_back(get<1>(data[i]));
    }
    cout << ans[0].x << " " << ans[100].x << " " << ans[200].x << endl;
    cout << ans[300].x << " " << ans[400].x << " " << ans[500].x << endl;
    return ans;
}

void Find_Contour_Button(Mat image, char imageType)
{

    //Data Initialize
    if(!image.empty()){ image.zeros(image.rows, image.cols, CV_8UC3);}

    //ROI Setting
    image = imageType == 'L' ? image(cv::Rect(0,0,1080,660)) : image(cv::Rect(200,0,1080,660));

    //Remove noise
    Mat image_smooth;
    cv::medianBlur(image,image_smooth,11);
    cv::GaussianBlur(image_smooth,image_smooth,Size(3,3),0,0);
    Mat test = image_smooth.clone();

    //Edge Detection
    Mat image_canny;
    Mat image_SobelX, image_SobelY;
    Canny_Ben(image_smooth,image_canny,70,130,3,0,image_SobelX,image_SobelY); //get the Gx, Gy
    image_SobelX.convertTo(image_SobelX,CV_64F);
    image_SobelY.convertTo(image_SobelY,CV_64F);
    cv::imshow("image_canny",image_canny);

    //Find Contour
    vector<vector<Point>> image_contours;
    cv::findContours(image_canny, image_contours, RETR_EXTERNAL, CHAIN_APPROX_NONE);

    vector<Point> image_contour = findBestContour(image_contours);
    image_contour = imageType == 'L' ? orderContour(image_contour, 0, 0) : orderContour(image_contour, 1080, 0);

    vector<vector<Point>> contours;
    contours.push_back(image_contour);
    cv::drawContours(image,contours,0,Scalar(0, 255, 0), 5);

    for(unsigned int i = 0; i < image_contour.size(); i += 100){
        std::string tmp = std::to_string(i);
        char const *num_text = tmp.c_str();
        cv::putText(image, num_text, image_contour[i],FONT_HERSHEY_PLAIN,1,Scalar(255, 0, 0),1);
    }

    cv::imshow("image",image);

    vector<tuple<double, double>> image_Gradient = getGradient(test, image_contour);
    tuple<vector<double>, vector<double>> result = getAngleMagnitude(image_Gradient);

}

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
//        cout << image_SobelX.at<double>(x, y) << " " << image_SobelY.at<double>(x, y) << endl;
    }

    return image_Gradient;
}

tuple<vector<double>, vector<double>> getAngleMagnitude(vector<tuple<double, double>> image_Gradient){
    float Gx, Gy;
    vector<double> magnitude, angle;
    for(unsigned int i = 0; i < image_Gradient.size(); i++){
        Gx = get<0>(image_Gradient[i]);
        Gy = get<1>(image_Gradient[i]);
        magnitude.push_back(sqrt(Gx * Gx + Gy * Gy));
        angle.push_back(atan2(Gx, Gy));
        cout << atan2(Gx, Gy) << endl;
    }

    return make_tuple(magnitude, angle);

}

//tuple<vector<Point>, vector<Point>> getGradientCanny(){

//}


