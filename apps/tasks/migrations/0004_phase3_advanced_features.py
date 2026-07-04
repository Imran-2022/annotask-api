# Generated migration for Phase 3 advanced annotation features
# This migration adds all the new models required for collaborative medical image annotation

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0003_annotation_upload'),
    ]

    operations = [
        # Create AnnotationProject model
        migrations.CreateModel(
            name='AnnotationProject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(
                    choices=[
                        ('active', 'Active'),
                        ('paused', 'Paused'),
                        ('completed', 'Completed'),
                        ('archived', 'Archived'),
                    ],
                    default='active',
                    max_length=20
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_locked', models.BooleanField(default=False)),
                ('collaborators', models.ManyToManyField(
                    blank=True,
                    related_name='collaborating_projects',
                    to=settings.AUTH_USER_MODEL
                )),
                ('locked_by', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='locked_projects',
                    to=settings.AUTH_USER_MODEL
                )),
                ('owner', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='owned_projects',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'ordering': ['-updated_at'],
            },
        ),

        # Create AnnotationLayer model
        migrations.CreateModel(
            name='AnnotationLayer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='layers',
                    to='tasks.annotationproject'
                )),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('project', 'name')},
            },
        ),

        # Update Annotation model options and add new fields
        migrations.AlterModelOptions(
            name='annotation',
            options={'ordering': ['-created_at']},
        ),

        migrations.RemoveField(
            model_name='annotation',
            name='user',
        ),

        migrations.AddField(
            model_name='Annotation',
            name='project',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='annotations',
                to='tasks.annotationproject'
            ),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='creator',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='created_annotations',
                to=settings.AUTH_USER_MODEL
            ),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='image_metadata',
            field=models.JSONField(default=dict, help_text='DICOM or image metadata'),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='shape_type',
            field=models.CharField(
                choices=[
                    ('polygon', 'Polygon'),
                    ('circle', 'Circle'),
                    ('rectangle', 'Rectangle'),
                    ('line', 'Line'),
                    ('freehand', 'Freehand'),
                    ('point', 'Point'),
                ],
                default='polygon',
                max_length=20
            ),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='shape_data',
            field=models.JSONField(default=dict, help_text='Stores points, dimensions, etc.'),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='label_class',
            field=models.CharField(
                choices=[
                    ('tumor', 'Tumor'),
                    ('healthy', 'Healthy Tissue'),
                    ('artifact', 'Artifact'),
                    ('other', 'Other'),
                ],
                default='other',
                max_length=50
            ),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='color',
            field=models.CharField(default='#10b981', max_length=7),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='opacity',
            field=models.FloatField(default=0.5),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='stroke_width',
            field=models.FloatField(default=2),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='locked_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='locked_annotations',
                to=settings.AUTH_USER_MODEL
            ),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='review_status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending Review'),
                    ('approved', 'Approved'),
                    ('rejected', 'Rejected'),
                    ('flagged', 'Flagged for Review'),
                ],
                default='pending',
                max_length=20
            ),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='reviewed_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='reviewed_annotations',
                to=settings.AUTH_USER_MODEL
            ),
        ),

        migrations.AddField(
            model_name='Annotation',
            name='last_edited_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='last_edited_annotations',
                to=settings.AUTH_USER_MODEL
            ),
        ),

        migrations.RenameField(
            model_name='Annotation',
            old_name='annotation_data',
            new_name='_legacy_annotation_data',
        ),

        # Create AnnotationComment model
        migrations.CreateModel(
            name='AnnotationComment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('annotation', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='comments',
                    to='tasks.annotation'
                )),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={'ordering': ['created_at']},
        ),

        # Create AnnotationHistory model
        migrations.CreateModel(
            name='AnnotationHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(
                    choices=[
                        ('created', 'Created'),
                        ('modified', 'Modified'),
                        ('deleted', 'Deleted'),
                        ('reviewed', 'Reviewed'),
                        ('locked', 'Locked'),
                        ('unlocked', 'Unlocked'),
                    ],
                    max_length=20
                )),
                ('previous_state', models.JSONField(blank=True, null=True, help_text='Previous annotation state')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('annotation', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='history',
                    to='tasks.annotation'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={'ordering': ['-timestamp']},
        ),

        # Create UserPresence model
        migrations.CreateModel(
            name='UserPresence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('project', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='active_users',
                    to='tasks.annotationproject'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={'unique_together': {('project', 'user')}},
        ),

        # Add indexes
        migrations.AddIndex(
            model_name='AnnotationProject',
            index=models.Index(fields=['owner', 'status'], name='tasks_annot_owner_i_idx'),
        ),

        migrations.AddIndex(
            model_name='AnnotationProject',
            index=models.Index(fields=['created_at'], name='tasks_annot_created_idx'),
        ),

        migrations.AddIndex(
            model_name='Annotation',
            index=models.Index(fields=['project', 'creator'], name='tasks_annot_proj_c_idx'),
        ),

        migrations.AddIndex(
            model_name='Annotation',
            index=models.Index(fields=['review_status'], name='tasks_annot_review_idx'),
        ),

        migrations.AddIndex(
            model_name='AnnotationHistory',
            index=models.Index(fields=['annotation', 'timestamp'], name='tasks_hist_annot_t_idx'),
        ),

        migrations.AddIndex(
            model_name='UserPresence',
            index=models.Index(fields=['project', 'is_active'], name='tasks_pres_proj_a_idx'),
        ),
    ]
