# main_script.R

source("R/data_loading.R")
source("R/sleep_detection.R")
source("R/result_saving.R")
source("R/plotting.R")

data_path <- "data/"
report_path <- "reports/"
output_path <- "results/"

library(dplyr)
library(purrr)
library(susieR)
library(Rfast)
library(lubridate)
library(ggplot2)
library(patchwork)
library(scales)

IDs <- paste0('ID', 1:10)

data_list <- load_hr_data(IDs, data_path)
sleep_sessions_list <- load_sleep_data(IDs, report_path)

for (id in IDs) {
  hr_data1 <- data_list[[id]]
  sleep_sessions_df <- sleep_sessions_list[[id]]
  hr_data1 <- process_hr_data(hr_data1)
  results <- detect_sleep(hr_data1)
  hr_data1 <- update_hr_data(hr_data1, results)
  hr_data1 <- update_sleep_report(hr_data1, sleep_sessions_df)
  save_hr_data(hr_data1, id, output_path)
  id_index <- match(id, IDs)
  create_and_save_plots(hr_data1, sleep_sessions_df, id, output_path, id_index)
}
