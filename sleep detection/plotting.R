# plotting.R

library(ggplot2)
library(patchwork)

create_and_save_plots <- function(hr_data1, sleep_sessions_df, id, output_path, id_index) {
  hr_data1$dt <- as.POSIXct(hr_data1$dt, format = "%Y-%m-%dT%H:%M:%OS", tz = "UTC")
  
  date_range <- seq(from = min(hr_data1$dt), to = max(hr_data1$dt), by = "day")
  date_labels <- paste("Day", seq_along(date_range))
  
  hr_data1$sleepornot_num <- as.numeric(as.character(hr_data1$sleepornot)) * 60 + 40
  
  p1 <- ggplot(data = hr_data1, aes(x = dt)) +
    geom_point(aes(y = hr_imp), color = "grey", size = 1) +
    geom_line(aes(y = fitted_hr), color = "black", size = 2) +
    labs(title = paste("Participant", id_index), x = "", y = "Heart Rate") +
    theme_minimal(base_size = 25) + 
    theme(
      plot.background = element_rect(fill = "white", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      axis.text.x = element_blank(),
      axis.ticks.x = element_blank(),
      axis.title.x = element_blank(),
      legend.position = "none"
    )
  p2 <- ggplot(data = hr_data1, aes(x = dt)) +
    geom_rect(data = sleep_sessions_df, aes(xmin = Start, xmax = End, ymin = 40, ymax = 100), fill = "gray", alpha = 0.5, inherit.aes = FALSE) +
    geom_line(aes(y = sleepornot_num), color = "black", size = 1) +
    labs(x = "Day", y = "Sleep State") +
    scale_x_datetime(
      breaks = date_range,
      labels = date_labels
    ) +
    theme_minimal(base_size = 25)
  
  combined_plot <- p1 / p2
  
  file_name <- paste0(output_path, "subplots/", id, "_sleepremove.png")
  ggsave(file_name, plot = combined_plot, width = 1400/72, height = 850/72, dpi = 301, bg = "transparent")
}
