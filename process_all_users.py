import pandas as pd
from data_loader import fetch_data
from matrix_profile import compute_matrix_profile

def process_all_users(filtered_uids, eventdata, segment_length=20):
    """
    Process heart rate data for all users and compute matrix profiles.

    Args:
        filtered_uids (list): List of user IDs to process.
        eventdata (DataFrame): DataFrame containing event data.
        segment_length (int): Window size for matrix profile calculation.

    Returns:
        all_matrix_profiles (DataFrame): DataFrame with matrix profiles for all users.
        hr_nosleep_df (DataFrame): DataFrame with non-sleep heart rate data for all users.
    """
    # Initialize DataFrames to store all users' matrix profiles and non-sleep HR data
    all_matrix_profiles = pd.DataFrame()
    hr_nosleep_df = pd.DataFrame()

    for ID in filtered_uids:
        # Fetch event data, full HR data, and non-sleep HR data for each user
        eventdata_, hr_data, hr_nosleep = fetch_data(ID, eventdata)
        hr_nosleep_df = pd.concat([hr_nosleep_df, hr_nosleep], ignore_index=True)

        # Compute the matrix profile for the non-sleep HR data
        user_matrix_profile = compute_matrix_profile(hr_nosleep, window_size=segment_length)
        user_matrix_profile['user_id'] = ID  # Add user ID to the matrix profile DataFrame
        all_matrix_profiles = pd.concat([all_matrix_profiles, user_matrix_profile], ignore_index=True)

    # Optionally save the accumulated matrix profiles to a CSV file
    all_matrix_profiles.to_csv("results/all_users_matrix_profiles.csv", index=False)
    
    return all_matrix_profiles, hr_nosleep_df
