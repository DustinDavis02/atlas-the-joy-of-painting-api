import pandas as pd
import os
import sys
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Environment variables
load_dotenv()

# Database credentials
USERNAME = os.getenv('MYSQL_USERNAME', 'root')
PASSWORD = os.getenv('MYSQL_PASSWORD', '')
HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_NAME = os.getenv('MYSQL_DB_NAME', 'JoyOfPaintingDB')

# SQLAlchemy setup
engine = create_engine(f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DB_NAME}')
Session = sessionmaker(bind=engine)
session = Session()

# Table models
metadata = MetaData()
subject_matter = Table('SubjectMatter', metadata, autoload_with=engine)
episode_subject_matter = Table('EpisodeSubjectMatter', metadata, autoload_with=engine)

# Load transformed data
episode_subject_df = pd.read_csv('src/data_cleaning/transformed_episodesubjectmatter.csv')

# Extract unique subjects for SubjectMatter table
unique_subjects = episode_subject_df['SubjectName'].unique()
subject_data = [{'SubjectName': subject} for subject in unique_subjects]

# Retrieve existing subjects from the database (if any)
existing_subjects = pd.read_sql('SELECT SubjectName FROM SubjectMatter', engine)['SubjectName'].tolist()

# Insert SubjectMatter data and retrieve SubjectName to SubjectID mapping
subject_id_map = {}
try:
    for data in subject_data:
        subject_name = data['SubjectName']
        if subject_name not in existing_subjects:
            ins = subject_matter.insert().values(**data)
            result = session.execute(ins)
            subject_id = result.inserted_primary_key[0]
        else:
            subject_id = session.execute(select(subject_matter.c.SubjectID).where(subject_matter.c.SubjectName == subject_name)).scalar()
        subject_id_map[subject_name] = subject_id
    session.commit()
except Exception as e:
    print(f"Error loading SubjectMatter data: {e}", file=sys.stderr)
    session.rollback()

# Insert EpisodeSubjectMatter data
try:
    for _, row in episode_subject_df.iterrows():
        subject_id = subject_id_map.get(row['SubjectName'])
        if subject_id:
            ins = episode_subject_matter.insert().values(EpisodeID=row['EpisodeID'], SubjectID=subject_id)
            session.execute(ins)
    session.commit()
except Exception as e:
    print(f"Error loading EpisodeSubjectMatter data: {e}", file=sys.stderr)
    session.rollback()

session.close()
print("Data loaded into SubjectMatter and EpisodeSubjectMatter tables.")