#!/bin/sh
mysqldump -ucotto -psupervis --add-drop-table --extended-insert --quote-names --databases cotto > /root/cotto_db_backup/mysql.cotto.$(date "+%Y%m%d").sql
gzip /root/cotto_db_backup/mysql.cotto.$(date "+%Y%m%d").sql
