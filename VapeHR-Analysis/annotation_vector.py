import numpy as np
import pandas as pd

def create_annotation_vectors(eventdata, all_matrix_profiles, filtered_uids):
    """
    Create annotation vectors based on event times for each user.

    Args:
        eventdata (DataFrame): DataFrame containing event data with a 'UID' column and 'isoDate' timestamps.
        all_matrix_profiles (DataFrame): DataFrame containing matrix profiles with 'user_id' and 'time' columns.
        filtered_ids (list): List of user IDs to process.

    Returns:
        annotation_vectors (dict): Dictionary where keys are user IDs and values are annotation vectors (numpy arrays).
    """
    # Calculate time differences between consecutive events for each user
    eventdata['time_diff'] = eventdata.groupby('ID')['Date'].diff().fillna(pd.Timedelta(seconds=0))

    annotation_vectors = {}

    for user_id in filtered_uids:
        # Filter data for the current user
        user_data = all_matrix_profiles[all_matrix_profiles['user_id'] == user_id]
        user_events = eventdata[eventdata['ID'] == user_id]

        # Initialize an annotation vector with zeros
        annotations = np.zeros(len(user_data))

        # Iterate over each event and assign annotation values
        for _, event in user_events.iterrows():
            event_time = event['Date']

            # Define time intervals before and after the event
            before_start = event_time - pd.Timedelta(minutes=60)
            after_end = event_time + pd.Timedelta(minutes=60)

            # Identify indices corresponding to these intervals
            before_indices = (user_data['time'] >= before_start) & (user_data['time'] < event_time)
            after_indices = (user_data['time'] > event_time) & (user_data['time'] <= after_end)

            # Assign annotations
            annotations[before_indices] = 1
            annotations[after_indices] = 2

        # Store the annotation vector for the current user
        annotation_vectors[user_id] = annotations

    return annotation_vectors
