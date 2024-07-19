## Contents
The repository comprises the Matlab functions for DPR
- DPR_demo.m
  Demo script for running the DPR function.
- DPR_function
  This folder consists of the functions of DPR.
  - DPRSetParameters.m
    This function is used to set the full width half maximum (FWHM) of the point spread function (PSF) of the imaging system, the gain level of DPR, the radius of the local-minimum filter, and the option of temporal analysis.
  - DPRStack.m
    This function is used to process an image stack.
  - DPR_UpdateSingle_mex.mexw64
    This function is used to process a single image and is developed for Windows computer using 64bits Matlab.
  - DPR_UpdateSingle_mex.maci64
    This function is used to process a single image and is developed for Macbook using Matlab.
  - DPR_UpdateSingle.m
    This is the source code for DPR.
  - save_tiff_img.m
    This function is used to save the DPR-enhanced image as Tiff.
 - Test_image
   There are two data sets in this folder.
   - sarcomere.tif consists of 15 frames of the engineered cardiac tissue imaged with a confocal microscope. The FWHM of PSF is around 4 pixels.
   - test_image.tif is a simulated data set. It consists of 60 frames of a simulated ring object imaged by a widefield microscope. Both Poisson noise and Gaussian are added to each frame. The FWHM of PSF is 4 pixels.