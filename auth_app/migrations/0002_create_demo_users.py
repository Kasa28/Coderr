from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


DEMO_PASSWORD = "GuestPassword123!"


def create_demo_users(apps, schema_editor):
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    Profile = apps.get_model("profile_app", "Profile")

    demo_users = [
        ("guest_customer", "customer"),
        ("guest_business", "business"),
    ]

    for username, user_type in demo_users:
        user, _ = User.objects.get_or_create(
            username=username,
            defaults={
                "email": f"{username}@example.com",
                "type": user_type,
            },
        )
        user.type = user_type
        user.password = make_password(DEMO_PASSWORD)
        user.save()
        Profile.objects.get_or_create(user=user)


class Migration(migrations.Migration):
    dependencies = [
        ("auth_app", "0001_initial"),
        ("profile_app", "0002_alter_profile_location_alter_profile_tel_and_more"),
    ]

    operations = [
        migrations.RunPython(create_demo_users, migrations.RunPython.noop),
    ]
