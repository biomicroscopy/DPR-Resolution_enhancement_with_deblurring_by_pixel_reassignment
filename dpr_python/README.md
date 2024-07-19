
# Python Tools for the DPR Algorithm

## Overview

This directory contains the Python implementation of the Deblurring by Pixel Reassignment (DPR) algorithm.

The project supports various image formats, including TIFF, JPEG, and PNG. Key functionalities include loading image stacks, applying the DPR algorithm, and saving the enhanced images.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [License](#license)

## Project Structure

```plaintext
├── dpr_function/
    ├── dpr_set_parameters.py
    ├── process_image.py
├── test_images/
    ├── test_image.tif
    ├── test_image.jpg
    ├── test_image.png
├── main.py
├── README.md
```

## Setup

Before getting started, ensure you have the following requirements:
1. **Python 3.7 or higher**
    Verify Python installation and version: 
    ```sh
    python3 --version
    ```
    If you don't have Python 3 installed, you can download it from [python.org](https://www.python.org/downloads/).

1. **Required Python packages**
    Install the necessary packages by running:
    ```sh
    pip install -r requirements.txt
    ```
    or run the below CLI
    ```sh
    pip install numpy scipy Pillow tifffile imageio
    ```
1. **Clone the repository:**

    ```bash
    git clone https://github.com/biomicroscopy/Resolution_Enhancement_With_Deblurring.git
    cd /path/to/the/Resolution_Enhancement_With_Deblurring-main
    ```
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
1. Run the Demo script

    To run the DPR processing demo, use the `dpr_demo.py` script. The parameters have been configured in the script.

    ```bash
    python3 dpr_demo.py
    ```
1. Provide the requested information:

    - File Name with Type: You will be prompted to enter the image file name with its type (e.g., test_image.tif). Press Enter to use the default value.
    - Use Default Parameters: You will be asked if you want to use the default DPR parameters. Press Enter to use the default values for psf, gain, background, and temporal.
    - Custom Parameters: If you choose not to use the default parameters, you will need to provide custom values for each parameter as prompted.

    For a demo, please use the default variables.
1. Check the Image process result
    -   The processed images will be saved in a directory named `DPR_results` inside the `test_images`.
    -   The saved image files will have `_result` appended to their original names.
    -   Open jpg/png files using any standard image viewer to inspect the enhanced images. For TIFF files, using FIJI for best compatibility and analysis. For more information on how to download and use FIJI, please check the FIJI section in the [Setup](#setup).

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/biomicroscopy/Resolution_Enhancement_With_Deblurring/blob/main/LICENSE) file for details.

## Contact
If you have any questions or need further assistance, please open an issue in the repository, and we will be happy to help.

