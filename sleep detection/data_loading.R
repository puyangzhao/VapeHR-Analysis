# data_loading.R

library(dplyr)
library(purrr)

load_hr_data <- function(ids, data_path) {
  data_list <- list()
  for (id in ids) {
    hr_filename <- paste0(data_path, id, "_imputed_hr.csv")
    data_list[[id]] <- read.csv(hr_filename)
  }
  return(data_list)
}

load_sleep_data <- function(ids, report_path) {
  sleep_sessions_list <- list()
  for (id in ids) {
    filename <- paste0(report_path, id, "_sleepreport.csv")
    sleep_data <- read.csv(filename)
    sleep_data$isoDate <- as.POSIXct(sleep_data$isoDate, format = "%Y-%m-%dT%H:%M:%OS", tz = "UTC")
    sleep_sessions <- extract_sleep_sessions(sleep_data)
    sleep_sessions_list[[id]] <- sleep_sessions
  }
  return(sleep_sessions_list)
}
