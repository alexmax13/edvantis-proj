#!/bin/bash
cd /home/san/Desktop/project_ed/fuel_proj
. env/bin/activate
python cron_task.py &>> log.txt
date > last_cron.txt