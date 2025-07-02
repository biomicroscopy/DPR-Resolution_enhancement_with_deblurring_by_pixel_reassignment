package com.dpr.plugin;

import ij.IJ;
import ij.ImagePlus;
import ij.ImageStack;
import ij.gui.GenericDialog;
import ij.plugin.PlugIn;
import ij.plugin.filter.Convolver;
import ij.plugin.filter.GaussianBlur;
import ij.process.FloatProcessor;
import ij.process.ImageProcessor;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

/**
 * Implements the Displacement-Preserving Reconstruction (DPR) algorithm as an ImageJ plugin.
 *
 * <p>This plugin is a high-fidelity translation of the provided MATLAB DPR library.
 * It enhances image resolution by calculating pixel displacements based on local gradients
 * and remapping pixel intensities.
 *
 * <p><b>Primary Source (Source of Truth):</b> The core logic, function signatures, and
 * mathematical operations are derived from the provided MATLAB code.
 * <p><b>Secondary Source (Verification):</b> The Python code was used to cross-reference
 * and verify the understanding of the algorithm's behavior and data flow.
 *
 * @author Gemini AI (based on user-provided MATLAB/Python sources)
 * @version 1.0
 */
public class DPR_Plugin implements PlugIn {

    /**
     * A simple private static class (POJO) to hold DPR parameters, similar to a MATLAB struct.
     */
    private static class DprOptions {
        final double psf;
        final double gain;
        final int background; // Radius for local-minimum filter
        final String temporal;

        DprOptions(double psf, double gain, int background, String temporal) {
            this.psf = psf;
            this.gain = gain;
            this.background = background;
            this.temporal = temporal;
        }
    }

    @Override
    public void run(String arg) {
        ImagePlus imp = IJ.getImage();
        if (imp == null) {
            IJ.noImage();
            return;
        }

        // --- Create User Dialog (GenericDialog) ---
        if (!showDialog()) {
            return; // User cancelled the dialog
        }
        // These static fields are set by showDialog()
        DprOptions options = new DprOptions(psf, gain, background, temporal);

        IJ.showStatus("Running DPR Plugin...");
        long startTime = System.currentTimeMillis();

        // --- Run DPR algorithm ---
        // The results are returned as an array of ImagePlus objects
        ImagePlus[] results = dprStack(imp, options);

        long endTime = System.currentTimeMillis();
        IJ.showStatus("DPR processing finished in " + (endTime - startTime) + " ms.");

        // --- Display Results ---
        if (results != null) {
            if(results[0] != null) results[0].show();
            if(results[1] != null) results[1].show();
        }
    }

    private static double psf;
    private static double gain;
    private static int background;
    private static String temporal;

    /**
     * Creates and shows a GenericDialog to get parameters from the user.
     * Maps to the main script's parameter setting section.
     *
     * @return false if the user cancels the dialog, true otherwise.
     */
    private boolean showDialog() {
        GenericDialog gd = new GenericDialog("DPR Parameters");
        gd.addNumericField("PSF FWHM (pixels):", 4, 2);
        gd.addNumericField("Gain:", 2, 2, 5, "(typically 1 or 2)");
        gd.addNumericField("Background Radius (pixels):", 10, 0);
        String[] temporalOptions = {"none", "mean", "var"};
        gd.addChoice("Temporal Processing:", temporalOptions, "mean");

        gd.showDialog();
        if (gd.wasCanceled()) {
            return false;
        }

        // Retrieve values from the dialog
        psf = gd.getNextNumber();
        gain = gd.getNextNumber();
        background = (int) gd.getNextNumber();
        temporal = gd.getNextChoice();
        
        return true;
    }


    /**
     * Processes an entire image stack, potentially in parallel.
     * Equivalent to MATLAB's `DPRStack.m`.
     *
     * @param imp     The input ImagePlus stack.
     * @param options The DPR parameters.
     * @return An array containing the DPR result ImagePlus and the magnified raw ImagePlus.
     */
    private ImagePlus[] dprStack(ImagePlus imp, DprOptions options) {
        int nSlices = imp.getStackSize();
        ImageStack inputStack = imp.getStack();

        // Prepare futures list to hold results from parallel processing
        List<Future<ImageProcessor[]>> futures = new ArrayList<>();
        // Equivalent to MATLAB's `parfor`
        ExecutorService executor = Executors.newWorkStealingPool();

        for (int i = 1; i <= nSlices; i++) {
            final int sliceIndex = i;
            Callable<ImageProcessor[]> task = () -> {
                IJ.showProgress(sliceIndex, nSlices);
                ImageProcessor ip = inputStack.getProcessor(sliceIndex).convertToFloat();
                return dprUpdateSingle(ip, options);
            };
            futures.add(executor.submit(task));
        }

        executor.shutdown();
        try {
            executor.awaitTermination(1, TimeUnit.HOURS);
        } catch (InterruptedException e) {
            IJ.log("DPR processing was interrupted.");
            Thread.currentThread().interrupt();
            return null;
        }

        // --- Collect results from all threads ---
        ImageStack dprResultStack = null;
        ImageStack magnifiedRawStack = null;

        try {
            for (Future<ImageProcessor[]> future : futures) {
                ImageProcessor[] resultPair = future.get(); // [I_DPR, raw_magnified]
                if (dprResultStack == null) {
                    dprResultStack = new ImageStack(resultPair[0].getWidth(), resultPair[0].getHeight());
                    magnifiedRawStack = new ImageStack(resultPair[1].getWidth(), resultPair[1].getHeight());
                }
                dprResultStack.addSlice(resultPair[0]);
                magnifiedRawStack.addSlice(resultPair[1]);
            }
        } catch (InterruptedException | ExecutionException e) {
            IJ.handleException(e);
            return null;
        }
        
        // --- Temporal Processing ---
        // Equivalent to MATLAB's `DPRStack` temporal logic
        ImagePlus dprFinalImage;
        if (nSlices > 1 && options.temporal.equalsIgnoreCase("mean")) {
            ImageProcessor meanIp = calculateMean(dprResultStack);
            dprFinalImage = new ImagePlus(imp.getShortTitle() + "_DPR_Mean", meanIp);
        } else if (nSlices > 1 && options.temporal.equalsIgnoreCase("var")) {
            ImageProcessor varIp = calculateVariance(dprResultStack);
            dprFinalImage = new ImagePlus(imp.getShortTitle() + "_DPR_Var", varIp);
        } else {
            dprFinalImage = new ImagePlus(imp.getShortTitle() + "_DPR_Stack", dprResultStack);
        }
        
        // --- Create magnified raw result for comparison (always mean) ---
        ImageProcessor magnifiedMean = calculateMean(magnifiedRawStack);
        ImagePlus magnifiedFinalImage = new ImagePlus(imp.getShortTitle() + "_Magnified_Mean", magnifiedMean);

        return new ImagePlus[]{dprFinalImage, magnifiedFinalImage};
    }

    /**
     * The core DPR algorithm for a single image frame.
     * Equivalent to MATLAB's `DPR_UpdateSingle.m`.
     *
     * @param i_in    The input FloatProcessor for a single slice.
     * @param options The DPR parameters.
     * @return An array of two ImageProcessors: {I_out, I_magnified}.
     */
    private ImageProcessor[] dprUpdateSingle(ImageProcessor i_in, DprOptions options) {
        
        // --- Parameter Setup ---
        // Equivalent to MATLAB's: PSF = PSF/1.6651;
        final double psf_1e = options.psf / 1.6651; // Convert FWHM to 1/e radius
        final int window_radius = options.background;

        // --- Image Upscaling Setup ---
        // Equivalent to MATLAB's: linspace and meshgrid to define new dimensions
        final int initialWidth = i_in.getWidth();
        final int initialHeight = i_in.getHeight();
        
        // upscaled image has ~5 pixels per PSF (1/e radius)
        final int newWidth = (int) Math.round(5 * initialWidth / psf_1e);
        final int newHeight = (int) Math.round(5 * initialHeight / psf_1e);
        final int PADDING = 10;

        // --- Background Subtraction (Local Minimum Filter) ---
        // Equivalent to MATLAB's: single_frame_I_in = I_in - min(I_in(:));
        ImageProcessor single_frame_I_in = i_in.duplicate();
        float minVal = Float.MAX_VALUE;
        float[] pixels = (float[]) single_frame_I_in.getPixels();
        for (float p : pixels) {
            if (p < minVal) minVal = p;
        }
        single_frame_I_in.add(-minVal);
        
        // Equivalent to MATLAB's: I - local_min(I) loop
        ImageProcessor single_frame_I_in_localmin = localMinimumFilter(single_frame_I_in, window_radius);

        // --- Upscale Images ---
        // Equivalent to MATLAB's: interp2(..., 'spline', 0)
        // We use ImageJ's BICUBIC as a high-quality approximation for spline interpolation.
        ImageProcessor single_frame_localmin_magnified = single_frame_I_in_localmin.duplicate();
        single_frame_localmin_magnified.setInterpolationMethod(ImageProcessor.BICUBIC);
        single_frame_localmin_magnified = single_frame_localmin_magnified.resize(newWidth, newHeight, true);

        ImageProcessor single_frame_I_magnified = single_frame_I_in.duplicate();
        single_frame_I_magnified.setInterpolationMethod(ImageProcessor.BICUBIC);
        single_frame_I_magnified = single_frame_I_magnified.resize(newWidth, newHeight, true);

        // --- Post-interpolation processing and Padding ---
        // Equivalent to MATLAB's: img(img < 0) = 0; img = padarray(img, [10 10], 0, 'both');
        single_frame_localmin_magnified = postProcessAndPad(single_frame_localmin_magnified, PADDING);
        single_frame_I_magnified = postProcessAndPad(single_frame_I_magnified, PADDING);
        
        final int paddedWidth = single_frame_I_magnified.getWidth();
        final int paddedHeight = single_frame_I_magnified.getHeight();
        
        // --- Local Normalization ---
        // Equivalent to MATLAB's: I_normalized = single_frame_localmin_magnified./(imgaussfilt(...) + 0.00001);
        ImageProcessor blurredIp = single_frame_localmin_magnified.duplicate();
        GaussianBlur gb = new GaussianBlur();
        gb.blurFloat((FloatProcessor)blurredIp, 10, 10, 0.01); // Sigma = 10
        
        ImageProcessor I_normalized = single_frame_localmin_magnified.duplicate();
        float[] normPix = (float[]) I_normalized.getPixels();
        float[] blurPix = (float[]) blurredIp.getPixels();
        for(int i = 0; i < normPix.length; i++) {
            normPix[i] = normPix[i] / (blurPix[i] + 1e-5f);
        }
        
        // --- Calculate Normalized Gradients ---
        // Equivalent to MATLAB's: imfilter(I_normalized, sobel, 'conv', 'replicate');
        Convolver convolver = new Convolver();
        // NOTE: MATLAB's 'conv' flips the kernel, so we use the standard kernels directly.
        // The assignment of X and Y gradients is intentionally swapped to match the MATLAB source exactly.
        float[] sobelX_kernel = {
         	   -1f,  0f,  1f,
         	   -2f,  0f,  2f,
         	   -1f,  0f,  1f
         	};  // For gradient Y in MATLAB
        float[] sobelY_kernel = {
         	   -1f, -2f, -1f,
         	    0f,  0f,  0f,
         	    1f,  2f,  1f
         	};  // For gradient X in MATLAB
        
        ImageProcessor gradient_y = I_normalized.duplicate();
        convolver.convolve(gradient_y, sobelX_kernel, 3, 3);

        ImageProcessor gradient_x = I_normalized.duplicate();
        convolver.convolve(gradient_x, sobelY_kernel, 3, 3);
        
        // --- Normalize Gradients ---
        // Equivalent to MATLAB's: gradient_x = gradient_x./(I_normalized+0.00001);
        float[] gradXPix = (float[]) gradient_x.getPixels();
        float[] gradYPix = (float[]) gradient_y.getPixels();
        for(int i = 0; i < normPix.length; i++) {
            gradXPix[i] /= (normPix[i] + 1e-5f);
            gradYPix[i] /= (normPix[i] + 1e-5f);
        }
        
        // --- Calculate Pixel Displacements ---
        // Equivalent to MATLAB's: displacement_x = gain_value * gradient_x;
        final float gain_value = (float) (0.5 * options.gain + 1.0);
        ImageProcessor displacement_x = gradient_x; // Reuse processor
        ImageProcessor displacement_y = gradient_y; // Reuse processor
        displacement_x.multiply(gain_value);
        displacement_y.multiply(gain_value);

        // Limit displacements: displacement(abs(displacement)>10) = 0;
        limitAbsoluteValues(displacement_x, 10);
        limitAbsoluteValues(displacement_y, 10);
        
        // --- Calculate Final Image with Weighted Pixel Displacements ---
        // This is the direct translation of the most complex loop in DPR_UpdateSingle.m
        FloatProcessor single_frame_I_out = new FloatProcessor(paddedWidth, paddedHeight);
        float[] outPixels = (float[]) single_frame_I_out.getPixels();
        float[] magPixels = (float[]) single_frame_I_magnified.getPixels();
        float[] dxPixels = (float[]) displacement_x.getPixels();
        float[] dyPixels = (float[]) displacement_y.getPixels();

        for (int nx = PADDING; nx < paddedHeight - PADDING; nx++) {
            for (int ny = PADDING; ny < paddedWidth - PADDING; ny++) {
                int index = nx * paddedWidth + ny;
                float dx = dxPixels[index];
                float dy = dyPixels[index];

                float dx_abs_frac = Math.abs(dx - (int) dx);
                float dy_abs_frac = Math.abs(dy - (int) dy);
                
                // Calculate weights for the 4 neighboring pixels
                float w1 = (1 - dx_abs_frac) * (1 - dy_abs_frac);
                float w2 = (1 - dx_abs_frac) * dy_abs_frac;
                float w3 = dx_abs_frac * (1 - dy_abs_frac);
                float w4 = dx_abs_frac * dy_abs_frac;

                // Calculate integer coordinates for the 4 neighbors
                int c1x = (int) dx;
                int c1y = (int) dy;
                int c2x = (int) dx;
                int c2y = (int) dy + (int) Math.signum(dy);
                int c3x = (int) dx + (int) Math.signum(dx);
                int c3y = (int) dy;
                int c4x = (int) dx + (int) Math.signum(dx);
                int c4y = (int) dy + (int) Math.signum(dy);

                // Distribute the intensity of the current pixel to its new locations
                float currentPixelValue = magPixels[index];
                outPixels[(nx + c1x) * paddedWidth + (ny + c1y)] += w1 * currentPixelValue;
                outPixels[(nx + c2x) * paddedWidth + (ny + c2y)] += w2 * currentPixelValue;
                outPixels[(nx + c3x) * paddedWidth + (ny + c3y)] += w3 * currentPixelValue;
                outPixels[(nx + c4x) * paddedWidth + (ny + c4y)] += w4 * currentPixelValue;
            }
        }
        
        // --- Crop final images to remove padding ---
        // Equivalent to MATLAB's: single_frame_I_out(11:end-10,11:end-10)
        single_frame_I_out.setRoi(PADDING, PADDING, newWidth, newHeight);
        single_frame_I_magnified.setRoi(PADDING, PADDING, newWidth, newHeight);

        return new ImageProcessor[]{single_frame_I_out.crop(), single_frame_I_magnified.crop()};
    }

    // =====================================================================================
    // MANDATORY HELPER FUNCTIONS
    // These methods replicate MATLAB functionality not directly available in ImageJ.
    // =====================================================================================

    /**
     * Helper function to replicate MATLAB's local minimum filtering loop.
     * For each pixel, it finds the minimum value in a square window around it.
     *
     * @param ip The input processor.
     * @param radius The radius of the search window.
     * @return A new ImageProcessor containing the local minimum values.
     */
    private ImageProcessor localMinimumFilter(ImageProcessor ip, int radius) {
        int width = ip.getWidth();
        int height = ip.getHeight();
        FloatProcessor outIp = new FloatProcessor(width, height);
        float[] outPixels = (float[]) outIp.getPixels();
        
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int u_min = Math.max(0, y - radius);
                int u_max = Math.min(height - 1, y + radius);
                int v_min = Math.max(0, x - radius);
                int v_max = Math.min(width - 1, x + radius);
                
                float localMin = Float.MAX_VALUE;
                for (int u = u_min; u <= u_max; u++) {
                    for (int v = v_min; v <= v_max; v++) {
                        float val = ip.getPixelValue(v, u);
                        if (val < localMin) {
                            localMin = val;
                        }
                    }
                }
                outPixels[y * width + x] = ip.getPixelValue(x, y) - localMin;
            }
        }
        return outIp;
    }

    /**
     * Helper to set negative values to zero and pad the image.
     * Replicates `img(img<0)=0;` and `padarray(img, [pad,pad], 0, 'both');`
     * @param ip Input processor
     * @param padding Amount of padding on each side
     * @return A new, processed, and padded ImageProcessor
     */
    private ImageProcessor postProcessAndPad(ImageProcessor ip, int padding) {
        float[] pixels = (float[]) ip.getPixels();
        for (int i = 0; i < pixels.length; i++) {
            if (pixels[i] < 0) {
                pixels[i] = 0;
            }
        }

        int newWidth = ip.getWidth() + 2 * padding;
        int newHeight = ip.getHeight() + 2 * padding;
        FloatProcessor paddedIp = new FloatProcessor(newWidth, newHeight);
        paddedIp.insert(ip, padding, padding);
        return paddedIp;
    }

    /**
     * Helper to limit the absolute values in a processor.
     * Replicates `disp(abs(disp)>limit)=0;`
     * @param ip The processor to modify in-place.
     * @param limit The absolute value limit.
     */
    private void limitAbsoluteValues(ImageProcessor ip, float limit) {
        float[] pixels = (float[]) ip.getPixels();
        for (int i = 0; i < pixels.length; i++) {
            if (Math.abs(pixels[i]) > limit) {
                pixels[i] = 0;
            }
        }
    }

    /**
     * Helper to calculate the mean projection of a stack.
     * @param stack The stack to process.
     * @return A single ImageProcessor with the mean pixel values.
     */
    private ImageProcessor calculateMean(ImageStack stack) {
        int width = stack.getWidth();
        int height = stack.getHeight();
        int n = stack.getSize();
        FloatProcessor meanIp = new FloatProcessor(width, height);
        float[] meanPixels = (float[]) meanIp.getPixels();
        
        for (int i = 1; i <= n; i++) {
            float[] slicePixels = (float[]) stack.getProcessor(i).getPixels();
            for (int j = 0; j < meanPixels.length; j++) {
                meanPixels[j] += slicePixels[j];
            }
        }
        meanIp.multiply(1.0 / n);
        return meanIp;
    }

    /**
     * Helper to calculate the variance projection of a stack.
     * @param stack The stack to process.
     * @return A single ImageProcessor with the variance of pixel values.
     */
    private ImageProcessor calculateVariance(ImageStack stack) {
        int width = stack.getWidth();
        int height = stack.getHeight();
        int n = stack.getSize();
        if (n <= 1) return stack.getProcessor(1);

        FloatProcessor meanIp = (FloatProcessor) calculateMean(stack);
        float[] meanPixels = (float[]) meanIp.getPixels();
        
        FloatProcessor varIp = new FloatProcessor(width, height);
        float[] varPixels = (float[]) varIp.getPixels();

        for (int i = 1; i <= n; i++) {
            float[] slicePixels = (float[]) stack.getProcessor(i).getPixels();
            for (int j = 0; j < varPixels.length; j++) {
                float diff = slicePixels[j] - meanPixels[j];
                varPixels[j] += diff * diff;
            }
        }
        varIp.multiply(1.0 / (n - 1)); // Use sample variance
        return varIp;
    }
} 
