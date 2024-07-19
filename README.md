# Resolution enhancement with deblurring by pixel reassignment (DPR)
Deblurring by pixel reassignment (DPR) is to perform PSF sharpening similar to deconvolution but in a manner less prone to noise-induced artifacts and without the requirement of a full model for the PSF. The basic principle of DPR is to reassignment the intensity value of pixels post-image acquisition. The pixel reassignment step size is dependent on the local log-image gradient. DPR relies solely on pixel reassignment. As such, no negativities are possible in the final image reconstruction. Moreover, intensity levels are rigorously conserved, with no requirement for additional procedures to ensure local linearity. 
A detailed description of the method can be found in:

Zhao, B., and Mertz, J. Resolution enhancement with deblurring by pixel reassignment (DPR). [Pub link](https://www.spiedigitallibrary.org/journals/advanced-photonics/volume-5/issue-06/066004/Resolution-enhancement-with-deblurring-by-pixel-reassignment/10.1117/1.AP.5.6.066004.full?webSyncID=100c5e17-3e55-b558-b001-3d8b3bd4461b&sessionGUID=d75b2c3e-257a-52be-e460-867d9b436758#_=_)

DOI:10.1117/1.AP.5.6.066004

If you find this code useful to your research, please consider citing it.
  
## Contributing

We welcome contributions to the project! To ensure a smooth process, please follow these guidelines:

1. **Fork the Repository:**
   - Go to the [project repository](https://github.com/biomicroscopy/Resolution_Enhancement_With_Deblurring.git) and click the "Fork" button.

2. **Create a New Branch:**
   - Clone your forked repository to your local machine.
   - Create a new branch for your feature or bug fix:
     ```bash
     git checkout -b feature-branch-name
     ```

3. **Make Your Changes:**
   - Implement your feature or fix the bug.
   - Ensure your code follows the project's coding standards and passes all tests.

4. **Commit Your Changes:**
   - Write a clear and concise commit message:
     ```bash
     git commit -m "Description of your changes"
     ```

5. **Push to Your Branch:**
   - Push your changes to your forked repository:
     ```bash
     git push origin feature-branch-name
     ```

6. **Open a Pull Request:**
   - Go to the original project repository and open a pull request.
   - Provide a detailed description of your changes and the problem they solve.
   - Refer


## Usage
Please check the demo scripts to get started.

## Feedback
If you have any comments, suggestions, or questions, please do contact us at byzhao@bu.edu.
