# DPR ImageJ Plugin

DPR plugin for [Fiji](https://fiji.sc/). This plugin enhances image resolution by calculating pixel displacements based on local gradients and remapping pixel intensities.


## Features
- High-fidelity translation of the DPR algorithm
- Supports image stacks and temporal processing (mean/variance projections)
- User-friendly parameter dialog
- Fast, parallelized processing

## Requirements
- Java 8 or higher
- Build Tool: [Maven](https://maven.apache.org/)
- ImageJ/Fiji: Version 1.54h or later

## Installation
1. **Clone the repo:**
   ```sh
   git clone https://github.com/biomicroscopy/DPR-Resolution_enhancement_with_deblurring_by_pixel_reassignment.git
   cd DPR-Resolution_enhancement_with_deblurring_by_pixel_reassignment/FIJI_ImageJ
   ```
1. **Build the plugin JAR:**
   ```sh
   mvn clean package
   ```
   The JAR will be created at `target/dpr-plugin-1.0.0.jar`.

1. **Install in ImageJ/Fiji:**
   - Copy the JAR file to the `plugins` directory of your ImageJ / Fiji installation (e.g., Fiji.app/plugins/).
   - Restart ImageJ/Fiji.

## Usage
- Open an image or stack in ImageJ/Fiji.
- Go to `Plugins > DPR > Run DPR`.
- Set the parameters in the dialog:
   | Parameter (Default)    | Description                                                                           |
   | ---------------------- | ------------------------------------------------------------------------------------- |
   | **PSF**                | Point Spread Function: defines blur radius. Lower values improve resolution.          |
   | **Gain**               | Controls intensity enhancement. Higher values amplify details but may increase noise. |
   | **Background**         | Level of background subtraction to improve contrast by removing local baseline.       |
   | **Temporal**           | Frame processing method: `mean` for averaging, `var` for variance-based enhancement.  |
- Click OK to run. Results will be displayed as new images.

## Project Structure
```
ImageJ/
├── pom.xml
├── README.md
├── src/
│   ├── main/
│   │   ├── java/com/dpr/plugin/DPR_Plugin.java
│   │   └── resources/plugins.config
│   └── test/java/com/dpr/plugin/DPR_PluginTest.java
└── target/
    └── dpr-plugin-1.0.0.jar
```

## Development
- Source code is in `src/main/java/com/dpr/plugin/DPR_Plugin.java`.
- Tests are in `src/test/java/com/dpr/plugin/`.
- Plugin registration is handled by `src/main/resources/plugins.config`.

## License
This project is provided under the MIT License.

## Contact
For questions or contributions, please create a GitHub issue or reach out to byzhao@bu.edu.
