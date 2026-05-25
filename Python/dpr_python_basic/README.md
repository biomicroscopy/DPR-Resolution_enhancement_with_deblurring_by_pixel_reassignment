# DPR Python Basic

CPU-only Python version of Deblurring by Pixel Reassignment (DPR). Use this
version if you do not have an NVIDIA GPU, or if you just want the simplest way
to process an image.

## Quick Start

From a terminal, run:

```bash
git clone https://github.com/biomicroscopy/DPR-Resolution_enhancement_with_deblurring_by_pixel_reassignment.git
cd DPR-Resolution_enhancement_with_deblurring_by_pixel_reassignment/Python/dpr_python_basic
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 dpr_demo.py --input test_images/test_image.tif
```

If you already cloned the repository, start at the `cd` command.

The result is written to:

```text
test_images/DPR_results/test_image_result.tif
```

Open TIFF results in FIJI/ImageJ for best compatibility. JPG and PNG results
can be opened with any normal image viewer.

## Process Your Own Image

Use `--input` with the path to your image:

```bash
python3 dpr_demo.py --input /path/to/my_image.tif
```

By default, the output is saved in a `DPR_results` folder next to the input
image, and `_result` is added to the filename.

To choose the output folder and format:

```bash
python3 dpr_demo.py \
  --input /path/to/my_image.tif \
  --output-dir /path/to/output_folder \
  --output-format tif
```

Supported output formats include `tif`, `jpg`, and `png`.

## Common Parameters

The default parameters are a good starting point:

```bash
python3 dpr_demo.py \
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
python3 dpr_demo.py
```

Interactive mode asks for the input file and parameters. It expects the input
image to be inside:

```text
Python/dpr_python_basic/test_images/
```

Interactive mode also offers the optional ML-based denoising path. The
non-interactive command-line path runs standard DPR processing only.

## Input Files

Sample files are included in `test_images/`:

- `test_image.tif`
- `sarcomere.tif`
- `test_image_jpg.jpg`
- `sarcomere_jpg.jpg`

For your own data, pass the full file path with `--input`. TIFF stacks and
standard Pillow-readable image files such as JPG and PNG are supported.

## Troubleshooting

If `python3` is not found, install Python 3.7 or newer from
https://www.python.org/downloads/.

If package installation fails, make sure your virtual environment is active and
run:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

If the script cannot find your image, pass an absolute path:

```bash
python3 dpr_demo.py --input /full/path/to/image.tif
```

If TIFF output does not open correctly in your default image viewer, use FIJI:
https://imagej.net/software/fiji/downloads

## Project Structure

```text
dpr_python_basic/
|-- dpr_demo.py
|-- requirements.txt
|-- dpr_function/
|   |-- dpr_set_parameters.py
|   |-- dpr_stack.py
|   |-- dpr_update_single.py
|   |-- process_image.py
|   `-- process_image_ml_denoise.py
`-- test_images/
    |-- test_image.tif
    |-- sarcomere.tif
    |-- test_image_jpg.jpg
    `-- sarcomere_jpg.jpg
```

## License

This project is licensed under the MIT License. See the repository-level
[LICENSE](../../LICENSE) file for details.
