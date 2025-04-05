# DPR Algorithm Implementations in Python

This directory contains two versions of the **Deblurring by Pixel Reassignment (DPR)** algorithm implemented in Python:

- 🖥️ **dpr_python_basic**: CPU-based implementation, compatible with most environments  
- ⚡ **dpr_python_nvidia**: GPU-accelerated implementation using NVIDIA CUDA and CuPy  

These tools are designed to enhance image resolution by applying DPR processing to image stacks (TIFF, JPEG, PNG).

## 📁 Repository Structure

```plaintext
Python/
├── dpr_python_basic/        # CPU-based DPR version (cross-platform)
│   ├── dpr_function/        # Core DPR processing logic
│   ├── test_images/         # Sample input images, and output images
│   ├── dpr_demo.py          # Entry point for running DPR
│   └── README.md            # Documentation for the basic version
│
├── dpr_python_nvidia/       # GPU-accelerated DPR version using CuPy
│   ├── dpr_gpu_functions/   # GPU-optimized processing logic
│   ├── test_images/         # Sample input images, and output images
<<<<<<< HEAD
│   ├── dpr_demo.py          # Entry point for GPU demo
=======
│   ├── dpr_gpu_demo.py          # Entry point for GPU demo
>>>>>>> efaa4e3 (Refactor the python libraries.)
│   └── README.md            # Documentation for the GPU version
│
└── README.md                # You're here!
```

## 🖥️ CPU-Based Version: `dpr_python_basic`

- Works on most computers, including Windows, Linux, and Mac.
- No GPU or CUDA required.
- Easy to set up and run with standard Python libraries.

> 📄 See [`dpr_python_basic/README.md`](./dpr_python_basic/README.md) for setup and usage.

## ⚡ GPU-Based Version: `dpr_python_nvidia`

- Designed for computers with an NVIDIA GPU.
- Uses CuPy for GPU acceleration.
- Much faster than the CPU version, especially on large images.

> 📄 See [`dpr_python_nvidia/README.md`](./dpr_python_nvidia/README.md) for installation, dependencies, and usage instructions.

## 🖼️ Supported Image Formats

Both versions support:
- TIFF (.tif)
- JPEG (.jpg)
- PNG (.png)

## 🛠 Getting Started

1. Choose the appropriate version based on your system.
2. Follow the individual README in the subdirectory to install dependencies and run the demo.
3. Use the provided test images or apply DPR to your own stack.

## 🤝 Contributing

Feel free to open an issue or submit a pull request if you have improvements, bug fixes, or feature suggestions.
