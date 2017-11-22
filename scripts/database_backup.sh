#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP_DIR=/home/jihun/database_backup/
mysqldump -u $MEMORIST_MYSQL_USER -p$MEMORIST_MYSQL_PASSWORD $MEMORIST_MYSQL_NAME > $BACKUP_DIR"memorist_db_backup_"$DATE.sql
find $BACKUP_DIR -ctime +3 -exec rm -f {} \;
