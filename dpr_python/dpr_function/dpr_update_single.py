import numpy as np
import scipy.ndimage as ndimage
from scipy.interpolate import RectBivariateSpline


def dpr_update_single(i_in, psf, options):
    # Read options
    gain = options['gain']
    window_radius = int(np.ceil(options['background']))

    # Set parameter for image upscaling
    psf = psf / 1.6651  # Convert PSF to 1/e radius

    # Upscale input image
    number_row_initial, number_column_initial = i_in.shape
    x0 = np.linspace(-0.5, 0.5, number_column_initial)
    y0 = np.linspace(-0.5, 0.5, number_row_initial)

    x = np.linspace(-0.5, 0.5, round(5 * number_column_initial / psf))
    y = np.linspace(-0.5, 0.5, round(5 * number_row_initial / psf))

    # Sobel kernel
    sobel_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    # DPR on single frames
    single_frame_i_in = i_in - np.min(i_in)
    local_minimum = np.zeros((number_row_initial, number_column_initial))
    single_frame_i_in_localmin = np.zeros((number_row_initial, number_column_initial))

    for u in range(number_row_initial):
        for v in range(number_column_initial):
            sub_window = single_frame_i_in[max(0, u - window_radius):min(number_row_initial, u + window_radius + 1),
                         max(0, v - window_radius):min(number_column_initial, v + window_radius + 1)]
            local_minimum[u, v] = np.min(sub_window)
            single_frame_i_in_localmin[u, v] = single_frame_i_in[u, v] - local_minimum[u, v]

    # Upscale
    interp_localmin = RectBivariateSpline(y0, x0, single_frame_i_in_localmin)
    single_frame_localmin_magnified = interp_localmin(y, x)
    single_frame_localmin_magnified[single_frame_localmin_magnified < 0] = 0
    single_frame_localmin_magnified = np.pad(single_frame_localmin_magnified, 10, mode='constant')

    interp_i = RectBivariateSpline(y0, x0, single_frame_i_in)
    single_frame_i_magnified = interp_i(y, x)
    single_frame_i_magnified[single_frame_i_magnified < 0] = 0
    single_frame_i_magnified = np.pad(single_frame_i_magnified, 10, mode='constant')

    number_row, number_column = single_frame_i_magnified.shape

    # Locally normalized version of Im
    i_normalized = single_frame_localmin_magnified / (
            ndimage.gaussian_filter(single_frame_localmin_magnified, 10) + 1e-5)

    # Calculate normalized gradients
    gradient_y = ndimage.convolve(i_normalized, sobel_x, mode='reflect')
    gradient_x = ndimage.convolve(i_normalized, sobel_y, mode='reflect')

    gradient_x = gradient_x / (i_normalized + 1e-5)
    gradient_y = gradient_y / (i_normalized + 1e-5)

    # Calculate pixel displacements
    gain_value = 0.5 * gain + 1
    displacement_x = gain_value * gradient_x
    displacement_y = gain_value * gradient_y
    displacement_x[np.abs(displacement_x) > 10] = 0
    displacement_y[np.abs(displacement_y) > 10] = 0

    # Calculate I_out with weighted pixel displacements
    single_frame_i_out = np.zeros((number_row, number_column))
    for nx in range(10, number_row - 10):
        for ny in range(10, number_column - 10):
            weighted1 = (1 - abs(displacement_x[nx, ny] - int(displacement_x[nx, ny]))) * (
                    1 - abs(displacement_y[nx, ny] - int(displacement_y[nx, ny])))
            weighted2 = (1 - abs(displacement_x[nx, ny] - int(displacement_x[nx, ny]))) * abs(
                displacement_y[nx, ny] - int(displacement_y[nx, ny]))
            weighted3 = abs(displacement_x[nx, ny] - int(displacement_x[nx, ny])) * (
                    1 - abs(displacement_y[nx, ny] - int(displacement_y[nx, ny])))
            weighted4 = abs(displacement_x[nx, ny] - int(displacement_x[nx, ny])) * abs(
                displacement_y[nx, ny] - int(displacement_y[nx, ny]))

            coordinate1 = [int(displacement_x[nx, ny]), int(displacement_y[nx, ny])]
            coordinate2 = [int(displacement_x[nx, ny]),
                           int(displacement_y[nx, ny]) + int(np.sign(displacement_y[nx, ny]))]
            coordinate3 = [int(displacement_x[nx, ny]) + int(np.sign(displacement_x[nx, ny])),
                           int(displacement_y[nx, ny])]
            coordinate4 = [int(displacement_x[nx, ny]) + int(np.sign(displacement_x[nx, ny])),
                           int(displacement_y[nx, ny]) + int(np.sign(displacement_y[nx, ny]))]

            # Shift I-local_min, use 'single_frame_localmin_magnified',
            # shift raw image, use 'single_frame_I_magnified'
            single_frame_i_out[nx + coordinate1[0], ny + coordinate1[1]] += weighted1 * single_frame_i_magnified[nx, ny]
            single_frame_i_out[nx + coordinate2[0], ny + coordinate2[1]] += weighted2 * single_frame_i_magnified[nx, ny]
            single_frame_i_out[nx + coordinate3[0], ny + coordinate3[1]] += weighted3 * single_frame_i_magnified[nx, ny]
            single_frame_i_out[nx + coordinate4[0], ny + coordinate4[1]] += weighted4 * single_frame_i_magnified[nx, ny]

    single_frame_i_out = single_frame_i_out[10:-10, 10:-10]
    single_frame_i_magnified = single_frame_i_magnified[10:-10, 10:-10]

    return single_frame_i_out, single_frame_i_magnified, gain, window_radius
