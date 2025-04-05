# dpr_stack.py

import cupy as cp
import numpy as np
from .update_single_gpu import update_single


def dpr_stack(input_stack, psf, options):
    """
    Perform DPR on a stack of images using GPU acceleration.

    Parameters:
        input_stack (numpy.ndarray): Input image stack with shape (height, width, frames).
        psf (float): PSF FWHM.
        options (dict): Dictionary with DPR parameters.

    Returns:
        tuple: (dpr_image, magnified_image) as numpy arrays.
    """
    num_frames = input_stack.shape[2]
    dpr_frames = []
    magnified_frames = []
    # Process each frame
    for i in range(num_frames):
        print(f"Processing frame {i + 1}/{num_frames}...")
        # Call the GPU-accelerated update; it returns NumPy arrays
        dpr_frame, magnified_frame, _, _ = update_single(input_stack[:, :, i], psf, options)
        dpr_frames.append(dpr_frame)
        magnified_frames.append(magnified_frame)

    # Stack frames along the third axis
    dpr_stack_arr = np.stack(dpr_frames, axis=2)
    magnified_stack_arr = np.stack(magnified_frames, axis=2)

    # Temporal processing (on GPU for speed)
    temporal = options.get('temporal', '')
    if temporal == 'mean':
        # Convert to CuPy, compute mean along frames, then back to NumPy
        dpr_image = cp.asnumpy(cp.mean(cp.asarray(dpr_stack_arr), axis=2))
    elif temporal == 'var':
        dpr_image = cp.asnumpy(cp.var(cp.asarray(dpr_stack_arr), axis=2))
    else:
        # No temporal reduction; return the full stack
        dpr_image = dpr_stack_arr

    return dpr_image, magnified_stack_arr