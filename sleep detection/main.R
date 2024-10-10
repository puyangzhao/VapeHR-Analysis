# main.R

source("R/data_loading.R")
source("R/sleep_detection.R")
source("R/result_saving.R")
source("R/plotting.R")

data_path <- "data/"
report_path <- "reports/"
output_path <- "results/"

hr_data_list <- load_hr_data(ids, data_path)
sleep_data_list <- load_sleep_data(ids, report_path)

for (id in ids) {
  hr_data1 <- hr_data_list[[id]]
  sleep_data <- sleep_data_list[[id]]
  
  sleep_sessions <- extract_sleep_sessions(sleep_data)
  save_hr_data(hr_data1, id, output_path)

  plots <- plot_sleep_detection(hr_data1, sleep_sessions, id, date_range, date_labels)
  save_plot(plots$p1, id, output_path, "p1")
  save_plot(plots$p2, id, output_path, "p2")
}
