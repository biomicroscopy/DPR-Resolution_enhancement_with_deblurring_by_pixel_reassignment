
# DPR Project

## Overview

This directory contains the Python implementation of the Deblurring by Pixel Reassignment (DPR) algorithm.

The project supports various image formats, including TIFF, JPEG, and PNG. Key functionalities include loading image stacks, applying the DPR algorithm, and saving the enhanced images.

## Table of Contents

- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
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

## Installation

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

## Usage
1. Run the Demo script

    To run the DPR processing demo, use the `dpr_demo.py` script. The parameters have been configured in the script.

    ```bash
    python3 dpr_demo.py
    ```
1. Check the Image process result
    -   The processed images will be saved in a directory named `DPR_results` inside the `test_images`.
    -   The saved image files will have `_result` appended to their original names.
    -   Open these files using any standard image viewer to inspect the enhanced images.
