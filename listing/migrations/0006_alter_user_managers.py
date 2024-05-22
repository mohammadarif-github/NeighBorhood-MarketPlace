
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0005_alter_user_managers'),  # Ensure this matches your latest migration
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, null=True),
        ),
    ]
