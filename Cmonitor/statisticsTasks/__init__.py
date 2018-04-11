import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/subtasks')
os.environ.update({"DJANGO_SETTINGS_MODULE": "indexStatistics.settings"})