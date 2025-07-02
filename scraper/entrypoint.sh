#!/bin/bash
set -e

FIRST_DATE=$(cut -d',' -f1 /app/config/date_range.txt | tr -d '\r\n ')

echo "Running initial scrape for first date: $FIRST_DATE"

python /app/src/scraper/presentation/cli.py scrape-for-day "$FIRST_DATE"

cron

tail -f /var/log/cron.log
