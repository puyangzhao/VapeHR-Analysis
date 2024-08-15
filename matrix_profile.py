import stumpy
import pandas as pd

def compute_matrix_profile(data, window_size):
    if len(data) < window_size:
        return None
    stumpy.config.STUMPY_EXCL_ZONE_DENOM = 0.5
    mp = stumpy.stump(data['hr_imp'], m=window_size, normalize=False)
    mp_df = pd.DataFrame({
        'time': data['dt'][0:len(mp[:, 0])],
        'matrix_profile': mp[:, 0]
    })
    return mp_df
