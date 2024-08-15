# plotting.R

library(ggplot2)

plot_sleep_detection <- function(hr_data1, sleep_sessions_df, id, date_range, date_labels) {
  p1 <- ggplot(data = hr_data1, aes(x = dt)) +
    geom_point(aes(y = hr_imp), color = "grey", size = 3) +
    geom_line(aes(y = fitted_hr), color = "black", size = 3) +
    labs(title = paste("Participant", id), x = "", y = "Heart Rate") +  
    theme_minimal(base_size = 55) + 
    theme(
      plot.background = element_rect(fill = "white", colour = NA),
      panel.background = element_rect(fill = "white", colour = NA),
      axis.text.x = element_blank(),
      axis.ticks.x = element_blank(),
      axis.title.x = element_blank(),
      legend.position = "none"
    )
  
  p2 <- ggplot(data = hr_data1, aes(x = dt)) +
    geom_rect(data = sleep_sessions_df, aes(xmin = Start, xmax = End, ymin = 0, ymax = 100), fill = "gray", alpha = 0.5, inherit.aes = FALSE) +
    geom_line(aes(y = sleepornot_num), color = "black", size = 3) +
    labs(x = "Time", y = "Sleep State") +
    scale_x_datetime(
      breaks = date_range,  
      labels = date_labels  
    ) +
    theme_minimal(base_size = 55)+
    theme(axis.title.x = element_text(size = 55), 
          axis.title.y = element_text(size = 55) 
    )
  return(list(p1 = p1, p2 = p2))
}
