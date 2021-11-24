#include "opencv2\core\core.hpp"
using namespace cv;
void Canny_Ben( InputArray _src, OutputArray _dst,
                double low_thresh, double high_thresh,
                int aperture_size, bool L2gradient,
				Mat &dx, Mat &dy);