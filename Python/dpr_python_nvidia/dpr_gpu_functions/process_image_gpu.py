import os
from .dpr_stack_gpu import dpr_stack
import logging
import numpy as np
import tifffile as tiff
from PIL import Image


def process_image(data_folder, file_name, file_type, psf, options):
    """
    Process and enhance a stack of images using the DPR (Deconvolution and Pixel Restoration) algorithm.

    Parameters:
    - data_folder (str): Directory path where the input image files are located and where results will be saved.
    - file_name (str): Base name of the image file(s) to be processed (excluding extension).
    - file_type (str): File extension/type of the images to be processed (e.g., 'tif', 'jpg', 'png').
    - psf (float): Point Spread Function (PSF) value used for deconvolution in the DPR algorithm.
    - options (dict): Dictionary of options for the DPR algorithm. It must include keys such as 'gain', 'background', and 'temporal'.

    Returns:
    - None: The function performs in-place operations and saves results to disk.

    This function performs the following steps:
    1. Loads an image stack from the specified directory.
    2. Applies the DPR algorithm to enhance the images.
    3. Saves the resulting DPR-enhanced images to a designated output directory.
    """
    print(f"Starting DPR demo.")

    # Load the image stack to determine the number of frames
    try:
        image_stack = load_image_stack(data_folder, file_name, file_type)
        print(f"Loaded input image stack from \"{data_folder}/{file_name}.{file_type}\":"
              f" {image_stack.shape} - dimensions(height, width, frames)")
    except Exception as e:
        logging.error(f"Error loading images: {e}")
        return

    # Prepare the folder for saving DPR-enhanced images
    save_folder = os.path.join(data_folder, 'DPR_results')
    os.makedirs(save_folder, exist_ok=True)

    # Run the DPR algorithm
    try:
        dpr_image, magnified_image = dpr_stack(image_stack, psf, options)
    except Exception as e:
        logging.error(f"Error running DPR algorithm: {e}")
        return

    # Save the DPR-enhanced image
    try:
        save_image(dpr_image, save_folder, f'{file_name}_result', file_type)
        print(f"Results saved to disk: \"{save_folder}/{file_name}_result.{file_type}\"")
    except Exception as e:
        logging.error(f"Error saving results: {e}")

    return image_stack, dpr_image, magnified_image


def save_image(image, save_folder, file_name, file_type):
    """
    Save an image in the specified format.

    Parameters:
    - image: 2D or 3D numpy array of the image to save
    - save_folder: Folder where the image will be saved
    - file_name: Name of the file to save
    - file_type: Format of the file to save (e.g., 'tif', 'jpg', 'png')
    """
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    file_path = os.path.join(save_folder, f'{file_name}.{file_type}')

    if file_type.lower() == 'tif':
        tiff.imwrite(file_path, image)
    elif file_type.lower() in ['jpg', 'jpeg', 'png']:
        # Normalize and convert to uint8 for saving in formats like JPEG or PNG
        if image.dtype != np.uint8:
            image = normalize_and_convert(image)
        img = Image.fromarray(image)
        img.save(file_path)


def normalize_and_convert(image):
    """
    Normalize the image data to the range 0-255 and convert to uint8.

    Parameters:
    - image (numpy.ndarray): Image data to normalize and convert.

    Returns:
    - numpy.ndarray: Normalized and converted image data in uint8 format.
    """
    image_min = image.min()
    image_max = image.max()
    if image_max > image_min:
        image = (image - image_min) / (image_max - image_min) * 255
    return image.astype(np.uint8)


def load_image_stack(data_folder, file_name, file_type):
    """
    Load a stack of images from a file.

    Parameters:
    - data_folder: Directory containing the image files
    - file_name: Base name of the image file
    - file_type: Type of the image file (e.g., 'tif', 'jpg', 'png')

    Returns:
    - image_stack: Numpy array containing the image stack (height, width, frames)
    - num_frames: Number of frames in the image stack
    """
    file_path = os.path.join(data_folder, f'{file_name}.{file_type}')
    try:
        if file_type.lower() == 'tif':
            image_stack = tiff.imread(file_path)
            if image_stack.ndim == 3:  # If image stack has 3 dimensions (frames, height, width)
                return np.transpose(image_stack, (1, 2, 0))  # Change to (height, width, frames)
        else:
            # For jpg and png, use PIL to read the images
            img = Image.open(file_path)
            # img = img.convert('RGB')  # Ensure the image is in RGB format
            return np.array(img)  # Convert to numpy array
    except Exception as e:
        logging.error(f"Error loading image stack from {file_path}: {e}")
        raise
