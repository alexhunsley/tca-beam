from jinja2 import Environment, FileSystemLoader
import click
from .config import BeamConfig, PermanentSettings
from .run import run
from .settings import *

beam_version = "(no version because beam is not packaged)"

try:
    from tca_beam import __version__
    beam_version = __version__
except ImportError:
    pass

# TODO:
# [x] try trogon/textualize on tca-beam -- see results in my main TW -- might have to make explicit tca-beam 'make' command
# -[x] upload to main pyPi
# -[ ] make bbtests
# -[x] option for preview-all
# -[x] impl two files
# -[x] flags for 'features in sub_dirs'
# -[x] make script use abs path to the templates, no chdir!
# -[x] --dry-run

# For docs:
#  tca-beam won't complain if the output_dir already exists, regardless of force_overwrite flag (which only applies to files).
#

# When you're testing and playing with beam, it might be tempting to set up a host xcode project with a _link_ to a folder
# where you are generating the files with beam.
# However, Xcode however won't add these files to any target (it's how linked folders work), so you're probably better off
# just adding a folder group to your project (in the usual way) after you've generated the files with beam.


@click.command(no_args_is_help=True)
@click.option('--two-files', is_flag=True, help="Put view and reducer into separate files")
@click.option('--sub-dirs', is_flag=True, help="Put each feature in a sub-directory")
@click.option('--preview-all', is_flag=True, help="Generate a single View that previews all feature Views")
@click.option('--output-dir', default='.', help="Output directory (defaults to current dir)")
@click.option('--force-overwrite', is_flag=True, help="Force overwriting any existing files")
@click.option('--dry-run', is_flag=True, help="Don't generate files, just preview any actions")
@click.option('--customise-settings', is_flag=True, help="Generate a user-editable file to tweak file naming settings.")
@click.option('--version', is_flag=True, help="Print version and exit")
@click.argument('feature_names', nargs=-1)
def start(two_files, sub_dirs, preview_all, output_dir, force_overwrite, dry_run, customise_settings, version, feature_names):

    if customise_settings:
        personalize_permanent_settings()
        sys.exit(0)

    permanent_settings = load_permanent_settings()
    dbg(f"Settings: {permanent_settings}")

    if version:
        p(beam_version)
        sys.exit(0)

    script_dir = os.path.abspath(os.path.dirname(__file__))

    templates_path = make_abs_path('templates')
    file_loader = FileSystemLoader(templates_path)
    jinja_env = Environment(loader=file_loader)

    config = BeamConfig(PermanentSettings(permanent_settings), script_dir, output_dir, jinja_env, two_files, sub_dirs, preview_all,
                        output_dir, force_overwrite, dry_run, feature_names)

    if len(feature_names) < 1:
        p()
        p("Please give one or more feature name arguments (after any option flags).")
        p()

        echo = click.echo
        echo(start.get_help(click.get_current_context()))
        sys.exit(1)

    p("")
    p("tca-beam is preparing two-by-fours...")
    p("")

    # if dry_run:
    #     p("In DRY-RUN mode. No files or folders will be created.")
    #     p("")

    # the output_dir is relative to the user's current dir, NOT the script!

    run(config)


if __name__ == '__main__':
    start()
