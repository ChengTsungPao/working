#include "Canny.h"

void Find_Canny(Mat image, Mat &smooth_image, Mat &canny_image, char imageType)
{
    //Data Initialize
    if(!image.empty()){ image.zeros(image.rows, image.cols, CV_8UC3);}

    //ROI Setting
    if(ROISWITCH){ image = imageType == 'L' ? image(LEFTCROP) : image(RIGHTCROP);}

    //Remove noise
    medianBlur(image, smooth_image, MEDIAN_KERNEL_SIZE);
    GaussianBlur(smooth_image, smooth_image, Size(GAUSSIAN_KERNEL_SIZE, GAUSSIAN_KERNEL_SIZE), 0, 0);

    //Edge Detection
    Canny(smooth_image, canny_image, LOW_THRESHOLD, HIGH_THRESHOLD);
}
