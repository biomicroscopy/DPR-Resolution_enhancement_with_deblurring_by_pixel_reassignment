import cupy as cp
import cupyx.scipy.ndimage as ndi


def scatter_add(out, x, y, vals):
    cp.add.at(out, (y, x), vals)


def update_single(i_in, psf, options):
    I_in = cp.asarray(i_in, dtype=cp.float32)

    gain = options['gain']
    window_radius = int(cp.ceil(options['background']))

    psf = psf / 1.6651

    # Local minimum subtraction
    I_in -= cp.min(I_in)
    local_min = ndi.minimum_filter(I_in, size=2 * window_radius + 1)
    I_local = I_in - local_min

    # Image upscaling
    upscale_factor = 5 / psf
    I_local_up = ndi.zoom(I_local, zoom=upscale_factor, order=3)
    I_in_up = ndi.zoom(I_in, zoom=upscale_factor, order=1)

    # Padding
    pad = 10
    I_local_up = cp.pad(I_local_up, pad, mode='constant')
    I_in_up = cp.pad(I_in_up, pad, mode='constant')

    # Normalization and Gaussian smoothing
    smoothed = ndi.gaussian_filter(I_local_up, sigma=10)
    I_norm = I_local_up / (smoothed + 1e-5)

    # Gradient computation
    grad_x = ndi.sobel(I_norm, axis=1) / (I_norm + 1e-5)
    grad_y = ndi.sobel(I_norm, axis=0) / (I_norm + 1e-5)

    # Pixel displacement computation
    gain_value = 0.5 * gain + 1
    disp_x = cp.clip(gain_value * grad_x, -10, 10)
    disp_y = cp.clip(gain_value * grad_y, -10, 10)

    # Weighted pixel reassignment
    nr, nc = I_in_up.shape
    grid_y, grid_x = cp.mgrid[0:nr, 0:nc]

    new_y = grid_y + disp_y
    new_x = grid_x + disp_x

    floor_x = cp.floor(new_x).astype(cp.int32)
    floor_y = cp.floor(new_y).astype(cp.int32)

    wx = new_x - floor_x
    wy = new_y - floor_y

    I_out = cp.zeros_like(I_in_up)

    scatter_add(I_out, floor_x, floor_y, (1 - wx) * (1 - wy) * I_in_up)
    scatter_add(I_out, floor_x, floor_y + 1, (1 - wx) * wy * I_in_up)
    scatter_add(I_out, floor_x + 1, floor_y, wx * (1 - wy) * I_in_up)
    scatter_add(I_out, floor_x + 1, floor_y + 1, wx * wy * I_in_up)

    # Crop padding
    I_out = I_out[pad:-pad, pad:-pad]
    I_magnified = I_in_up[pad:-pad, pad:-pad]

    return cp.asnumpy(I_out), cp.asnumpy(I_magnified), gain, window_radius
