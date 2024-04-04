from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os
import re
from datetime import datetime
import sys
from dotenv import load_dotenv

# Environment variables
load_dotenv()

# Environment variables for database credentials
USERNAME = os.getenv('MYSQL_USERNAME', 'root')
PASSWORD = os.getenv('MYSQL_PASSWORD', '')
HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_NAME = os.getenv('MYSQL_DB_NAME', 'JoyOfPaintingDB')

# SQLAlchemy engine and session setup
engine = create_engine(f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DB_NAME}')
Session = sessionmaker(bind=engine)

# Episodes table model
metadata = MetaData()
episodes = Table('Episodes', metadata,
                 Column('EpisodeID', String(10), primary_key=True),
                 Column('Title', String(255)),
                 Column('AirDate', Date))

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

# Function to generate EpisodeID in 'SXXEXX' format
def generate_episode_id(season, episode):
    return f"S{str(season).zfill(2)}E{str(episode).zfill(2)}"

# Function to parse the file
def parse_line(line, season, episode):
    match = re.match(r'"(.+?)" \(([^)]+)\)', line)
    if match:
        title, date_str = match.groups()
        title = standardize_title(title)
        date_obj = datetime.strptime(date_str, '%B %d, %Y')
        episode_id = generate_episode_id(season, episode)
        return {'EpisodeID': episode_id, 'Title': title, 'AirDate': date_obj.strftime('%Y-%m-%d')}
    return None

# Read and parse the file
data = []
season = 1
episode = 1

with open('datasets/The Joy Of Painting - Episode Dates', 'r') as file:
    for line in file:
        parsed_line = parse_line(line, season, episode)
        if parsed_line:
            data.append(parsed_line)
            episode += 1
        if episode > 13:
            season += 1
            episode = 1

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to load DataFrame to database
def load_data_to_db(df):
    session = Session()
    try:
        for _, row in df.iterrows():
            ins = episodes.insert().values(EpisodeID=row['EpisodeID'], Title=row['Title'], AirDate=row['AirDate'])
            session.execute(ins)
        session.commit()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        session.rollback()
    finally:
        session.close()

# Load the data into the database
load_data_to_db(df)