# Resolution Enhancement Algorithm - Deblurring by Pixel Reassignment (DPR)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![DOI](https://img.shields.io/badge/DOI-10.1117%2F1.AP.5.6.066004-blue)](https://doi.org/10.1117/1.AP.5.6.066004)

Welcome to the repository for Resolution Enhancement Algorithm - Deblurring by Pixel Reassignment (DPR) — an image resolution enhancement algorithm that sharpens the Point Spread Function (PSF) with minimal noise amplification and no model-based deconvolution.

## Citation

If DPR accelerates your research, please cite:

> Zhao, B. & Mertz, J. _Resolution enhancement with deblurring by pixel reassignment (DPR)._ Advanced Photonics **5**(6), 066004 (2023).  
> 🔗 [10.1117/1.AP.5.6.066004](https://doi.org/10.1117/1.AP.5.6.066004)

## Overview
This repository hosts a suite of tools and algorithms aimed at enhancing the resolution of images. We strive to provide clearer and more detailed visual data, which can significantly improve data analysis and research outcomes in various fields.

Deblurring by pixel reassignment (DPR) is to perform PSF sharpening similar to deconvolution but in a manner less prone to noise-induced artifacts and without the requirement of a full model for the PSF. The basic principle of DPR is to reassignment the intensity value of pixels post-image acquisition. The pixel reassignment step size is dependent on the local log-image gradient. DPR relies solely on pixel reassignment. As such, no negativities are possible in the final image reconstruction. Moreover, intensity levels are rigorously conserved, with no requirement for additional procedures to ensure local linearity.

## DPR Result Example
<img src="https://github.com/biomicroscopy/DPR-Resolution_enhancement_with_deblurring_by_pixel_reassignment/blob/main/imgs/dpr_result_02.png" width=75%>
  
## Features
  - **Advanced Deblurring Algorithms**: Techniques developed to effectively reduce blur and artifacts in microscopy images.
  - **Documentation**: Each part of the project, whether it's Python or MATLAB code, has its own detailed README to guide you through installation, usage, and customization.

## Getting Started
To begin using the tools provided in this repository, please navigate to the specific directory of interest:

  - Python-based version: [README](https://github.com/biomicroscopy/Resolution_Enhancement_With_Deblurring/blob/main/Python/README.md).
  - Python-based NVIDIA GPU-accelerated version: [README](https://github.com/biomicroscopy/DPR-Resolution_enhancement_with_deblurring_by_pixel_reassignment/blob/main/Python/dpr_python_nvidia/README.md)
  - MATLAB-based version: [README](https://github.com/biomicroscopy/Resolution_Enhancement_With_Deblurring/blob/main/MatLab/README.md).
  - FIJI/ImageJ Plugin: [README](https://github.com/biomicroscopy/DPR-Resolution_enhancement_with_deblurring_by_pixel_reassignment/blob/main/ImageJ/README.md) 

These individual README files will provide you with detailed instructions on setting up and running the applications.

## Contributing

Contributions are highly welcome! If you have enhancements, bug fixes, or improvements, please feel free to fork the repository and submit a pull request. You can also open an issue for bugs you might find or for feature requests.

## User Feedback

Your feedback helps guide our development and improvements. Please take a moment to fill out the [DPR Algorithm User Feedback](https://docs.google.com/forms/d/e/1FAIpQLSf3UcPsnofb7Hb-OURkfZoRNM6LJbGQPdsjCArrfbeH6jkigQ/viewform?usp=header) questionnaire to help us better understand your needs and further improve DPR.

## License
This project is made available under the MIT License. For more details, see the [LICENSE](https://github.com/biomicroscopy/Resolution_Enhancement_With_Deblurring/blob/main/LICENSE) file.

## Contact
If you have any comments, suggestions, or questions, please do contact us at byzhao@bu.edu.
