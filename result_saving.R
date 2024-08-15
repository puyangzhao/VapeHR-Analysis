# result_saving.R

save_hr_data <- function(hr_data, id, output_path) {
  file_name <- file.path(output_path, paste0(id, "_imputed_hr.csv"))
  write.csv(hr_data, file_name, row.names = FALSE)
}

save_plot <- function(plot, id, output_path, plot_type = "png") {
  file_name <- file.path(output_path, paste0(id, "_sleepremove.", plot_type))
  ggsave(file_name, plot = plot, dpi = 301, bg = "transparent")
}
