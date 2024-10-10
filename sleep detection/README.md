# Heart Rate Data Processing and Sleep Detection

This repository contains R scripts for processing heart rate data, detecting sleep sessions, and generating visualizations.

## Directory Structure

- `main_script.R`: The main script to run the analysis.
- `R/`: Contains modular R scripts.
  - `data_loading.R`: Functions to load heart rate and sleep report data.
  - `sleep_detection.R`: Functions to detect sleep sessions.
  - `result_saving.R`: Functions to save processed data.
  - `plotting.R`: Functions to create and save plots.
- `data/`: Directory to place your heart rate data files.
- `reports/`: Directory to place your sleep report data files.
- `results/`: Directory where processed data and plots will be saved.

## Prerequisites

- R version >= 3.6.0
- R packages:
  - dplyr
  - purrr
  - susieR
  - Rfast
  - lubridate
  - ggplot2
  - patchwork
  - scales

Install the required packages using:

```R
install.packages(c("dplyr", "purrr", "susieR", "Rfast", "lubridate", "ggplot2", "patchwork", "scales"))
