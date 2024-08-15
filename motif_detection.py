import numpy as np
import pandas as pd

def find_motifs_per_user(user_data, percentile=90):
    """
    Identify the smallest 90% of corrected_matrix_profile values for each user, by date and AVS value.

    Args:
        user_data (DataFrame): DataFrame containing user data with corrected matrix profiles.
        percentile (int): Percentile value to use for motif detection.

    Returns:
        list: List of motifs identified.
    """
    results = []
    user_data['time'] = pd.to_datetime(user_data['time'])
    user_data['date'] = user_data['time'].dt.date

    grouped_data = user_data.groupby(['date', 'AVS'])

    for (date, avs_value), group_data in grouped_data:
        cutoff = np.percentile(group_data['corrected_matrix_profile'], percentile)
        selected_indices = group_data[group_data['corrected_matrix_profile'] <= cutoff]

        for _, row in selected_indices.iterrows():
            results.append({
                'Time': row['time'],
                'Index': row.name,
                'Period': avs_value,
                'mp': row['corrected_matrix_profile'],
                'User_ID': row['user_id']
            })

    return results

def filter_motifs(motifs_df):
    """
    Filter the motifs based on certain criteria.

    Args:
        motifs_df (DataFrame): DataFrame containing all detected motifs.

    Returns:
        DataFrame: Filtered motifs DataFrame.
    """
    filtered_motifs = pd.DataFrame()
    last_accepted_index = -np.inf

    for i in range(len(motifs_df)):
        if i == 0:
            filtered_motifs = pd.concat([filtered_motifs, motifs_df.iloc[[i]]], ignore_index=True)
            last_accepted_index = motifs_df.iloc[i]['Index']
        else:
            current_row = motifs_df.iloc[i]
            previous_row = filtered_motifs.iloc[-1]

            if abs(current_row['Index'] - last_accepted_index) < 40:
                if current_row['mp'] < previous_row['mp']:
                    filtered_motifs.iloc[-1] = current_row
                    last_accepted_index = current_row['Index']
            else:
                filtered_motifs = pd.concat([filtered_motifs, motifs_df.iloc[[i]]], ignore_index=True)
                last_accepted_index = current_row['Index']

    return filtered_motifs
