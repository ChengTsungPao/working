#include "Contour.h"

void Find_Contour_Button(Mat image, Mat &image_smooth, vector<Point> &image_contour, char imageType)
{

    //Data Initialize
    if(!image.empty()){ image.zeros(image.rows, image.cols, CV_8UC3);}

    //ROI Setting
    image = imageType == 'L' ? image(Rect(0,0,1080,660)) : image(Rect(200,0,1080,660));

    //Remove noise
    medianBlur(image,image_smooth,11);
    GaussianBlur(image_smooth,image_smooth,Size(3,3),0,0);

    //Edge Detection
    Mat image_canny;
    Canny(image_smooth, image_canny, 80, 130);

    //Find Contour
    vector<vector<Point>> image_contours;
    findContours(image_canny, image_contours, RETR_EXTERNAL, CHAIN_APPROX_NONE);

    vector<int> shape = {image.rows, image.cols};
    image_contour = findBestContour(image_contours, shape);
    image_contour = imageType == 'L' ? orderContour(image_contour, shape[0], shape[1]) : orderContour(image_contour, shape[0], 0);

}

vector<Point> findBestContour(vector<vector<Point>> contours, vector<int> shape){
    cout << shape[0] << " " << shape[1] << endl;
    vector<Point> ans = contours[0];

    for(unsigned int i = 1; i < contours.size(); i++){
        if(contours[i].size() > ans.size()){
            ans = contours[i];
        }
    }
    return ans;
}

void HoughLinesPHandler(vector<int> shape, vector<vector<Point>> contours, unsigned int contourIndex){
    int minLineLength = 10;
    int maxLineGap = 1;

    vector<vector<int>> image(shape[0], vector<int> (shape[1], 0));
    drawContours(image, contours, contourIndex, Scalar(0, 255, 255), 2);
    vector<Vec4i> lines;
    HoughLinesP(image, lines, 1, M_PI / 180, 100, minLineLength, maxLineGap);
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
    double angle;
    vector<tuple<double, Point>> data;
    for(unsigned int i = 0; i < contour.size(); i++){
        x_ = contour[i].x;
        y_ = contour[i].y;
        angle = atan2((y - x_), (x - y_));
        data.push_back(make_tuple(angle, Point(x_, y_)));
    }

    sort(data.begin(), data.end(), TupleCompare<0>());

    vector<Point> ans;
    for(unsigned int i = 0; i < data.size(); i++){
        ans.push_back(get<1>(data[i]));
    }

    return ans;
}

void drawContour(Mat &drawImage, vector<Point> image_contour){
    vector<vector<Point>> contours;
    contours.push_back(image_contour);
    drawContours(drawImage,contours,0,Scalar(0, 255, 0), 2);

    for(unsigned int i = 0; i < image_contour.size(); i += 100){
        std::string tmp = std::to_string(i);
        char const *num_text = tmp.c_str();
        putText(drawImage, num_text, image_contour[i], FONT_HERSHEY_PLAIN, 1, Scalar(255, 0, 0), 1);
    }
}




