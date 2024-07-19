import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def dpr_set_parameters(psf, **kwargs):
    """
    Set parameters for Displacement-Preserving Reconstruction (DPR).

    Parameters:
    - psf: Point Spread Function (PSF) full width at half maximum (FWHM) in pixels
    - kwargs: Dictionary of additional parameters (gain, background, temporal)

    Returns:
    - options: Dictionary containing DPR parameters
    """
    options = {
        'gain': 1,
        'background': int(np.ceil(17 * psf)),
        'temporal': None
    }

    for key, value in kwargs.items():
        if key in options:
            options[key] = value
        else:
            raise ValueError(f"Unknown parameter '{key}'")

    logging.info(f"DPR parameters: {options}")

    return options
