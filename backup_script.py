# backup_script.py (run in PythonAnywhere console)
import os
from datetime import datetime

# Backup database
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
os.system(f'mysqldump -u yourusername -p yourusername$tazuddin > backup_{timestamp}.sql')