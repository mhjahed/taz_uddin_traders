# Create a backup script
# backup_db.py
import os
import datetime

def backup_database():
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backup_{timestamp}.sql'
    
    # For SQLite
    os.system(f'cp db.sqlite3 backups/{backup_file}')
    
    # For PostgreSQL
    # os.system(f'pg_dump your_db_name > backups/{backup_file}')
    
    print(f'Backup created: {backup_file}')

if __name__ == '__main__':
    backup_database()