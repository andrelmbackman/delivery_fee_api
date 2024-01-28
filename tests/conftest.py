import os
import sys


"""Configuration file to help pytest find the app module."""


API_ENDPOINT = "/delivery_fee"

current_directory = os.path.dirname(os.path.abspath(__file__))

root_directory = os.path.dirname(current_directory)

sys.path.append(root_directory)
