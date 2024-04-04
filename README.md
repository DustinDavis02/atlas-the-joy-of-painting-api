
# Atlas: The Joy of Painting API

## Project Overview

This project aims to provide an accessible database and API for fans of "The Joy of Painting" to filter through 403 episodes based on the month of original broadcast, subject matter, and color palette. This ETL (Extract, Transform, Load) project consolidates data from multiple sources into a centralized database, making it usable for a frontend application designed for viewer interaction.

## Features

- **Data Integration**: Consolidates episode information from various file formats and databases into a single structured database.
- **Flexible Filtering**: Allows users to filter episodes based on the month, subject matter, and color palette, with support for multiple filters simultaneously.

## Getting Started

### Prerequisites

- SQL database (MySQL)
- Python 3.x
- Relevant Python packages (pandas, sqlalchemy, python-dotenv)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Dustindavis02/atlas-the-joy-of-painting-api.git
   ```
<!-- 2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ``` -->

### Setting Up the Database

1. Navigate to the `database` folder and run the SQL scripts to create your database structure:
   ```
   mysql -u <your-username> -p <your-database-name> < create_database.sql
   ```

### Running the ETL Process

1. Execute the ETL scripts to populate the database:
   ```
   python clean_data.py
   python transform_colors.py
   python transform_subjectmatter.py
   python load_colors.py
   python load_episodes.py
   python load_subjectmatter.py
   ```

## Contributing

Feel free to fork the project and submit pull requests with improvements or bug fixes. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
