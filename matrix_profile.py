import pandas as pd
import stumpy

def compute_matrix_profile(data, window_size):
    """
    Compute the matrix profile for heart rate data.

    Args:
        data (DataFrame): Heart rate data.
        window_size (int): Window size for matrix profile calculation.

    Returns:
        mp_df (DataFrame): DataFrame containing time and matrix profile values.
    """
    # Return None if the data is shorter than the window size
    if len(data) < window_size:
        return None
    # Ensure that time information is preserved after computing the matrix profile
    stumpy.config.STUMPY_EXCL_ZONE_DENOM = 0.5
    # Calculate the matrix profile for 'hr_imp' column with the specified window size, without normalization
    mp = stumpy.stump(data['hr_imp'], m=window_size, normalize=False)
    # Create a DataFrame with the matrix profile and the corresponding time values
    mp_df = pd.DataFrame({
        'time': data['dt'][0:len(mp[:, 0])],  # Preserve the time column
        'matrix_profile': mp[:, 0]            # Matrix profile values
    })
    return mp_df
