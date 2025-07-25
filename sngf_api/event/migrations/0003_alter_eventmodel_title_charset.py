from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_alter_eventmodel_title'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE event_eventmodel
                MODIFY title TEXT
                CHARACTER SET utf8mb4
                COLLATE utf8mb4_unicode_ci;
            """,
            reverse_sql="""
                ALTER TABLE event_eventmodel
                MODIFY title TEXT
                CHARACTER SET utf8
                COLLATE utf8_general_ci;
            """
        ),
    ]
