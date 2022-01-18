#include "AlgorithmInterface.h"

Point getExtremePoint(string path, char imageType, bool visiable) {

    Mat image;                                             // origin image

    // Load Image
    Image_Load(path, image);

    return getExtremePoint(image, imageType, visiable);
}


Point getExtremePoint(Mat image, char imageType, bool visiable) {

    Mat smooth_image;                                      // smooth of image
    Mat contour_image;                                     // draw contour on image
    Mat result_image;                                      // draw result on image

    vector<Point> image_contour;                           // best contour of image
    vector<Vec4i> bestTwoLines;                            // best two lines of houghLinesP
    int image_extremePoint_index;                          // image_contour[image_extremePoint_index] => extremePoint

    vector<tuple<double, double>> image_Gradient;          // Gradient of image_contour
    tuple<vector<double>, vector<double>> image_result;    // (magnitude, angle)



    // Find Contour
    Find_Contour_Button(image, smooth_image, image_contour, bestTwoLines, imageType);
    contour_image = smooth_image.clone();

    // Get Contour Gradient
    image_Gradient = getGradient(smooth_image, image_contour);
    image_result = getAngleMagnitude(image_Gradient);

    // Find Extreme Point
    image_extremePoint_index = findExtremePointByGradient(image_Gradient);



    // Draw Image
    if(visiable){
        result_image = smooth_image.clone();

        drawContour(contour_image, image_contour);
        drawLines(contour_image, bestTwoLines);
        drawMarker(result_image,image_contour[image_extremePoint_index],Scalar(0,255,0),MARKER_TILTED_CROSS,12,7,8);
        showImage(image, smooth_image, contour_image, result_image);
    }

    return image_contour[image_extremePoint_index];

}


void showImage(Mat image, Mat smooth_image, Mat contour_image, Mat result_image){

    imshow("origin Image", image);
    imshow("smooth image", smooth_image);
    imshow("contour Image", contour_image);
    imshow("result Image", result_image);

}





