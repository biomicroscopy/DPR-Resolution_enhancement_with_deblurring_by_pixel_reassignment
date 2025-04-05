# dpr_gpu_set_parameters.py

import numpy as np

def set_parameters(psf, **kwargs):
    """
    Set parameters for Displacement-Preserving Reconstruction (DPR).

    Parameters:
        psf (float): PSF full width at half maximum in pixels.
        kwargs: Additional parameters (gain, background, temporal).

    Returns:
        dict: Dictionary containing DPR parameters.
    """
    options = {
        'gain': 1,
        'background': int(np.ceil(17 * psf)),  # default background as 17*psf
        'temporal': None
    }

    for key, value in kwargs.items():
        if key in options:
            options[key] = value
        else:
            raise ValueError(f"Unknown parameter '{key}'")
    
    print(f"DPR parameters: {options}")
    return options