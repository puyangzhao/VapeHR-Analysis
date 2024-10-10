import numpy as np
import pandas as pd

def correct_matrix_profiles(all_matrix_profiles, annotation_vectors):
    """
    Correct matrix profiles based on annotation vectors.

    Args:
        all_matrix_profiles (DataFrame): DataFrame containing all users' matrix profiles.
        annotation_vectors (dict): Dictionary where keys are user IDs and values are annotation vectors.

    Returns:
        corrected_matrix_profiles (dict): Dictionary with corrected matrix profiles for each user.
        all_corrected_profiles (DataFrame): DataFrame containing corrected matrix profiles for all users.
    """
    corrected_matrix_profiles = {}
    all_corrected_profiles = pd.DataFrame()

    for user_id, user_data in all_matrix_profiles.groupby('user_id'):
        if user_id in annotation_vectors:
            original_mp = user_data['matrix_profile'].values
            annotation_vector = annotation_vectors[user_id]

            # Ensure that the lengths match
            min_length = min(len(original_mp), len(annotation_vector))
            original_mp = original_mp[:min_length]
            annotation_vector = annotation_vector[:min_length]

            # Compute the maximum matrix profile value
            max_mp_value = np.max(original_mp)

            # Calculate the corrected matrix profile
            corrected_mp = original_mp + ((1 - annotation_vector) * max_mp_value)

            # Store the corrected profile for this user
            corrected_matrix_profiles[user_id] = corrected_mp

            # Create a DataFrame to store the time, corrected matrix profile, and annotation vector for this user
            corrected_profile_df = pd.DataFrame({
                'time': user_data['time'].iloc[:min_length],
                'corrected_matrix_profile': corrected_mp,
                'AVS': annotation_vector,
                'user_id': user_id
            })

            all_corrected_profiles = pd.concat([all_corrected_profiles, corrected_profile_df], ignore_index=True)

    return corrected_matrix_profiles, all_corrected_profiles
