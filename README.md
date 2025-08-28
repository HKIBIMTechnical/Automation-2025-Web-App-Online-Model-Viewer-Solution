# Web-App-Online-Model-Viewer-Solution
![image](https://github.com/HKIBIMTechnical/Automation-2025-Web-App-Online-Model-Viewer-Solution/blob/main/image.png)
This is a Streamlit-based web application for online model viewing and analysis, integrating with Speckle for BIM/CAD data visualization and parameter exploration. It provides interactive charts and data export features for selected model parameters.

## Disclaimer

**This program is for learning and reference purposes only.**

Some sensitive words or information have been removed from the code, which may cause errors or incomplete functionality. Despite this, the project serves as a valuable learning example for integrating Streamlit with BIM/CAD data workflows and visualization.

## Main Features

- Connects to Speckle servers and streams
- Visualizes BIM/CAD model data interactively
- Allows parameter selection and data export
- Displays summary charts using Plotly

## How to Run

1. Install the main requirements:

   ```
   pip install streamlit specklepy pandas plotly
   ```

   (You may need to install additional dependencies based on your environment and usage.)
2. Run the app:

   ```
   streamlit run streamlit_app.py
   ```

## Notes

- You will need to provide your own `secrets.toml` or set the required Streamlit secrets for Speckle server access.
- Some features may not work as intended due to the removal of sensitive or proprietary code.
- For educational use only.
