# UNIS_AGF211_SurfaceRadiationAndAlbedo
Data and Code for UNIS AGF-211 surface radiation project

## Authors:
- Hayden Mann (hay.mann@icloud.com)
- Nikola Reissner (nikola.reissner@gmx.de)
- *If anything appears to be not working or missing: Contact Hayden and Niki.

### Code Author Directory:
- I: Hayden Mann: hmann@bowdoin.edu (until Summer 2027), hay.mann@icloud.com

# Scripts
- *data_analyis.py<sup> I</sup>*: This program acts as a supporter to rad_plots_adjustedSW.py. It is not
run on its own. Its purpose is to help with data infrastructure.
- *rad_plots_adjustedSW.py<sup> I</sup>*: Plots shortwave radiation balance, longwave radiation balance,
net radiation balance, and albedo. Applies adjustment to incoming SW sensors who were showing large deviations in data collected, despite being adjacent to each other and thus experiencing the same conditions.
- *tiny_tags.py<sup> I</sup>*: Plots temperature time series for all four Tinytag probes, and
can also compute basic statistics (mean/min/max)

# Data (DataDataData)

- *MaggieMay*: 1-min resolution .dat files containing timestamped **radiation** data from the control station (Maggie May). Opened and read in *data_analysis.py*.
- *Dataframes*: The latest .csv files for the control (Maggie May) and experimental (Layla) stations. Both include necessary **radiative** data. Handled in *data_analysis.py*.
- *albedo_radiation*: Contains corresponding .txt, .csv, and .ttd files for the experimental (Layla) station Tinytag **temperature** data. Also includes **radiative** data for the experimental section. Opening and processing is handled in *data_analysis.py*.
- *calibration_coefficients*: Provided from Dr. Lukas Frank. Includes calibration coefficients for Tinytag data.

# How to Run:
- Run *rad_plots_adjustedSW.py* for plots of radiation. Can toggle data statistics on and off, as well as for each specific plot you want to run.
- Run *tiny_tags.py* for a plot of temperature. Can toggle data statistics on and off.
- Nothing will happen if you run *data_analysis.py*.

# Example Plots:



