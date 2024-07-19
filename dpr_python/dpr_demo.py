from dpr_function import dpr_set_parameters, process_image


def main():
    """
    Main function to execute the DPR (Deconvolution and Pixel Restoration) process.

    This script:
    1. Sets up the parameters and file paths for processing images.
    2. Configures the DPR algorithm parameters.
    3. Calls the `process_image` function to load, process, and save the enhanced images.
    """
    # Set the directory containing the images and image parameters
    data_folder = 'test_images'  # Directory where the input images are located and results will be saved
    file_name = 'test_image_jpg'     # Base name of the image file(s) (without extension)
    file_type = 'jpg'            # File type/extension of the image files (e.g., 'tif', 'jpg', 'png')

    # Set DPR parameters
    psf = 4  # Point Spread Function (PSF) value used for deconvolution in the DPR algorithm

    # Define DPR options in a dictionary format
    options = dpr_set_parameters.dpr_set_parameters(
        psf=psf,           # PSF value for deconvolution
        gain=2,            # Gain parameter for the DPR algorithm
        background=10,     # Background value for the DPR algorithm
        temporal='mean'   # Temporal processing option ('mean' or 'var')
    )

    # Run the DPR processing demo
    process_image.process_image(
        data_folder=data_folder,  # Directory containing the images
        file_name=file_name,      # Base name of the image file(s)
        file_type=file_type,      # File extension/type of the image files
        psf=psf,                  # PSF value for the DPR algorithm
        options=options           # Options dictionary for DPR processing
    )


if __name__ == '__main__':
    main()
