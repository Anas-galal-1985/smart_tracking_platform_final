from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0001_initial'),  # تأكد من اسم آخر مايجريشن صحيح
    ]

    operations = [
        migrations.AddField(
            model_name='videostream',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 1, 1)),
            preserve_default=False,
        ),
    ]
