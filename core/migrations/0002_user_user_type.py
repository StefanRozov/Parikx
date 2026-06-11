from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("client", "Клиент"),
                    ("master", "Мастер"),
                    ("admin", "Администратор"),
                ],
                default="client",
                max_length=10,
            ),
        ),
    ]
