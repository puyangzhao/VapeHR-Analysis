from data_loader import fetch_data
from process_all_users import process_all_users
from annotation_vector import create_annotation_vectors
from correct_matrix_profile import correct_matrix_profiles
from motif_detection import find_motifs_per_user, filter_motifs
from regression_analysis import perform_regression_analysis, plot_regression_results, perform_t_tests

# Load eventdata
# eventdata = pd.read_csv('path_to_eventdata.csv')

# Define the list of user IDs to process
# filtered_ids = ['user1', 'user2', ...]

# Process all users to compute matrix profiles
all_matrix_profiles, hr_nosleep_df = process_all_users(filtered_ids, eventdata)

# Create annotation vectors for all users
annotation_vectors = create_annotation_vectors(eventdata, all_matrix_profiles, filtered_ids)

# Correct the matrix profiles using annotation vectors
corrected_matrix_profiles, all_corrected_profiles = correct_matrix_profiles(all_matrix_profiles, annotation_vectors)

# Detect motifs
motifs_results = []
for user_id in all_corrected_profiles['user_id'].unique():
    user_data = all_corrected_profiles[all_corrected_profiles['user_id'] == user_id]
    user_motifs = find_motifs_per_user(user_data, 10)
    motifs_results.extend(user_motifs)

motifs_df = pd.DataFrame(motifs_results)
motifs_df.to_csv("results/detailed_ids_identified_potential_motifs.csv", index=False)

# Perform regression analysis
regression_df = perform_regression_analysis(motifs_df, hr_nosleep_df, eventdata)
regression_df.to_csv("hou_basic_ids_regression_results.csv", index=False)

# Plot regression results
plot_regression_results(regression_df)

# Perform t-tests
t_test_results = perform_t_tests(regression_df)

# Output t-test results
for user_id, result in t_test_results.items():
    print(f"User ID {user_id} - t-statistic: {result['t_stat']}, p-value: {result['p_val']}")
