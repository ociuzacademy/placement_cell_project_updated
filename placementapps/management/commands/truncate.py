from django.core.management.base import BaseCommand
from django.db import connection, transaction

class Command(BaseCommand):
    help = 'Truncates student and all related placement application/notification tables'

    def handle(self, *args, **options):
        # List of all target tables exactly as they are named in MySQL
        tables_to_truncate = [
            'placementapps_tbl_student',
            'placementapps_jobapplication',
            'placementapps_sessionapplication',
            'placementapps_studentnotification',
            'placementapps_tutornotification',
            'placementapps_airesumescreening',
            'placementapps_tbl_admin',
            'placementapps_tbl_department'
            'placementapps_Job',
            'placementapps_TrainingSession',
            'placementapps_Course',
            'placementapps_tbl_tutor'
        ]
        
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    # 1. Disable foreign key checks for MySQL
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
                    
                    # 2. Loop through and truncate each table
                    for table in tables_to_truncate:
                        self.stdout.write(self.style.WARNING(f'Truncating {table}...'))
                        cursor.execute(f"TRUNCATE TABLE {table};")
                    
                    # 3. Re-enable foreign key checks
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
                        
            self.stdout.write(self.style.SUCCESS('Successfully truncated all requested tables.'))
            
        except Exception as e:
            # Safe backup: ensure constraints are turned back on even if it fails mid-execution
            with connection.cursor() as cursor:
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            self.stderr.write(self.style.ERROR(f'Error truncating tables: {e}'))

#Run python manage.py truncate to truncate the tables