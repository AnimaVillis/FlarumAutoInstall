import os
import subprocess
import shutil
import tarfile
import datetime
import json

try:
    import mysql.connector
except ImportError:
    print("The mysql-connector-python library is missing. I'm installing...")
    subprocess.run(["pip", "install", "mysql-connector-python"])

def load_config():
    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
    
    return config_data

config_data = load_config()

database_name = config_data['database']['name']
tempcopydir = config_data['tempcopydir']
flarumdir = config_data['flarumdir']
copyassets = config_data['copyassets']
backupdir = config_data['backupdir']
autoupdate = config_data['autoupdate']
mysqldumpcmd = config_data['mysqldumpcmd']
user = config_data['user']
password = config_data['password']
dumpoptions = config_data['dumpoptions']
gzip = config_data['gzip']

DOW = datetime.datetime.now().strftime("%w")

os.makedirs(backupdir, exist_ok=True)

print(f"Dumping MySQL Database '{database_name}'")
subprocess.run([mysqldumpcmd, f"--user={user}", f"--password={password}", *dumpoptions.split(), database_name],
               stdout=open(f"{backupdir}/{DOW}-{database_name}.sql", "w"),
               stderr=subprocess.PIPE,
               text=True,
               check=True)

print("Compressing database File")
try:
    subprocess.run([gzip, f"{backupdir}/{DOW}-{database_name}.sql"],
                   stderr=subprocess.PIPE,
                   check=True)
except subprocess.CalledProcessError as e:
    print(f"Error compressing {DOW}-{database_name}.sql: {e.stderr}")

if not os.path.exists(tempcopydir):
    os.makedirs(tempcopydir)

print("Copy composer.json, composer.lock and public/assets")
if copyassets.lower() == "y":
    shutil.copy(os.path.join(flarumdir, "composer.json"), backupdir)
    shutil.copy(os.path.join(flarumdir, "composer.lock"), backupdir)
    shutil.copytree(os.path.join(flarumdir, "public/assets"), os.path.join(backupdir, "public/assets"))
    
    print("Compressing all files, and copy them to flarum folder")
    
    if not os.path.exists(os.path.join(flarumdir, tempcopydir)):
        os.makedirs(os.path.join(flarumdir, tempcopydir))
    
    with tarfile.open(f"{flarumdir}/Flarum-AutoUpdate.tar.gz", "w:gz") as tar:
        tar.add(tempcopydir, arcname=os.path.basename(tempcopydir))

    print("List of files and dirs copied.")
    print(os.listdir(backupdir))
    print("Autocopy completed!")

if autoupdate.lower() == "y":
    print("Autoupdate turned on..")
    subprocess.run(["composer", "update", "--prefer-dist", "--no-plugins", "--no-dev", "-a", "--with-all-dependencies"],
                   cwd=flarumdir,
                   stderr=subprocess.PIPE,
                   check=True)
    subprocess.run(["php", "flarum", "migrate"], cwd=flarumdir, check=True)
    subprocess.run(["php", "flarum", "cache:clear"], cwd=flarumdir, check=True)
    print("Flarum was copied and updated automatically.")
