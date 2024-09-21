# VapeHR-Analysis
This project statistically analyzes heart rate data to identify patterns associated with nicotine vaping. It involves preprocessing, matrix profile computation, annotation vector generation, and regression analysis, aiming to reveal how vaping affects heart rate and contributes to understanding nicotine's cardiovascular impact.
## Project Description

The VapeHR-Analysis project involves several key steps:
1. **Data Preprocessing**: Loading and cleaning heart rate and vaping event data.
2. **Matrix Profile Computation**: Calculating the matrix profile of heart rate data to identify patterns.
3. **Annotation Vector Generation**: Marking time segments related to vaping events.
4. **Regression Analysis**: Performing statistical analysis to determine how vaping affects heart rate.

## Features

- **Data Loading and Preprocessing**
- **Matrix Profile Computation**
- **Annotation Vector Creation**
- **Regression and Statistical Analysis**
- **Visualizations of Heart Rate Patterns**

# SleepAnalysis

## Overview

This project processes heart rate data for multiple participants, applies trend filtering to identify sleep periods, and saves the results for further analysis.

## Project Structure

- `scripts/`: Contains all R scripts organized by functionality.
- `data/`: Directory to store input data files.
- `results/csv/`: Directory where the processed CSV files will be saved.

## Setup

1. Clone the repository.
2. Place your data files in the `data/` directory.
3. Open and run the scripts in the `scripts/` folder in the specified order.

## Scripts

1. `00_load_libraries.R`: Loads all necessary R libraries.
2. `01_define_parameters.R`: Defines parameters and constants used across scripts.
3. `02_load_data.R`: Loads the data into R.
4. `03_process_data.R`: Processes the data, applies trend filtering, and identifies sleep periods.
5. `04_save_results.R`: Saves the processed data to CSV files.
