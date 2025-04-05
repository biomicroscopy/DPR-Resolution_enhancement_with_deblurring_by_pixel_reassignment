import matplotlib.pyplot as plt
import numpy as np
import time
from dpr_function import dpr_set_parameters, process_image, process_image_ml_denoise


def get_user_input(prompt, default=None):
    """Get user input with a default value."""
    response = input(f"{prompt} [{default}]: ")
    return response if response else default


def display_images(initial_image, magnified_image, result_image):
    """Display the initial, magnified, and result images for comparison."""
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


def main():
    # Get user inputs
    data_folder = 'test_images'
    file_name_with_type = get_user_input(
        "Important: The image should be located in the '.../Python/dpr_python_basic/test_images' folder.\n"
        "Enter the file name with type, or press Enter to use the default value:", "test_image.tif"
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
        "y"
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
            "y"
        ).lower()

    if use_default_params == 'y':
        psf = 4
        gain = 2
        background = 10
        temporal = 'mean'
    else:
        print("Enter the values for the following parameters:")
        psf = float(get_user_input("PSF (Point Spread Function) - Determines the blur radius", "4"))
        gain = float(get_user_input("Gain - Controls the intensity enhancement", "2"))
        background = float(get_user_input("Background - Sets the background level to subtract", "10"))
        temporal = get_user_input("Temporal - Temporal analysis method ('mean' or 'var')", "mean")

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


if __name__ == '__main__':
    main()
