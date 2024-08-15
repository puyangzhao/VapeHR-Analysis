import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

def perform_regression_analysis(motifs_df, hr_nosleep_df, eventdata):
    """
    Perform regression analysis on heart rate data and detected motifs.

    Args:
        motifs_df (DataFrame): DataFrame containing detected motifs.
        hr_nosleep_df (DataFrame): DataFrame containing non-sleep heart rate data.
        eventdata (DataFrame): DataFrame containing event data.

    Returns:
        regression_df (DataFrame): DataFrame containing regression results for each motif.
    """
    regression_results = []

    for user_id in motifs_df['User_ID'].unique():
        user_hr_data = hr_nosleep_df[hr_nosleep_df['UID'] == user_id].copy()
        user_hr_data['dt'] = pd.to_datetime(user_hr_data['dt'])
        user_hr_data = user_hr_data.sort_values(by='dt').reset_index(drop=True)

        user_motifs = motifs_df[motifs_df['User_ID'] == user_id]
        user_events = eventdata[eventdata['UID'] == user_id].copy()
        user_events.loc[:, 'isoDate'] = pd.to_datetime(user_events['isoDate'])

        for _, row in user_motifs.iterrows():
            motif_time = row['Time']
            motif_period = row['Period']
            motif_index = user_hr_data[user_hr_data['dt'] == motif_time].index.min()

            if pd.notna(motif_index):
                start_index = max(motif_index, 0)
                end_index = min(motif_index + 20, len(user_hr_data) - 1)
                segment = user_hr_data.iloc[start_index:end_index + 1]

                if not segment[segment['dt'].isin(user_events['isoDate'])].empty:
                    continue

                X = np.arange(-10, 11).reshape(-1, 1)
                y = segment['hr_imp'].values

                if len(X) == len(y)):
                    model = LinearRegression()
                    model.fit(X, y)
                    r_squared = model.score(X, y)

                    regression_results.append({
                        'user_id': user_id,
                        'time': motif_time,
                        'slope': model.coef_[0],
                        'intercept': model.intercept_,
                        'r_squared': r_squared,
                        'period': motif_period
                    })

    regression_df = pd.DataFrame(regression_results)
    return regression_df

def plot_regression_results(regression_df):
    """
    Plot regression results using bar plots and box plots.

    Args:
        regression_df (DataFrame): DataFrame containing regression results.
    """
    good_fit_df = regression_df[regression_df['r_squared'] > 0.8]
    average_r_squared_good = good_fit_df.groupby('user_id')['r_squared'].mean().reset_index()

    plt.figure(figsize=(12, 8), dpi=301)
    barplot = sns.barplot(x='user_id', y='r_squared', data=average_r_squared_good)
    barplot.set_xticklabels(barplot.get_xticklabels(), rotation=45)
    plt.title('High R² Values by User (R² > 0.8)')
    plt.xlabel('User ID')
    plt.ylabel('Average R²')
    plt.show()

    good_fit_df['period_numeric'] = good_fit_df['period'].replace({'non-vaping': 0, 'before': 1, 'after': 2})
    plot_boxplots(good_fit_df)
    run_mixed_effect_models(good_fit_df)

def plot_boxplots(good_fit_df):
    """
    Plot boxplots for slopes and intercepts.

    Args:
        good_fit_df (DataFrame): DataFrame containing regression results with good fit.
    """
    plt.figure(figsize=(14, 11), dpi=301)
    sns.set(style="whitegrid")

    plt.subplot(2, 1, 1)
    slope_plot = sns.boxplot(x='user_id', y='slope', hue='period', data=good_fit_df)
    plt.title('Boxplot of Slopes Before and After for Each User ID')
    plt.xlabel('User ID')
    plt.ylabel('Slope')
    plt.xticks(rotation=90)

    plt.subplot(2, 1, 2)
    intercept_plot = sns.boxplot(x='user_id', y='intercept', hue='period', data=good_fit_df)
    plt.title('Boxplot of Intercepts Before and After for Each User ID')
    plt.xlabel('User ID')
    plt.ylabel('Intercept')
    plt.xticks(rotation=90)

    plt.tight_layout()
    plt.savefig("plots/Boxplot_before_vape_report.png", dpi=400)
    plt.show()

def run_mixed_effect_models(good_fit_df):
    """
    Run mixed-effect models to analyze the effect of period on slope and intercept.

    Args:
        good_fit_df (DataFrame): DataFrame containing regression results with good fit.
    """
    filtered_df = good_fit_df[good_fit_df['period'].isin([0, 1])]
    model_avg = smf.mixedlm("slope ~ period_numeric", filtered_df, groups=filtered_df["user_id"], re_formula="~1")
    result_avg = model_avg.fit()
    print("Model for Average Heart Rate:")
    print(result_avg.summary())

    model_change = smf.mixedlm("intercept ~ period_numeric", filtered_df, groups=filtered_df["user_id"], re_formula="~1")
    result_change = model_change.fit()
    print("\nModel for Change in Heart Rate:")
    print(result_change.summary())

def perform_t_tests(good_fit_df):
    """
    Perform paired t-tests on slope data before and after vaping.

    Args:
        good_fit_df (DataFrame): DataFrame containing regression results with good fit.

    Returns:
        dict: Dictionary with t-test results for each user.
    """
    results = {}

    for user_id in good_fit_df['user_id'].unique():
        user_data = good_fit_df[good_fit_df['user_id'] == user_id]
        before = user_data[user_data['period'] == 'before']['slope'].dropna()
        after = user_data[user_data['period'] == 'after']['slope'].dropna()

        min_len = min(len(before), len(after))
        if min_len > 0:
            before = before.iloc[:min_len]
            after = after.iloc[:min_len]
            t_stat, p_val = stats.ttest_rel(before, after)
            results[user_id] = {'t_stat': t_stat, 'p_val': p_val}

    return results
