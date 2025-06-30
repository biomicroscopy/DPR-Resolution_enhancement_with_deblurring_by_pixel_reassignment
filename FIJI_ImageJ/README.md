TODO: Optimize the README

# DPR ImageJ Plugin

DPR plugin for [Fiji](https://fiji.sc/). This plugin enhances image resolution by calculating pixel displacements based on local gradients and remapping pixel intensities.

## Features
- High-fidelity translation of the DPR algorithm
- Supports image stacks and temporal processing (mean/variance projections)
- User-friendly parameter dialog
- Fast, parallelized processing

## Requirements
- Java 8 or higher
- [Maven](https://maven.apache.org/) (for building)
- ImageJ 1.54h or later (or Fiji)

## Installation
1. **Build the plugin JAR:**
   ```sh
   mvn clean package
   ```
   The JAR will be created at `target/dpr-plugin-1.0.0.jar`.

2. **Install in ImageJ/Fiji:**
   - Copy the JAR file to the `plugins` directory of your ImageJ or Fiji installation.
   - Restart ImageJ/Fiji.

## Usage
- Open an image or stack in ImageJ/Fiji.
- Go to `Plugins > DPR > Run DPR`.
- Set the parameters in the dialog:
  - **PSF FWHM (pixels):** Point spread function width
  - **Gain:** Typically 1 or 2
  - **Background Radius (pixels):** For local minimum filter
  - **Temporal Processing:** Choose `none`, `mean`, or `var`
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
└── dpr-plugin-1.0.0.jar
```

## Development
- Source code is in `src/main/java/com/dpr/plugin/`.
- Tests are in `src/test/java/com/dpr/plugin/`.
- Plugin registration is handled by `src/main/resources/plugins.config`.

## License
This project is provided under the MIT License.

## Contact
For questions or contributions, please contact byzhao@bu.edu.
