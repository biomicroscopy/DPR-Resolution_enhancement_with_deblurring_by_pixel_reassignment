# **DPR Algorithm (GPU-Optimized Python Version)**

## **Overview**
This repository provides a **GPU-accelerated** implementation of the [Deblurring by Pixel Reassignment](https://www.spiedigitallibrary.org/journals/advanced-photonics/volume-5/issue-06/066004/Resolution-enhancement-with-deblurring-by-pixel-reassignment/10.1117/1.AP.5.6.066004.full?webSyncID=100c5e17-3e55-b558-b001-3d8b3bd4461b&sessionGUID=d75b2c3e-257a-52be-e460-867d9b436758#_=_) (DPR) algorithm. It supports TIFF, JPEG, and PNG image formats and uses NVIDIA CUDA to enhance processing speed.

Compared to the CPU version, the GPU-optimized implementation runs **10-100x faster**, depending on the image size and hardware.

## Hardware Requirements
This version requires a **computer with an NVIDIA GPU** (e.g., RTX 3080, Tesla V100).
If your system **does not** have an NVIDIA GPU (e.g., MacBook, AMD GPU), use the `dpr_python_basic` version instead.

## Project Structure
```plaintext
├── dpr_gpu_functions/
│   ├── set_parameters_gpu.py
│   ├── process_image_gpu.py
│   ├── dpr_stack_gpu.py
│   ├── dpr_update_single_gpu.py
├── test_images/
│   ├── DPR_results/
├── dpr_demo.py
├── README.md
```

## Setup

Before getting started, ensure you have the following requirements:

### 1. Python 3.7 or higher
Verify Python installation and version:
```sh
python --version
```
If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/).

### 2. Clone the repository:
```bash
git clone https://github.com/biomicroscopy/Resolution_Enhancement_With_Deblurring.git
cd Resolution_Enhancement_With_Deblurring-main/dpr_python
```

### 3. Upgrade pip:
```sh
pip install --upgrade pip
```

### 4. Required Python packages:
Install the necessary packages:
```sh
pip install -r requirements.txt
```
or manually via:
```sh
pip install numpy scipy Pillow tifffile imageio matplotlib cupy-cuda12x
```

**Important:**
*Replace `cupy-cuda12x` with the version that matches your installed CUDA toolkit (e.g., `cupy-cuda11x` for CUDA 11.x). To determine your CUDA version, refer to the [Confirm CUDA Installation](#confirm-cuda-installation) section. For more details, check the [CuPy Installation Guide](https://docs.cupy.dev/en/stable/install.html).*

### 5. FIJI (Optional):
FIJI is recommended for viewing TIFF images.

- Download FIJI from the [official page](https://imagej.net/software/fiji/downloads).
- Install and open TIFF files by dragging and dropping them into the FIJI interface.

## CUDA and GPU Acceleration

To leverage GPU acceleration:

### 1. Verify NVIDIA GPU:
Check if your system has an NVIDIA GPU:
```sh
nvidia-smi
```

### 2. Install CUDA Toolkit:

- Visit the [CUDA Toolkit Downloads page](https://developer.nvidia.com/cuda-downloads).
- Select your operating system and follow the installation instructions provided.

### 3. Confirm CUDA Installation:
After installation, verify your CUDA version:
```sh
nvcc --version
```

Ensure your CuPy installation matches your CUDA version as mentioned earlier.

## Usage

### Running the Demo:
Execute the DPR processing demo script:
```bash
python dpr_demo_nvidia.py
```

### Provide Input Parameters:
- **File Name with Type**: Prompted during execution (e.g., `test_image.tif`). Press Enter for default.
- **Use Default Parameters**: Recommended for demo purposes (`psf=4, gain=2, background=10, temporal='mean'`). Press Enter to accept defaults or manually input custom values.

### Viewing Results:
- Processed images are saved in the `DPR_results` directory inside `test_images`.
- Saved images have `_result` appended to their original filenames.
- JPG/PNG images can be viewed with standard image viewers. TIFF files are best viewed using FIJI.

## License

This project is licensed under the MIT License. See [LICENSE](https://github.com/biomicroscopy/Resolution_Enhancement_With_Deblurring/blob/main/LICENSE) for details.

## Contact

For questions or customized support, please open an issue on the GitHub repository or via email. We're happy to help!
