from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("marketplace_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="marketplaceoffer",
            old_name="creator",
            new_name="user",
        ),
    ]
