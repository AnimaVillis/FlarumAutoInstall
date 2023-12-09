# AutoUpdate Script

AutoUpdate Script is a Python tool for automating the backup and update process of a Flarum forum database. 
The script allows users to create a backup, copy necessary files, and perform an automatic update of their Flarum installation.

## Features

- **Automated Backup:** Schedule regular backups of the specified Flarum forum database.
- **Configurable Settings:** Customize the backup and update process using a configuration file (config.json).
- **Automatic Folder Creation:** Ensure necessary folders are created automatically during the backup and update process.

## Requirements

- Python 3.x
- mysql-connector-python

## Usage

1. Clone the repository: `git clone https://github.com/AnimaVillis/FlarumAutoScripts.git`
2. Configure the script using the `config.json` file.
3. Run the script: `python auto_update.py`

## Author

AnimaVillis - [GitHub Profile](https://github.com/AnimaVillis)

## License

This project is licensed under the MIT License.
