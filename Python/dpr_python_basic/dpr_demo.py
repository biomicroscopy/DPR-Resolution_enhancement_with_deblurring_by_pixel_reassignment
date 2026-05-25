import argparse
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
    plt.title('DPR_Magnified')

    plt.subplot(1, 3, 3)
    plt.imshow(result_image, cmap='gray')
    plt.title('DPR_Result')

    plt.tight_layout()
    plt.show()


def build_parser():
    parser = argparse.ArgumentParser(description="Run the CPU DPR demo non-interactively.")
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
    from dpr_function import dpr_set_parameters, process_image

    input_path = Path(input_path)
    if not input_path.suffix:
        raise ValueError("Input file must include an extension.")

    data_folder = input_path.parent
    file_name = input_path.stem
    file_type = input_path.suffix.lstrip(".")
    temporal_option = None if temporal == "none" else temporal
    options = dpr_set_parameters.dpr_set_parameters(
        psf,
        gain=gain,
        background=background,
        temporal=temporal_option,
    )

    start_time = time.time()
    print("Running standard DPR processing without ML denoise...")
    result = process_image.process_image(
        data_folder,
        file_name,
        file_type,
        psf,
        options,
        output_dir=output_dir,
        output_format=output_format,
    )

    if result is not None:
        initial_image, dpr_image, magnified_image = result
    else:
        print("Processing failed. No output returned.")
        return

    processing_time = time.time() - start_time
    print(f"\nProcessing Time: {processing_time:.2f} seconds")

    if show_images and initial_image is not None:
        display_images(initial_image, magnified_image, dpr_image)


def run_interactive():
    from dpr_function import dpr_set_parameters, process_image, process_image_ml_denoise

    # Get user inputs
    data_folder = Path(__file__).parent / 'test_images'
    file_name_with_type = get_user_input(
        "Important: The image should be located in the '.../Python/dpr_python_basic/test_images' folder.\n"
        "Enter the file name with type, or press Enter to use the default value:",
        DEFAULT_INPUT,
    )
    file_name, file_type = file_name_with_type.rsplit('.', 1)

    # Ask user if they want to use default parameters
    use_default_params = get_user_input(
        "Would you like to use the default parameters? (y/n/e)\n"
        "Defaults: PSF=4, Gain=2, Background=10, Temporal='mean'\n"
        "y = Use default settings\n"
        "n = Enter custom values\n"
        "e = Learn what these parameters do\n"
        "Press Enter to use the default value",
        "y",
    ).lower()

    if use_default_params == 'e':
        print("\nParameter Explanations:")
        print("- PSF (Point Spread Function): Defines blur radius. Lower values improve resolution, default is 4.")
        print("- Gain: Controls intensity enhancement. Higher values amplify details but may increase noise,"
              " default is 2.")
        print("- Background: Sets the level of background subtraction to improve contrast, default is 10.")
        print("- Temporal: Determines frame processing ('mean' for averaging, 'var' for variance-based enhancement),"
              " default is 'mean'.\n")

        # Ask again after explanation
        use_default_params = get_user_input(
            "Now, would you like to use the default parameters? (y/n) \n"
            "Press Enter to use the default value",
            "y",
        ).lower()

    if use_default_params == 'y':
        psf = DEFAULT_PSF
        gain = DEFAULT_GAIN
        background = DEFAULT_BACKGROUND
        temporal = DEFAULT_TEMPORAL
    else:
        print("Enter the values for the following parameters:")
        psf = float(get_user_input("PSF (Point Spread Function) - Determines the blur radius", str(DEFAULT_PSF)))
        gain = float(get_user_input("Gain - Controls the intensity enhancement", str(DEFAULT_GAIN)))
        background = float(get_user_input("Background - Sets the background level to subtract", str(DEFAULT_BACKGROUND)))
        temporal = get_user_input("Temporal - Temporal analysis method ('mean' or 'var')", DEFAULT_TEMPORAL)

    options = dpr_set_parameters.dpr_set_parameters(psf, gain=gain, background=background, temporal=temporal)

    # Ask user if they want ML-based background denoise.
    use_ml_denoise = get_user_input(
        "Do you want to use ML-based background denoising before processing? (y/n)",
        "n"
    ).lower()

    # Start timing
    start_time = time.time()

    if use_ml_denoise == 'y':
        print("Applying ML-based background denoising before DPR processing...")
        result = process_image_ml_denoise.process_image_ml_denoise(data_folder, file_name, file_type, psf, options)
    else:
        print("Running standard DPR processing without ML denoise...")
        result = process_image.process_image(data_folder, file_name, file_type, psf, options)

    # Check if the process returned results
    if result is not None:
        initial_image, dpr_image, magnified_image = result
    else:
        print("Processing failed. No output returned.")
        return

    # End timing
    end_time = time.time()
    processing_time = end_time - start_time

    print(f"\nProcessing Time: {processing_time:.2f} seconds")

    if initial_image is not None:
        # Display the images
        display_images(initial_image, magnified_image, dpr_image)


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
