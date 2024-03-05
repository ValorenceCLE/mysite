from django.apps import AppConfig
from django.core.management import call_command



class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'  # Replace 'your_app_name' with the actual name of your app

    def ready(self):
        # Call the speedtest_command management command when the app is ready
        call_command('speedtest_command')
