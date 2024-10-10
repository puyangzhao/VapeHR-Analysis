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

process_hr_data <- function(hr_data1) {
  hr_data1$date <- as.Date(hr_data1$date)
  hr_data1$sleepornot <- rep(0, nrow(hr_data1))
  return(hr_data1)
}

detect_sleep <- function(hr_data1) {
  two_day_combinations <- hr_data1 %>%
    group_by(date) %>%
    summarise(hr_list = list(hr_imp), .groups = 'drop') %>%
    mutate(next_hr_list = lead(hr_list)) %>%
    na.omit() %>%
    mutate(combined_hr = map2(hr_list, next_hr_list, c)) %>%
    select(date, combined_hr)
  
  results <- list()
  for (i in seq_along(two_day_combinations$combined_hr)) {
    hr_data <- two_day_combinations$combined_hr[[i]]
    date_range <- two_day_combinations$date[i]
    
    s <- susie_trendfilter(hr_data, scaled_prior_variance=0, L=7)
    yres <- predict(s)
    
    actual_lengths <- table(hr_data1$date[hr_data1$date %in% c(date_range, date_range + 1)])
    first_day_length <- actual_lengths[1]
    
    inx <- which(yres[1:first_day_length] >= min(yres[1:first_day_length]) & yres[1:first_day_length] <= min(yres[1:first_day_length]) + 9.5)
    
    # 更新结果
    result <- list(date = date_range, yres = yres, sleepornot = rep(0, length(hr_data)))
    result$sleepornot[inx] <- 1
    results[[i]] <- result
  }
  return(results)
}

update_hr_data <- function(hr_data1, results) {
  for (res in results) {
    date_range <- res$date
    first_day_length <- length(res$sleepornot[1:first_day_length])
    hr_data1$sleepornot[hr_data1$date == date_range] <- res$sleepornot[1:first_day_length]
    hr_data1$fitted_hr[hr_data1$date == date_range] <- res$yres[1:first_day_length]
  }
  hr_data1 <- hr_data1 %>%
    mutate(
      dt = as.POSIXct(dt, format="%Y-%m-%dT%H:%M:%S", tz = "UTC"),
      date = as.Date(date),
      sleepornot = as.factor(sleepornot)
    )
  return(hr_data1)
}

update_sleep_report <- function(hr_data1, sleep_sessions_df) {
  sleep_sessions_df <- mutate(sleep_sessions_df,
                              Start = as.POSIXct(Start, format="%Y-%m-%d %H:%M:%S", tz = "UTC"),
                              End = as.POSIXct(End, format="%Y-%m-%d %H:%M:%S", tz = "UTC"),
                              ymin = 40,
                              ymax = 120)
  hr_data1$sleep_report <- 0
  for (i in 1:nrow(sleep_sessions_df)) {
    start_time <- sleep_sessions_df$Start[i]
    end_time <- sleep_sessions_df$End[i]
    hr_data1$sleep_report[hr_data1$dt >= start_time & hr_data1$dt <= end_time] <- 1
  }
  return(hr_data1)
}
