from GaussianMixtureModel import gaussianMixtureModel, test_gaussianMixtureModel


if __name__ == "__main__":

    path = "./dataset/hw4/"
    soccer1_filename = "soccer1.jpg"
    soccer2_filename = "soccer2.jpg"

    gmm_func = gaussianMixtureModel(path)
    
    # M1 Gaussian Mixture Model 
    gmm_func.getGaussianMixtureModel([soccer1_filename])
    gmm_func.predictGaussianMixtureModel(soccer1_filename)
    gmm_func.plotResult()
    gmm_func.predictGaussianMixtureModel(soccer2_filename)
    gmm_func.plotResult()

    # M2 Gaussian Mixture Model 
    gmm_func.getGaussianMixtureModel([soccer1_filename, soccer2_filename])
    gmm_func.predictGaussianMixtureModel(soccer1_filename)
    gmm_func.plotResult()
    gmm_func.predictGaussianMixtureModel(soccer2_filename)
    gmm_func.plotResult()

    # M2 Difference Components Gaussian Mixture Model 
    test_gaussianMixtureModel(path, soccer1_filename, soccer2_filename, [2, 14])
