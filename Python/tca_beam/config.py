import sys
from dataclasses import dataclass
from jinja2 import Environment
from .helpers import *


def print_settings_advice_and_exit():
    p("""            
    Please check the file ~/.beam-settings.toml for issues or corruption,
    and consider deleting it and running 'tca-beam --customise-settings'
    to generate the file again with the default values.
    
    """)

    sys.exit(1)


class PermanentSettings:

    def __init__(self, configParser):
        self.configParser = configParser
        self.two_files_view_part_filename = self.sanitized_setting('two_files_view_part_filename')
        self.two_files_reducer_part_filename = self.sanitized_setting('two_files_reducer_part_filename')
        self.one_file_filename = self.sanitized_setting('one_file_filename')
        self.preview_all_filename = self.sanitized_setting('preview_all_filename')
        self.feature_subdirs_dir_name = self.sanitized_setting('feature_subdirs_dir_name')


    def sanitized_setting(self, setting_name) -> str:
        section = "file_naming"

        setting_string = ""

        try:
            setting_string = self.configParser.get(section, setting_name)
        except Exception as e:
            error(f"Error reading setting '{setting_name}' from the settings file.\n")
            print_settings_advice_and_exit()

        if not setting_string or len(setting_string) <= 0:
            error("Couldn't find a key {setting_name} in the ")
            print_settings_advice_and_exit()

        # check for bungled string replacement in settings
        if ("{" in setting_string or "}" in setting_string) and "{{featureName}}" not in setting_string:
            p(f"""

ERROR: Found a user-customised settings string that seems to contain a corrupt tag:

    {setting_string}

The only valid tag you can use is '{{featureName}}'.
""")
            print_settings_advice_and_exit()

        dbg(f"Got sanitized settings: {setting_string}")

        return sanitize_filename(setting_string)


@dataclass
class BeamConfig:
    permanent_settings: PermanentSettings
    script_dir: str
    target_dir: str
    jinja_env: Environment
    two_files: bool
    sub_dirs: bool
    preview_all: bool
    output_dir: str
    force_overwrite: bool
    dry_run: bool
    feature_names: [str]
