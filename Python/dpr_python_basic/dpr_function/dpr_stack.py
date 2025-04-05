import numpy as np
import sys
from dpr_function import dpr_update_single


def dpr_stack(input_stack, psf, options):
    """
    Perform DPR on a stack of images.

    Args:
        input_stack
        psf (float): PSF value.
        options (dict): Options for DPR.

    Returns:
        None
    """
    # The image stack has 3 dimensions(height, width, frames)
    num_frames = input_stack.shape[2]

    # Initialize output stacks with the correct shape after magnification
    magnified_shape = dpr_update_single.dpr_update_single(input_stack[:, :, 0], psf, options)[1].shape
    dpr_stack_zeros = np.zeros((magnified_shape[0], magnified_shape[1], num_frames))
    magnified_stack = np.zeros((magnified_shape[0], magnified_shape[1], num_frames))

    print(f"Starting DPR stack processing for {num_frames} frames")

    for i in range(num_frames):
        sys.stdout.write(f"\rProcessing frame {i + 1}/{num_frames}")
        sys.stdout.flush()
        dpr_frame, magnified_frame, gain, window_radius = \
            dpr_update_single.dpr_update_single(input_stack[:, :, i], psf, options)
        dpr_stack_zeros[:, :, i] = dpr_frame
        magnified_stack[:, :, i] = magnified_frame

    # Temporal processing
    temporal = options.get('temporal', '')
    if temporal == 'mean':
        dpr_stack_zeros = np.mean(dpr_stack_zeros, axis=2)
    elif temporal == 'var':
        dpr_stack_zeros = np.var(dpr_stack_zeros, axis=2)

    print(f"\nCompleted DPR stack processing")
    return dpr_stack_zeros, magnified_stack
