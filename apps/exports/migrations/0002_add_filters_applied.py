# Generated manually to fix missing filters_applied column
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('exports', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            ALTER TABLE export_logs 
            ADD COLUMN IF NOT EXISTS filters_applied JSONB NOT NULL DEFAULT '{}'::jsonb;
            """,
            reverse_sql="""
            ALTER TABLE export_logs 
            DROP COLUMN IF EXISTS filters_applied;
            """,
        ),
    ]

