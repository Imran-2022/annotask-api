from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='image_file',
            field=models.FileField(upload_to='annotations/', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='annotation_data',
            field=models.JSONField(blank=True, null=True, help_text='Stores annotation coordinates and metadata'),
        ),
    ]
