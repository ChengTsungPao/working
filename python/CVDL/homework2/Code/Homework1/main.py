from PCA import pca

if __name__ == "__main__":

    path = ".//Dataset_CvDl_Hw2//Q4_Image//"
    pca_fcn = pca(path)
    pca_fcn.image_reconstruction()
    pca_fcn.compute_reconstruction_error()