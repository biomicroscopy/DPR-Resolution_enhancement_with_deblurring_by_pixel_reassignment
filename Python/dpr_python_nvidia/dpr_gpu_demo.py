import argparse
import importlib.util
from pathlib import Path
import sys
import time


DEFAULT_INPUT = "test_image.tif"
DEFAULT_PSF = 4
DEFAULT_GAIN = 2
DEFAULT_BACKGROUND = 10
DEFAULT_TEMPORAL = "mean"


def get_user_input(prompt, default=None):
    """Get user input with a default value."""
    response = input(f"{prompt} [{default}]: ")
    return response if response else default


def display_images(initial_image, magnified_image, result_image):
    """Display the initial, magnified, and result images for comparison."""
    import matplotlib.pyplot as plt
    import numpy as np

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(initial_image[..., 0], cmap='gray')
    plt.title('Initial')

    plt.subplot(1, 3, 2)
    plt.imshow(np.mean(magnified_image, axis=2), cmap='gray')
    plt.title('DPR Magnified')

    plt.subplot(1, 3, 3)
    plt.imshow(result_image, cmap='gray')
    plt.title('DPR Result')

    plt.tight_layout()
    plt.show()


def load_set_parameters():
    module_path = Path(__file__).parent / "dpr_gpu_functions" / "set_parameters_gpu.py"
    spec = importlib.util.spec_from_file_location("set_parameters_gpu", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.set_parameters


def build_parser():
    parser = argparse.ArgumentParser(description="Run the GPU DPR demo non-interactively.")
    parser.add_argument(
        "--input",
        help="Path to the input image file. If omitted, the demo runs interactively.",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory for DPR output. Defaults to DPR_results next to the input file.",
    )
    parser.add_argument(
        "--output-format",
        help=(
            "Output image format, for example tif, jpg, or png. "
            "Defaults to the input file extension."
        ),
    )
    parser.add_argument(
        "--psf",
        type=float,
        default=DEFAULT_PSF,
        help=f"PSF FWHM in pixels. Default: {DEFAULT_PSF}.",
    )
    parser.add_argument(
        "--gain",
        type=float,
        default=DEFAULT_GAIN,
        help=f"DPR gain. Default: {DEFAULT_GAIN}.",
    )
    parser.add_argument(
        "--background",
        type=float,
        default=DEFAULT_BACKGROUND,
        help=f"Background radius parameter. Default: {DEFAULT_BACKGROUND}.",
    )
    parser.add_argument(
        "--temporal",
        choices=["mean", "var", "none"],
        default=DEFAULT_TEMPORAL,
        help=(
            f"Temporal reduction mode. Default: {DEFAULT_TEMPORAL}. "
            "Use 'none' to save the full stack."
        ),
    )
    return parser


def run_processing(
    input_path,
    output_dir,
    output_format,
    psf,
    gain,
    background,
    temporal,
    show_images,
):
    from dpr_gpu_functions.process_image_gpu import process_image

    set_parameters = load_set_parameters()
    input_path = Path(input_path)
    if not input_path.suffix:
        raise ValueError("Input file must include an extension.")

    data_folder = input_path.parent
    file_name = input_path.stem
    file_type = input_path.suffix.lstrip(".")
    temporal_option = None if temporal == "none" else temporal
    options = set_parameters(psf, gain=gain, background=background, temporal=temporal_option)

    print("Starting DPR processing...")
    start_time = time.time()

    initial_image, dpr_image, magnified_image = process_image(
        data_folder,
        file_name,
        file_type,
        psf,
        options,
        output_dir=output_dir,
        output_format=output_format,
    )

    elapsed_time = time.time() - start_time
    print(f"DPR processing completed in {elapsed_time:.2f} seconds.")

    if show_images and initial_image is not None:
        display_images(initial_image, magnified_image, dpr_image)


def run_interactive():
    script_dir = Path(__file__).parent
    data_folder = script_dir / 'test_images'

    # Get user inputs
    file_name_with_type = get_user_input(
        "The image should be in the 'test_images' folder. \n"
        "Enter the file name with type or press Enter to use the default value:",
        DEFAULT_INPUT,
    )
    input_path = data_folder / file_name_with_type

    # Ask user if they want to use default parameters
    use_default_params = get_user_input(
        "Do you want to use default parameters (psf=4, gain=2, background=10, temporal='mean')? (y/n)",
        "y",
    ).lower()

    if use_default_params == 'y':
        psf = DEFAULT_PSF
        gain = DEFAULT_GAIN
        background = DEFAULT_BACKGROUND
        temporal = DEFAULT_TEMPORAL
    else:
        print("Enter the values for the following parameters:")
        psf = float(get_user_input("PSF (Point Spread Function)", str(DEFAULT_PSF)))
        gain = float(get_user_input("Gain", str(DEFAULT_GAIN)))
        background = float(get_user_input("Background", str(DEFAULT_BACKGROUND)))
        temporal = get_user_input("Temporal ('mean' or 'var')", DEFAULT_TEMPORAL)

    run_processing(input_path, None, None, psf, gain, background, temporal, show_images=True)


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.input is None:
        if len(sys.argv) > 1:
            parser.error("--input is required when running with command-line arguments")
        run_interactive()
        return

    run_processing(
        args.input,
        args.output_dir,
        args.output_format,
        args.psf,
        args.gain,
        args.background,
        args.temporal,
        show_images=False,
    )


if __name__ == '__main__':
    main()
