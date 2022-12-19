#!/bin/sh
 
# Name of your flarum database
databases="flarum_forum"
 
# Directory name for temp copy
tempcopydir="tempdir"
 
# Directory where is your flarum folder
flarumdir=/your_path_to/flarum
copyassets="y"
 
# Directory where you want the backup files to be placed
backupdir=/your_path_to/flarum/copy/$tempcopydir
 
# Autoupdate turn on/off
autoupdate="y"
 
# MySQL dump command, use the full path name here
mysqldumpcmd=/usr/bin/mysqldump
 
# MySQL Username and password
userpassword=" --user=databaseuser --password=databasepassword"
 
# MySQL dump options
dumpoptions=" --quick --add-drop-table --add-locks --extended-insert --lock-tables --no-tablespaces"
 
# Unix Commands
gzip=/bin/gzip
 
# Get the Day of the Week (0-6)
DOW=`date +%w`
 
# Create our backup directory if not already there
mkdir -p ${backupdir}
if [ ! -d ${backupdir} ] 
then
   echo "Not a directory: ${backupdir}"
   exit 1
fi
 
# Dump all of our databases
echo "Dumping MySQL Database"
for database in $databases
do
   $mysqldumpcmd $userpassword $dumpoptions $database > ${backupdir}/${DOW}-${database}.sql
done
 
# Compress database backup files
echo "Compressing database Files"
for database in $databases
do
   rm -f ${backupdir}/${DOW}-${database}.sql.gz
   $gzip ${backupdir}/${DOW}-${database}.sql
done
 
echo "Copy composer.json and public/assets"
if [ $copyassets = "y" ]
then
   cp composer.json $backupdir/composer.json
   mkdir -p $backupdir/public/assets
   cp -R public/assets $backupdir/public
   echo "Comporessing all files, and copy them to flarum folder"
   tar -czvf Flarum-AutoUpdate.tar.gz $tempcopydir
   pwd
fi
 
echo "List of files and dirs copied."
ls -l ${backupdir}
echo "Autocopy completed!"
 
if [ $autoupdate = "y" ]
then
   echo "Autoupdate turned on.."
   composer update --prefer-dist --no-plugins --no-dev -a --with-all-dependencies
   php flarum migrate
   php flarum cache:clear
   echo "Flarum was copied and updated automatically."
fi
exit