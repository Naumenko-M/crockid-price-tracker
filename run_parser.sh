#!/bin/bash

cd /Users/mihail/Desktop/crockid-price-tracker

echo "========================================" >> logs/wb_cron.log
echo "Запуск парсера: $(date '+%d.%m.%Y %H:%M:%S')" >> logs/wb_cron.log

/Users/mihail/Desktop/crockid-price-tracker/.venv/bin/python src/parse_wb_test.py >> logs/wb_cron.log 2>&1

echo "Завершение парсера: $(date '+%d.%m.%Y %H:%M:%S')" >> logs/wb_cron.log
echo "Код завершения: $?" >> logs/wb_cron.log
echo "" >> logs/wb_cron.log

tail -28 logs/wb_cron.log