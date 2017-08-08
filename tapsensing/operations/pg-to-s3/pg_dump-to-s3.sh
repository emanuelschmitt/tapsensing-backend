#!/bin/bash

set -e

# Database credentials
PG_HOST="localhost"
PG_DB="tapsensing"
PG_USER="tapsensing"
PG_PASS="XXX"

# S3
S3_PATH="tapsensing/dumps"

# get databases list
dbs=("$@")

# Vars
NOW=$(date +"%m-%d-%Y-at-%H-%M-%S")
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Dump database
PGPASSWORD=$PG_PASS pg_dump -Fc -h $PG_HOST -U $PG_USER $PG_DB > /tmp/"$NOW"_"$db".dump

# Copy to S3
aws s3 cp /tmp/"$NOW"_"$db".dump s3://$S3_PATH/"$NOW"_"$db".dump --storage-class STANDARD_IA

# Delete local file
rm /tmp/"$NOW"_"$db".dump

# Log
echo "* Database $db is archived"

# Delere old files
echo "* Delete old backups";
$DIR/s3-autodelete.sh $S3_PATH "7 days"
