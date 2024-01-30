#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Add code to run commands from the 'commands' folder here
    #commands_folder = 'mysite/polls/management/commands'
    #for filename in os.listdir(commands_folder):
        #if filename.endswith('.py') and not filename.startswith('__'):
            #script_path = os.path.join(commands_folder, filename)
            #subprocess.Popen(['python', 'manage.py', script_path], cwd=os.path.dirname(__file__))

    # Run the Django server
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
