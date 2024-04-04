import pandas as pd
import re

# Function to standardize episode titles
def standardize_title(title):
    # Initial standardization
    title = title.replace('Mt.', 'Mount').replace('"', '').strip()
    title = title.title()

    # Specific replacements
    special_cases = {
        "The Old Home Place": "Old Home Place",
        "Shades Of Grey": "Shades Of Gray",
        "Hide A Way Cove": "Hide-A-Way Cove",
        "Evening At Sunset": "Evening Sunset",
        "Autumn Mountain": "Autumn Mountains",
        "Golden Rays Of Sunshine": "Golden Rays Of Sunlight",
        "Toward Days End": "Toward Day's End",
        "Evergreens At Sunset": "Evergreen At Sunset",
        "A Pretty Autumn Day": "Pretty Autumn Day",
        "Misty Forest Oval": "Misty Forest",
        "Quiet Mountains River": "Quiet Mountain River",
        "The Footbridge": "Footbridge",
        "Forest Down Oval": "Forest Dawn Oval",
        "Storm'S A Comin": "Storm's A Comin'",
        "Gray Mountain": "Grey Mountain",
        "Cabin At Trails End": "Cabin At Trail's End",
        "The Old Oak Tree": "Old Oak Tree",
        "Summer In The Mountain": "Summer In The Mountains",
        "Rivers Peace": "River's Peace",
        "Mountain Path": "Mountain Pass",
        "Snow Fall": "Snowfall",
        "Half-Oval Vignette": "Half Oval Vignette",
        "Winter In Pastel": "Pastel Winter",
        "Black And White Seascape": "Black & White Seascape",
    }

    # Check if the title matches any special case
    for key, value in special_cases.items():
        if key.lower() == title.lower():
            return value

    # General handling for 's case at the end of words
    title = re.sub(r"(\w)'S(\s|$)", r"\1's\2", title)

    return title

# Load the Subject Matter dataset
subject_matter_path = 'datasets/The Joy Of Painiting - Subject Matter'
subject_matter_df = pd.read_csv(subject_matter_path)

# title standardization
subject_matter_df['TITLE'] = subject_matter_df['TITLE'].apply(standardize_title)

# Prepare DataFrame for EpisodeSubjectMatter table
subject_columns = subject_matter_df.columns[2:]
episode_subject_data = []

for _, row in subject_matter_df.iterrows():
    episode_id = row['EPISODE']
    for subject in subject_columns:
        if row[subject] == 1:
            episode_subject_data.append({'EpisodeID': episode_id, 'SubjectName': subject})

episode_subject_df = pd.DataFrame(episode_subject_data)

# Save the DataFrame to the CSV file
episode_subject_df.to_csv('src/data_cleaning/transformed_episodesubjectmatter.csv', index=False)

print("DataFrame saved as CSV file in the data_cleaning folder for review.")