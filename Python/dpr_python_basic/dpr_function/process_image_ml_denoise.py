import os
import logging
import numpy as np
import tifffile as tiff
import bm3d
from PIL import Image
from dpr_function import dpr_stack

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def process_image_ml_denoise(data_folder, file_name, file_type, psf, options):
    """
    Process image using deep-learning-based denoising before DPR.

    Returns:
    - initial_image: Original loaded image stack.
    - dpr_image: DPR-processed image.
    - magnified_image: Magnified output from DPR.
    """
    logging.info("Starting DPR with deep-learning-based denoising.")

    # Load image stack
    try:
        initial_image = load_image_stack(data_folder, file_name, file_type)
        logging.info(f"Loaded image stack: {initial_image.shape} (height, width, frames)")
    except Exception as e:
        logging.error(f"Error loading images: {e}")
        return None  # Return None on error

    # Apply deep-learning-based denoising
    try:
        denoised_stack = denoise_images(initial_image)
        logging.info("Denoising completed.")
    except Exception as e:
        logging.error(f"Error during denoising: {e}")
        return None  # Return None on error

    # Process with DPR
    try:
        dpr_image, magnified_image = dpr_stack.dpr_stack(denoised_stack, psf, options)
    except Exception as e:
        logging.error(f"Error running DPR algorithm: {e}")
        return None  # Return None on error

    # Save output
    save_folder = os.path.join(data_folder, "DPR_results")
    os.makedirs(save_folder, exist_ok=True)

    try:
        save_image(dpr_image, save_folder, f"{file_name}_result", file_type)
        logging.info(f"Results saved: \"{save_folder}/{file_name}_result.{file_type}\"")
    except Exception as e:
        logging.error(f"Error saving results: {e}")

    # Ensure the function returns all expected values
    return initial_image, dpr_image, magnified_image


def denoise_images(image_stack):
    """
    Apply deep-learning-based denoising using BM3D.

    Parameters:
    - image_stack (numpy.ndarray): Image stack (height, width, frames).

    Returns:
    - denoised_stack (numpy.ndarray): Denoised image stack.
    """
    denoised_stack = np.zeros_like(image_stack)

    for i in range(image_stack.shape[2]):  # Process frame-by-frame
        denoised_stack[:, :, i] = bm3d.bm3d(image_stack[:, :, i], sigma_psd=15,
                                            stage_arg=bm3d.BM3DStages.HARD_THRESHOLDING)

    return denoised_stack


def save_image(image, save_folder, file_name, file_type):
    """
    Save an image to disk.

    Parameters:
    - image: 2D numpy array.
    - save_folder: Directory path.
    - file_name: Output file name.
    - file_type: Image format.
    """
    os.makedirs(save_folder, exist_ok=True)
    file_path = os.path.join(save_folder, f"{file_name}.{file_type}")

    if file_type.lower() == "tif":
        tiff.imwrite(file_path, image)
    elif file_type.lower() in ["jpg", "jpeg", "png"]:
        if image.dtype != np.uint8:
            image = normalize_and_convert(image)
        img = Image.fromarray(image)
        img.save(file_path)


def normalize_and_convert(image):
    """
    Normalize image data to range 0-255 and convert to uint8.

    Parameters:
    - image (numpy.ndarray): Input image.

    Returns:
    - numpy.ndarray: Normalized uint8 image.
    """
    image_min = image.min()
    image_max = image.max()
    if image_max > image_min:
        image = (image - image_min) / (image_max - image_min) * 255
    return image.astype(np.uint8)


def load_image_stack(data_folder, file_name, file_type):
    """
    Load an image stack from disk.

    Parameters:
    - data_folder: Directory containing images.
    - file_name: Base file name.
    - file_type: Image format.

    Returns:
    - image_stack (numpy.ndarray): Image stack (height, width, frames).
    """
    file_path = os.path.join(data_folder, f"{file_name}.{file_type}")
    try:
        if file_type.lower() == "tif":
            image_stack = tiff.imread(file_path)
            if image_stack.ndim == 3:
                return np.transpose(image_stack, (1, 2, 0))  # Convert to (H, W, frames)
        else:
            img = Image.open(file_path)
            return np.array(img)
    except Exception as e:
        logging.error(f"Error loading image stack: {e}")
        return None
