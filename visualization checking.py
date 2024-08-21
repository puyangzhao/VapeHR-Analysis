import matplotlib.pyplot as plt
import pandas as pd

def plot_vaping_frequency(eventdata, filtered_uids):
    """
    Plot the frequency of daily vaping events by user.

    Args:
        eventdata (DataFrame): DataFrame containing event data.
        filtered_ids (list): List of user IDs to plot.
    """
    # Extracting just the date from the timestamp
    eventdata['date'] = eventdata['isoDate'].dt.date
    # Grouping by UID and date and counting the number of events
    smoking_frequency = eventdata.groupby(['ID', 'date']).size().reset_index(name='smoking_count')

    # Plot using Matplotlib
    fig, ax = plt.subplots(dpi=301)

    for user in filtered_uids:
        user_data = smoking_frequency[smoking_frequency['UID'] == user]
        ax.bar(user_data['smoking_count'].value_counts().index,
               user_data['smoking_count'].value_counts().values, label=user)

    ax.set_xlabel("Vaping Count")
    ax.set_ylabel("Frequency")
    ax.set_title("Frequency of Daily Vaping Events by User")
    ax.legend(title="User ID", bbox_to_anchor=(1.05, 1), loc='best')
    plt.show()
