package com.dpr.plugin;

import ij.IJ;
import ij.ImagePlus;
import ij.ImageStack;
import ij.gui.GenericDialog;
import ij.measure.Calibration;
import ij.plugin.PlugIn;
import ij.plugin.filter.Convolver;
import ij.plugin.filter.GaussianBlur;
import ij.process.FloatProcessor;
import ij.process.ImageProcessor;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

/**
 * Implements the DPR algorithm as an ImageJ plugin.
 */
public class DPR_Plugin implements PlugIn {

    /** Simple POJO for DPR parameters. */
    private static class DprOptions {
        final double psf;        // PSF FWHM
        final double gain;       // displacement gain
        final int background;    // radius for local minimum filter
        final String temporal;   // none | mean | var
        DprOptions(double psf, double gain, int background, String temporal) {
            this.psf = psf;
            this.gain = gain;
            this.background = background;
            this.temporal = temporal;
        }
    }

    // Dialog-captured fields
    private static double psf;
    private static double gain;
    private static int background;
    private static String temporal;

    @Override
    public void run(String arg) {
        ImagePlus imp = IJ.getImage();
        if (imp == null) {
            IJ.noImage();
            return;
        }

        if (!showDialog()) {
            return; // user cancelled
        }
        DprOptions options = new DprOptions(psf, gain, background, temporal);

        IJ.showStatus("Running DPR Plugin...");
        long t0 = System.currentTimeMillis();

        ImagePlus[] results = dprStack(imp, options);

        long t1 = System.currentTimeMillis();
        IJ.showStatus("DPR processing finished in " + (t1 - t0) + " ms.");

        if (results != null) {
            if (results[0] != null) results[0].show();   // DPR final
            if (results[1] != null) results[1].show();   // magnified raw final
        }
    }

    /**
     * Parameter dialog.
     */
    private boolean showDialog() {
        GenericDialog gd = new GenericDialog("DPR Parameters");
        gd.addNumericField("PSF FWHM (pixels):", 4, 2);
        gd.addNumericField("Gain:", 2, 2, 5, "(typically 1 or 2)");
        gd.addNumericField("Background Radius (pixels):", 10, 0);
        String[] temporalOptions = {"none", "mean", "var"};
        gd.addChoice("Temporal Processing:", temporalOptions, "mean");

        gd.showDialog();
        if (gd.wasCanceled()) return false;

        psf = gd.getNextNumber();
        gain = gd.getNextNumber();
        background = (int) gd.getNextNumber();
        temporal = gd.getNextChoice();
        return true;
    }

    /**
     * Process an entire stack and return {DPR_result, magnified_raw}.
     */
    private ImagePlus[] dprStack(ImagePlus imp, DprOptions options) {
        final int nSlices = imp.getStackSize();
        final ImageStack inputStack = imp.getStack();

        // --- Compute output calibration (preserved for all results) ---
        final Calibration originalCal = imp.getCalibration();
        final Calibration newCal = originalCal.copy();
        // Ensure unit is preserved; if missing/invalid, default to microns
        String unit = originalCal.getUnit();
        if (unit == null || unit.isEmpty() || unit.equalsIgnoreCase("pixel") || unit.equalsIgnoreCase("pixels")) {
            unit = "µm"; // ImageJ-friendly; shows as microns in UI
        }
        newCal.setUnit(unit);

        // Convert PSF FWHM to 1/e radius and compute magnification (≈ 5 px per PSF 1/e)
        final double psf_1e = options.psf / 1.6651;
        final double magnification = (psf_1e > 0) ? (5.0 / psf_1e) : 1.0; // guard div-by-zero

        // Pixel size shrinks by the magnification
        if (magnification > 0) {
            newCal.pixelWidth  = originalCal.pixelWidth  / magnification;
            newCal.pixelHeight = originalCal.pixelHeight / magnification;
            // Units, z-spacing, frame interval, origins are preserved via copy()
        }

        // --- Parallel per-slice DPR ---
        List<Future<ImageProcessor[]>> futures = new ArrayList<>();
        ExecutorService executor = Executors.newWorkStealingPool();

        for (int i = 1; i <= nSlices; i++) {
            final int sliceIndex = i;
            futures.add(executor.submit(() -> {
                IJ.showProgress(sliceIndex, nSlices);
                ImageProcessor ip = inputStack.getProcessor(sliceIndex).convertToFloat();
                return dprUpdateSingle(ip, options);
            }));
        }

        executor.shutdown();
        try {
            if (!executor.awaitTermination(1, TimeUnit.HOURS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            IJ.log("DPR processing interrupted.");
            Thread.currentThread().interrupt();
            return null;
        }

        // --- Collect results ---
        ImageStack dprResultStack = null;
        ImageStack magnifiedRawStack = null;

        try {
            for (Future<ImageProcessor[]> f : futures) {
                ImageProcessor[] pair = f.get(); // [I_DPR, raw_magnified]
                if (dprResultStack == null) {
                    dprResultStack = new ImageStack(pair[0].getWidth(), pair[0].getHeight());
                    magnifiedRawStack = new ImageStack(pair[1].getWidth(), pair[1].getHeight());
                }
                dprResultStack.addSlice(pair[0]);
                magnifiedRawStack.addSlice(pair[1]);
            }
        } catch (InterruptedException ie) {
            Thread.currentThread().interrupt();
            IJ.handleException(ie);
            return null;
        } catch (ExecutionException ee) {
            IJ.handleException(ee);
            return null;
        }

        // --- Temporal combine DPR stack ---
        ImagePlus dprFinalImage;
        if (nSlices > 1 && options.temporal.equalsIgnoreCase("mean")) {
            ImageProcessor meanIp = calculateMean(dprResultStack);
            dprFinalImage = new ImagePlus(imp.getShortTitle() + "_DPR_Mean", meanIp);
            dprFinalImage.setCalibration(newCal); // attach calibration immediately
        } else if (nSlices > 1 && options.temporal.equalsIgnoreCase("var")) {
            ImageProcessor varIp = calculateVariance(dprResultStack);
            dprFinalImage = new ImagePlus(imp.getShortTitle() + "_DPR_Var", varIp);
            dprFinalImage.setCalibration(newCal);
        } else {
            dprFinalImage = new ImagePlus(imp.getShortTitle() + "_DPR_Stack", dprResultStack);
            dprFinalImage.setCalibration(newCal);
        }

        // --- Magnified raw (always mean) ---
        ImageProcessor magnifiedMean = calculateMean(magnifiedRawStack);
        ImagePlus magnifiedFinalImage = new ImagePlus(imp.getShortTitle() + "_Magnified_Mean", magnifiedMean);
        magnifiedFinalImage.setCalibration(newCal);

        return new ImagePlus[]{dprFinalImage, magnifiedFinalImage};
    }

    /**
     * Single-frame DPR core. Returns {I_DPR, I_magnified} as ImageProcessors.
     */
    private ImageProcessor[] dprUpdateSingle(ImageProcessor i_in, DprOptions options) {
        // --- Parameters ---
        final double psf_1e = options.psf / 1.6651;             // FWHM -> 1/e radius
        final int window_radius = options.background;            // local-min filter radius

        // --- Dimensions & target upscale ---
        final int initialWidth = i_in.getWidth();
        final int initialHeight = i_in.getHeight();
        final int newWidth = (int) Math.round(5 * initialWidth / psf_1e);
        final int newHeight = (int) Math.round(5 * initialHeight / psf_1e);
        final int PADDING = 10;

        // --- Background subtraction (global min) ---
        ImageProcessor single_frame_I_in = i_in.duplicate();
        float minVal = Float.MAX_VALUE;
        float[] inPix = (float[]) single_frame_I_in.convertToFloat().getPixels();
        for (float p : inPix) if (p < minVal) minVal = p;
        single_frame_I_in.add(-minVal);

        // --- Local-min filter and subtract ---
        ImageProcessor single_frame_I_in_localmin = localMinimumFilter(single_frame_I_in, window_radius);

        // --- Upscale with bicubic (spline-like) ---
        ImageProcessor single_frame_localmin_magnified = single_frame_I_in_localmin.duplicate();
        single_frame_localmin_magnified.setInterpolationMethod(ImageProcessor.BICUBIC);
        single_frame_localmin_magnified = single_frame_localmin_magnified.resize(newWidth, newHeight, true);

        ImageProcessor single_frame_I_magnified = single_frame_I_in.duplicate();
        single_frame_I_magnified.setInterpolationMethod(ImageProcessor.BICUBIC);
        single_frame_I_magnified = single_frame_I_magnified.resize(newWidth, newHeight, true);

        // --- Post-process & pad (clip negatives, zero-pad border) ---
        single_frame_localmin_magnified = postProcessAndPad(single_frame_localmin_magnified, PADDING);
        single_frame_I_magnified = postProcessAndPad(single_frame_I_magnified, PADDING);

        final int paddedWidth = single_frame_I_magnified.getWidth();
        final int paddedHeight = single_frame_I_magnified.getHeight();

        // --- Local normalization: divide by Gaussian blur ---
        ImageProcessor blurredIp = single_frame_localmin_magnified.duplicate();
        GaussianBlur gb = new GaussianBlur();
        gb.blurFloat((FloatProcessor) blurredIp, 10, 10, 0.01); // sigmaX=sigmaY=10

        ImageProcessor I_normalized = single_frame_localmin_magnified.duplicate();
        float[] normPix = (float[]) I_normalized.getPixels();
        float[] blurPix = (float[]) blurredIp.getPixels();
        for (int i = 0; i < normPix.length; i++) {
            normPix[i] = normPix[i] / (blurPix[i] + 1e-5f);
        }

        // --- Sobel gradients (note MATLAB conv kernel orientation comments) ---
        Convolver convolver = new Convolver();
        float[] sobelX_kernel = { -1f, 0f, 1f, -2f, 0f, 2f, -1f, 0f, 1f }; // used for gradient Y in MATLAB
        float[] sobelY_kernel = { -1f, -2f, -1f, 0f, 0f, 0f, 1f, 2f, 1f }; // used for gradient X in MATLAB

        ImageProcessor gradient_y = I_normalized.duplicate();
        convolver.convolve(gradient_y, sobelX_kernel, 3, 3);

        ImageProcessor gradient_x = I_normalized.duplicate();
        convolver.convolve(gradient_x, sobelY_kernel, 3, 3);

        // --- Normalize gradients by intensity ---
        float[] gradXPix = (float[]) gradient_x.getPixels();
        float[] gradYPix = (float[]) gradient_y.getPixels();
        for (int i = 0; i < normPix.length; i++) {
            gradXPix[i] /= (normPix[i] + 1e-5f);
            gradYPix[i] /= (normPix[i] + 1e-5f);
        }

        // --- Displacements ---
        final float gain_value = (float) (0.5 * options.gain + 1.0);
        ImageProcessor displacement_x = gradient_x; // reuse
        ImageProcessor displacement_y = gradient_y; // reuse
        displacement_x.multiply(gain_value);
        displacement_y.multiply(gain_value);

        limitAbsoluteValues(displacement_x, 10);
        limitAbsoluteValues(displacement_y, 10);

        // --- Resample / accumulate using bilinear weights and integer steps ---
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

                float w1 = (1 - dx_abs_frac) * (1 - dy_abs_frac);
                float w2 = (1 - dx_abs_frac) * dy_abs_frac;
                float w3 = dx_abs_frac * (1 - dy_abs_frac);
                float w4 = dx_abs_frac * dy_abs_frac;

                int c1x = (int) dx;
                int c1y = (int) dy;
                int c2x = (int) dx;
                int c2y = (int) dy + (int) Math.signum(dy);
                int c3x = (int) dx + (int) Math.signum(dx);
                int c3y = (int) dy;
                int c4x = (int) dx + (int) Math.signum(dx);
                int c4y = (int) dy + (int) Math.signum(dy);

                float v = magPixels[index];
                outPixels[(nx + c1x) * paddedWidth + (ny + c1y)] += w1 * v;
                outPixels[(nx + c2x) * paddedWidth + (ny + c2y)] += w2 * v;
                outPixels[(nx + c3x) * paddedWidth + (ny + c3y)] += w3 * v;
                outPixels[(nx + c4x) * paddedWidth + (ny + c4y)] += w4 * v;
            }
        }

        // --- Crop off padding ---
        single_frame_I_out.setRoi(PADDING, PADDING, newWidth, newHeight);
        single_frame_I_magnified.setRoi(PADDING, PADDING, newWidth, newHeight);

        return new ImageProcessor[]{ single_frame_I_out.crop(), single_frame_I_magnified.crop() };
    }

    // ===================== Helper functions =====================

    /** Local minimum filter; returns I(x,y) - localMin(x,y) within a square window. */
    private ImageProcessor localMinimumFilter(ImageProcessor ip, int radius) {
        int width = ip.getWidth();
        int height = ip.getHeight();
        FloatProcessor outIp = new FloatProcessor(width, height);
        float[] outPixels = (float[]) outIp.getPixels();

        for (int y = 0; y < height; y++) {
            int u_min = Math.max(0, y - radius);
            int u_max = Math.min(height - 1, y + radius);
            for (int x = 0; x < width; x++) {
                int v_min = Math.max(0, x - radius);
                int v_max = Math.min(width - 1, x + radius);
                float localMin = Float.MAX_VALUE;
                for (int u = u_min; u <= u_max; u++) {
                    for (int v = v_min; v <= v_max; v++) {
                        float val = ip.getPixelValue(v, u);
                        if (val < localMin) localMin = val;
                    }
                }
                outPixels[y * width + x] = ip.getPixelValue(x, y) - localMin;
            }
        }
        return outIp;
    }

    /** Clip negatives to 0 and zero-pad by {@code padding} on all sides. */
    private ImageProcessor postProcessAndPad(ImageProcessor ip, int padding) {
        float[] pixels = (float[]) ip.getPixels();
        for (int i = 0; i < pixels.length; i++) if (pixels[i] < 0) pixels[i] = 0;
        int newWidth = ip.getWidth() + 2 * padding;
        int newHeight = ip.getHeight() + 2 * padding;
        FloatProcessor padded = new FloatProcessor(newWidth, newHeight);
        padded.insert(ip, padding, padding);
        return padded;
    }

    /** Hard-limit absolute values in-place (|p|>limit -> 0). */
    private void limitAbsoluteValues(ImageProcessor ip, float limit) {
        float[] pixels = (float[]) ip.getPixels();
        for (int i = 0; i < pixels.length; i++) {
            if (Math.abs(pixels[i]) > limit) pixels[i] = 0;
        }
    }

    /** Mean projection of a stack. */
    private ImageProcessor calculateMean(ImageStack stack) {
        int width = stack.getWidth();
        int height = stack.getHeight();
        int n = stack.getSize();
        FloatProcessor meanIp = new FloatProcessor(width, height);
        float[] mean = (float[]) meanIp.getPixels();
        for (int i = 1; i <= n; i++) {
            float[] s = (float[]) stack.getProcessor(i).getPixels();
            for (int j = 0; j < mean.length; j++) mean[j] += s[j];
        }
        meanIp.multiply(1.0 / n);
        return meanIp;
    }

    /** Sample variance projection of a stack. */
    private ImageProcessor calculateVariance(ImageStack stack) {
        int width = stack.getWidth();
        int height = stack.getHeight();
        int n = stack.getSize();
        if (n <= 1) return stack.getProcessor(1);
        FloatProcessor meanIp = (FloatProcessor) calculateMean(stack);
        float[] mean = (float[]) meanIp.getPixels();
        FloatProcessor varIp = new FloatProcessor(width, height);
        float[] var = (float[]) varIp.getPixels();
        for (int i = 1; i <= n; i++) {
            float[] s = (float[]) stack.getProcessor(i).getPixels();
            for (int j = 0; j < var.length; j++) {
                float d = s[j] - mean[j];
                var[j] += d * d;
            }
        }
        varIp.multiply(1.0 / (n - 1));
        return varIp;
    }
}
