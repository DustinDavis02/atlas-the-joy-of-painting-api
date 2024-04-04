import pandas as pd
import re

# Function that read and process the Episode Dates text file
def read_episode_dates(file_path):
    titles = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(r'"(.+?)" \((.+)\)', line.strip())
            if match:
                title = match.group(1)
                titles.append(title)
    return titles

# Load the Episode Dates dataset
episode_dates_titles = read_episode_dates('datasets/The Joy Of Painting - Episode Dates')

# Load the Colors Used dataset
df_colors_used = pd.read_csv('datasets/The Joy Of Painiting - Colors Used')

# Load the Subject Matter datset
df_subject_matter = pd.read_csv('datasets/The Joy Of Painiting - Subject Matter')

# Function that standardize titles
def standardize_title(title):
    title = title.replace('Mt.', 'Mount').replace('"', '').strip()
    return title.title()

# Standardize titles for datasets
episode_dates_titles = [standardize_title(title) for title in episode_dates_titles]
df_colors_used['painting_title'] = df_colors_used['painting_title'].apply(standardize_title)
df_subject_matter['TITLE'] = df_subject_matter['TITLE'].apply(standardize_title)

# Extract the unique titles
titles_episode_dates = set(episode_dates_titles)
titles_colors_used = set(df_colors_used['painting_title'])
titles_subject_matter = set(df_subject_matter['TITLE'])

# Finds the differences
diff_colors_vs_dates = titles_colors_used.difference(titles_episode_dates)
diff_subject_vs_dates = titles_subject_matter.difference(titles_episode_dates)
diff_dates_vs_colors_subject = titles_episode_dates.difference(titles_colors_used.union(titles_subject_matter))

# Output the differences
print("Differences - Colors vs Dates:\n", diff_colors_vs_dates)
print("\nDifferences - Subject Matter vs Dates:\n", diff_subject_vs_dates)
print("\nDifferences - Dates vs Colors and Subject Matter:\n", diff_dates_vs_colors_subject)