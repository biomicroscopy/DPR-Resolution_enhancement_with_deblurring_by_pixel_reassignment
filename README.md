# Resolution Enhancement Algorithm - Deblurring by Pixel Reassignment (DPR)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![DOI](https://img.shields.io/badge/DOI-10.1117%2F1.AP.5.6.066004-blue)](https://doi.org/10.1117/1.AP.5.6.066004)

This repository contains MATLAB, Python, and ImageJ/Fiji implementations of Deblurring by Pixel Reassignment (DPR), an image resolution enhancement method described in the publication below.

## Citation

If you use this software or method in your research, please cite:

> Zhao, B. & Mertz, J. _Resolution enhancement with deblurring by pixel reassignment (DPR)._ Advanced Photonics **5**(6), 066004 (2023).  
> 🔗 [10.1117/1.AP.5.6.066004](https://doi.org/10.1117/1.AP.5.6.066004)

## Overview
Deblurring by pixel reassignment (DPR) performs PSF sharpening by reassigning pixel intensities after image acquisition. The pixel reassignment step size depends on the local log-image gradient. See the paper for the scientific method, assumptions, and validation.

## DPR Result Example
<img src="https://github.com/biomicroscopy/DPR-Resolution_enhancement_with_deblurring_by_pixel_reassignment/blob/main/imgs/dpr_result_02.png" width=75%>
  
## Repository Contents
  - `Python/`: CPU and NVIDIA GPU Python implementations.
  - `MatLab/`: MATLAB scripts and functions.
  - `ImageJ/`: ImageJ/Fiji plugin source code.
  - `imgs/`: documentation images.

## Getting Started
To begin using the tools provided in this repository, please navigate to the specific directory of interest:

  - Python implementations: [Python/README.md](Python/README.md).
  - Python NVIDIA GPU implementation: [Python/dpr_python_nvidia/README.md](Python/dpr_python_nvidia/README.md).
  - MATLAB implementation: [MatLab/README.md](MatLab/README.md).
  - ImageJ/Fiji plugin: [ImageJ/README.md](ImageJ/README.md).

These individual README files will provide you with detailed instructions on setting up and running the applications.

## Contributing

Contributions are highly welcome! If you have enhancements, bug fixes, or improvements, please feel free to fork the repository and submit a pull request. You can also open an issue for bugs you might find or for feature requests.

## User Feedback

Your feedback helps guide our development and improvements. Please take a moment to fill out the [DPR Algorithm User Feedback](https://docs.google.com/forms/d/e/1FAIpQLSf3UcPsnofb7Hb-OURkfZoRNM6LJbGQPdsjCArrfbeH6jkigQ/viewform?usp=header) questionnaire to help us better understand your needs and further improve DPR.

## License
This project is made available under the MIT License. For more details, see the [LICENSE](LICENSE) file.

## Contact
If you have any comments, suggestions, or questions, please do contact us at byzhao@bu.edu.
