import matplotlib.pyplot as plt
import numpy as np
from dpr_function import dpr_set_parameters, process_image


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
        "Enter the file name with type or press Enter to use the default value:",
        "test_image.tif"
    )
    file_name, file_type = file_name_with_type.rsplit('.', 1)

    # Ask user if they want to use default parameters
    use_default_params = get_user_input(
        "Do you want to use default parameters (psf=4, gain=2, background=10, temporal='mean')? (y/n) \n"
        "Press Enter to use the default value:",
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

    # Run the demo
    initial_image, dpr_image, magnified_image = process_image.process_image(data_folder, file_name, file_type, psf, options)

    if initial_image is not None:
        # Display the images
        display_images(initial_image, magnified_image, dpr_image)


if __name__ == '__main__':
    main()
