# MATLAB Tools for the DPR Algorithm

Welcome to the MATLAB section of the "Resolution Enhancement With Deblurring" project. This part of the repository contains MATLAB scripts designed to deblur and enhance the resolution of images, particularly useful in biomicroscopy and other scientific imaging applications.

## Getting Started

### Prerequisites

- MATLAB (Recommended version: R2020a or later)
  - Ensure MATLAB is installed on your computer. For installation details, refer to the [official MathWorks installation guide](https://www.mathworks.com/help/install/).

### Installation

1. **Clone the Repository**
   
   If you have not already cloned the entire project repository, you can clone it or just download this specific MATLAB directory.
     ```bash
     git clone https://github.com/biomicroscopy/Resolution_Enhancement_With_Deblurring.git
     cd Resolution_Enhancement_With_Deblurring/MatLab
     ```
1. **Set Up MATLAB**
   
   Open MATLAB and set your current folder to the directory where you cloned the repository, specifically navigating to the MATLAB folder.
  
1. **FIJI**

   If you are processing TIFF (e.g. test_image.tif) files, it is recommended to use FIJI for viewing the results. FIJI is an enhanced version of ImageJ, bundled with many plugins to facilitate scientific image analysis.
    1. Download FIJI:
       - Visit the FIJI [download page](https://imagej.net/software/fiji/downloads).
       - Choose the appropriate version for your operating system (Windows, MacOS, or Linux).
    1. Install FIJI:
       - Follow the instructions provided on the download page to install FIJI on your system.
    1. Open Your TIFF Files:
       - After installing FIJI, you can open the TIFF files by simply dragging and dropping them onto the FIJI frontend.

## Usage
To use the MATLAB scripts for image deblurring
  1. Open the Script: Open the DPR_demo.m script included in the directory.
  1. Run the Script: Execute the script in MATLAB's command window to start the deblurring process. Modify the script as necessary to point to your specific image files or to adjust parameters.
  1. Check the Image process result. For TIFF files, use FIJI for best compatibility and analysis. For more information on how to download and use FIJI, please check the FIJI section in the [Setup](#setup).

## Contents
The repository comprises the Matlab functions for DPR
- DPR_demo.m
  Demo script for running the DPR function.
- DPR_function
  This folder consists of the functions of DPR.
  - DPRSetParameters.m
    This function is used to set the full-width half maximum (FWHM) of the point spread function (PSF) of the imaging system, the gain level of DPR, the radius of the local-minimum filter, and the option of temporal analysis.
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
   There are two data sets in this folder. It is recommended to use FIJI for viewing the TIFF 
   - sarcomere.tif consists of 15 frames of the engineered cardiac tissue imaged with a confocal microscope. The FWHM of PSF is around 4 pixels.
   - test_image.tif is a simulated data set. It consists of 60 frames of a simulated ring object imaged by a widefield microscope. Both Poisson noise and Gaussian are added to each frame. The FWHM of PSF is 4 pixels.

## Contributing
Contributions are welcome! If you have improvements, bug fixes, or enhancements, please fork the repository, make your changes, and submit a pull request. For significant changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/biomicroscopy/Resolution_Enhancement_With_Deblurring/blob/main/LICENSE) file for details.

## Contact
If you have any questions or need further assistance, please open an issue in the repository, and we will be happy to help.
