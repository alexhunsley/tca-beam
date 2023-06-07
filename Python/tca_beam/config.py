from dataclasses import dataclass
from jinja2 import Environment

@dataclass
class BeamConfig:
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
