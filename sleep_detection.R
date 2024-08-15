# sleep_detection.R

extract_sleep_sessions <- function(sleep_data) {
  sleep_sessions <- data.frame(Start=as.POSIXct(character()), End=as.POSIXct(character()))
  start_time <- NA
  for (i in 1:nrow(sleep_data)) {
    if (is.na(start_time) && sleep_data$type[i] != 'awake') {
      start_time <- sleep_data$isoDate[i]
    } else if (!is.na(start_time) && sleep_data$type[i] == 'awake') {
      end_time <- sleep_data$isoDate[i]
      sleep_sessions <- rbind(sleep_sessions, data.frame(Start=start_time, End=end_time))
      start_time <- NA
    } else if (!is.na(start_time) && sleep_data$type[i] != 'awake' && i > 1 && sleep_data$type[i-1] != 'awake') {
      time_diff <- difftime(sleep_data$isoDate[i], sleep_data$isoDate[i-1], units = "hours")
      if (time_diff > 3) {
        end_time <- sleep_data$isoDate[i-1]
        sleep_sessions <- rbind(sleep_sessions, data.frame(Start=start_time, End=end_time))
        start_time <- sleep_data$isoDate[i]
      }
    }
  }
  if (!is.na(start_time)) {
    end_time <- sleep_data$isoDate[nrow(sleep_data)]
    sleep_sessions <- rbind(sleep_sessions, data.frame(Start=start_time, End=end_time))
  }
  return(sleep_sessions)
}
