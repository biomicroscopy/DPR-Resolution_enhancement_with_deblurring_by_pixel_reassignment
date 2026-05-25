# DPR Python NVIDIA

NVIDIA GPU-accelerated Python version of Deblurring by Pixel Reassignment
(DPR), implemented with CuPy.

Use this version only on a computer with an NVIDIA GPU and a working NVIDIA
driver. If you are on a MacBook, AMD GPU, or CPU-only machine, use
`../dpr_python_basic` instead.

## Quick Start

First verify that your NVIDIA GPU is visible:

```bash
nvidia-smi
```

Then install and run the demo:

```bash
git clone https://github.com/biomicroscopy/DPR-Resolution_enhancement_with_deblurring_by_pixel_reassignment.git
cd DPR-Resolution_enhancement_with_deblurring_by_pixel_reassignment/Python/dpr_python_nvidia
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 dpr_gpu_demo.py --input test_images/test_image.tif
```

If you already cloned the repository, start at the `cd` command.

The result is written to:

```text
test_images/DPR_results/test_image_result.tif
```

Open TIFF results in FIJI/ImageJ for best compatibility. JPG and PNG results
can be opened with any normal image viewer.

## CuPy and CUDA Version

This folder's `requirements.txt` installs `cupy-cuda12x`, which is correct for
CUDA 12.x.

If your system uses CUDA 11.x, install the matching CuPy package instead:

```bash
python3 -m pip install numpy scipy pillow tifffile imageio matplotlib cupy-cuda11x
```

To check your CUDA compiler version, run:

```bash
nvcc --version
```

The NVIDIA driver is the most important requirement for the prebuilt CuPy
packages. If `nvidia-smi` fails, fix the driver/GPU environment before running
this demo.

## Process Your Own Image

Use `--input` with the path to your image:

```bash
python3 dpr_gpu_demo.py --input /path/to/my_image.tif
```

By default, the output is saved in a `DPR_results` folder next to the input
image, and `_result` is added to the filename.

To choose the output folder and format:

```bash
python3 dpr_gpu_demo.py \
  --input /path/to/my_image.tif \
  --output-dir /path/to/output_folder \
  --output-format tif
```

Supported output formats include `tif`, `jpg`, and `png`.

## Common Parameters

The default parameters are a good starting point:

```bash
python3 dpr_gpu_demo.py \
  --input test_images/test_image.tif \
  --psf 4 \
  --gain 2 \
  --background 10 \
  --temporal mean
```

- `--psf`: point spread function FWHM in pixels. Default: `4`.
- `--gain`: DPR enhancement gain. Default: `2`.
- `--background`: background subtraction radius parameter. Default: `10`.
- `--temporal`: stack reduction mode. Use `mean`, `var`, or `none`. Default:
  `mean`.

Use `--temporal none` if you want to save the full DPR stack instead of a
single reduced image.

## Interactive Mode

You can also run the demo without command-line arguments:

```bash
python3 dpr_gpu_demo.py
```

Interactive mode asks for the input file and parameters. It expects the input
image to be inside:

```text
Python/dpr_python_nvidia/test_images/
```

## Input Files

Sample files are included in `test_images/`:

- `test_image.tif`
- `sarcomere.tif`
- `test_image_jpg.jpg`
- `sarcomere_jpg.jpg`

For your own data, pass the full file path with `--input`. TIFF stacks and
standard Pillow-readable image files such as JPG and PNG are supported.

## Troubleshooting

If `nvidia-smi` is not found or does not show your GPU, this GPU version will
not run. Install or repair the NVIDIA driver, or use `../dpr_python_basic`.

If `ModuleNotFoundError: No module named 'cupy'` appears, install the CuPy
package that matches your CUDA version:

```bash
python3 -m pip install cupy-cuda12x
```

or, for CUDA 11.x:

```bash
python3 -m pip install cupy-cuda11x
```

If the script cannot find your image, pass an absolute path:

```bash
python3 dpr_gpu_demo.py --input /full/path/to/image.tif
```

If TIFF output does not open correctly in your default image viewer, use FIJI:
https://imagej.net/software/fiji/downloads

## Project Structure

```text
dpr_python_nvidia/
|-- dpr_gpu_demo.py
|-- requirements.txt
|-- dpr_gpu_functions/
|   |-- dpr_stack_gpu.py
|   |-- process_image_gpu.py
|   |-- set_parameters_gpu.py
|   `-- update_single_gpu.py
`-- test_images/
    |-- test_image.tif
    |-- sarcomere.tif
    |-- test_image_jpg.jpg
    `-- sarcomere_jpg.jpg
```

## License

This project is licensed under the MIT License. See the repository-level
[LICENSE](../../LICENSE) file for details.
