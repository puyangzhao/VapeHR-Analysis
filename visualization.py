import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_heart_rate_data(user_hr_data, user_events, filtered_motifs, date, user_id):
    """
    Plot heart rate data with annotations for vaping events and detected motifs.

    Args:
        user_hr_data (DataFrame): DataFrame containing the user's heart rate data.
        user_events (DataFrame): DataFrame containing the user's vaping events.
        filtered_motifs (DataFrame): DataFrame containing the filtered motifs.
        date (str): Date to plot.
        user_id (str): User ID.
    """
    plt.figure(figsize=(32, 6), dpi=301)

    group = user_hr_data[user_hr_data['date'] == date]

    plt.plot(group['dt'], group['hr_imp'], label='Heart Rate', linestyle='-', marker='', alpha=0.5)

    daily_events = user_events[user_events['isoDate'].dt.date == date]
    for idx, event in enumerate(daily_events.itertuples()):
        plt.axvline(x=event.isoDate, color='red', linestyle='--', linewidth=1, label='Vaping Event' if idx == 0 else "")

    daily_motifs = filtered_motifs[filtered_motifs['Time'].dt.date == date]
    for idx, motif in enumerate(daily_motifs.itertuples()):
        motif_time = motif.Time
        motif_index = group[group['dt'] == motif_time].index.min()
        start_index = max(motif_index - 10, 0)
        end_index = min(motif_index + 10, len(group) - 1)

        if pd.notna(motif_index):
            color = 'pink' if motif.Period == '2.0' else \
                    'orange' if motif.Period == '1.0' else \
                    'blue'
            plt.plot(group['dt'].iloc[start_index:end_index+1], group['hr_imp'].iloc[start_index:end_index+1],
                     color=color, label=f"{motif.Period.capitalize()} Motif" if idx == 0 else "", linewidth=2, zorder=10)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xlabel('Time')
    plt.ylabel('Heart Rate')
    plt.title(f'Heart Rate Data Visualization for User {user_id} on {date}')
    plt.legend()
    plt.show()
