# DPR Algorithm Implementations in Python

This directory contains two Python implementations of the **Deblurring by Pixel Reassignment (DPR)** algorithm:

- **dpr_python_basic**: CPU-based implementation.
- **dpr_python_nvidia**: NVIDIA GPU implementation using CuPy.

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
│   ├── dpr_gpu_demo.py      # Entry point for GPU demo
│   └── README.md            # Documentation for the GPU version
│
└── README.md                # You're here!
```

## CPU-Based Version: `dpr_python_basic`

- Runs without CUDA.
- No GPU or CUDA required.

See [`dpr_python_basic/README.md`](./dpr_python_basic/README.md) for setup and usage.

## GPU-Based Version: `dpr_python_nvidia`

- Designed for computers with an NVIDIA GPU.
- Uses CuPy for GPU acceleration.

See [`dpr_python_nvidia/README.md`](./dpr_python_nvidia/README.md) for installation, dependencies, and usage instructions.

## Input Images

Sample input images are provided in each implementation's `test_images/` directory. See the implementation-specific README files for usage instructions.

## Getting Started

1. Choose the appropriate version based on your system.
2. Follow the individual README in the subdirectory to install dependencies and run the demo.
3. Use the provided test images or apply DPR to your own stack.

## Contributing

Feel free to open an issue or submit a pull request if you have improvements, bug fixes, or feature suggestions.
