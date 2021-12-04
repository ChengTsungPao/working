#include "LoadImage.h"

void Image_Load(string image_filename ,Mat &load_image){

        load_image = imread(image_filename);

}
