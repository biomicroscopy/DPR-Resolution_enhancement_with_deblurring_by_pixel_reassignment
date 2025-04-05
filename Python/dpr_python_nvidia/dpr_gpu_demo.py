import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from dpr_gpu_functions.set_parameters_gpu import set_parameters
from dpr_gpu_functions.process_image_gpu import process_image
import time


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
    plt.title('DPR Magnified')

    plt.subplot(1, 3, 3)
    plt.imshow(result_image, cmap='gray')
    plt.title('DPR Result')

    plt.tight_layout()
    plt.show()


def main():
    script_dir = Path(__file__).parent
    data_folder = script_dir / 'test_images'

    # Get user inputs
    file_name_with_type = get_user_input(
        "The image should be in the 'test_images' folder. \nEnter the file name with type or press Enter to use the default value:",
        "test_image.tif"
    )
    file_name, file_type = file_name_with_type.rsplit('.', 1)

    # Ask user if they want to use default parameters
    use_default_params = get_user_input(
        "Do you want to use default parameters (psf=4, gain=2, background=10, temporal='mean')? (y/n)",
        "y"
    ).lower()

    if use_default_params == 'y':
        psf = 4
        gain = 2
        background = 10
        temporal = 'mean'
    else:
        print("Enter the values for the following parameters:")
        psf = float(get_user_input("PSF (Point Spread Function)", "4"))
        gain = float(get_user_input("Gain", "2"))
        background = float(get_user_input("Background", "10"))
        temporal = get_user_input("Temporal ('mean' or 'var')", "mean")

    options = set_parameters(psf, gain=gain, background=background, temporal=temporal)

    print("Starting DPR processing...")
    start_time = time.time()

    # Run the DPR demo
    initial_image, dpr_image, magnified_image = process_image(data_folder, file_name, file_type, psf, options)

    elapsed_time = time.time() - start_time
    print(f"DPR processing completed in {elapsed_time:.2f} seconds.")

    if initial_image is not None:
        display_images(initial_image, magnified_image, dpr_image)


if __name__ == '__main__':
    main()
