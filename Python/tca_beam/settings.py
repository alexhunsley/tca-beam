import sys
import shutil
from configparser import ConfigParser
from pathlib import Path
from typing import Optional
from .helpers import *

settings_filename = '.beam-settings.toml'
settings_user_copy_filename = settings_filename
settings_built_in_path = f"templates/{settings_filename}"


def personalize_permanent_settings(force=False):
    """
    Copies the default settings file to the user's home directory.
    """
    # location of the default settings file
    default_settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), settings_built_in_path)

    # destination for the copied settings file in the user's home directory
    home = str(Path.home())
    destination_settings_path = os.path.join(home, settings_filename)

    if not force and os.path.exists(destination_settings_path):
        p()
        p(f"A settings file already exists at {destination_settings_path}.")
        p("If you want to generate the settings file again from defaults, please delete that existing file first.")
        p()
        sys.exit(1)

    # Copy the settings file
    shutil.copyfile(default_settings_path, destination_settings_path)

    p()
    p(f"I've copied default settings to '{destination_settings_path}'.")
    p(f"Please edit this file with your favourite text editor.")
    p()
    p("Note that you can later delete this file to go back to the defaults.")
    p("")
    sys.exit(0)


def load_permanent_settings() -> Optional[ConfigParser]:
    """
    Loads the user's custom settings if they exist, otherwise loads the default settings.
    Returns a ConfigParser object, or None if no settings file is found.
    """
    # location of the settings files
    home = str(Path.home())
    user_settings_path = os.path.join(home, settings_user_copy_filename)
    default_settings_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), settings_built_in_path)

    dbg(f"got user_settings_path = {user_settings_path}")
    dbg(f"got default_settings_path = {default_settings_path}")

    configParser = ConfigParser()

    # If the user's custom settings exist, load them
    if os.path.exists(user_settings_path):
        configParser.read(user_settings_path)
    # ... or if the default settings exist, load them
    elif os.path.exists(default_settings_path):
        configParser.read(default_settings_path)
    else:
        return None

    return configParser
