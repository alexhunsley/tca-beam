from jinja2 import Environment, FileSystemLoader
import click
from .config import BeamConfig, PermanentSettings
from .run import run
from .settings import *
from .text_tree_parser import *
import os

beam_version = "(no version because beam is not packaged)"

try:
    from tca_beam import __version__
    beam_version = __version__
except ImportError:
    pass

# TODO:
# -[ ] add --suppress-views (implies two-files style but only makes the reducers)
# -[ ] make bbtests
# -[x] try trogon/textualize on tca-beam -- see results in my main TW -- might have to make explicit tca-beam 'make' command
# -[x] upload to main pyPi
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



def start_test_tree():

    # hacky PoC: we just drive the start function, for now

    root_nodes = []
    non_leaf_nodes = []

    # root_leaf_func = lambda feature_name: create_simple_reducer(feature_name)
    # non_leaf_func = lambda feature_names: create_hor_reducer(feature_names)

    root_leaf_func = lambda feature_name: root_nodes.append(feature_name)
    # non_leaf_func = lambda feature_names: non_leaf_nodes.extend(feature_names)
    non_leaf_func = lambda feature_names: non_leaf_nodes.append(feature_names)


    process_nodes_from_file("tca_beam/tree.txt", root_leaf_func, non_leaf_func)


    for feature_name in root_nodes:
        create_simple_reducer(feature_name)

    # We need to fix the data to prevent our HOR data -> file generation
    # from clobbering HOR reducers with simple non-HOR versions of the
    # same file when it appears in a value list! We only want to process
    # the key version of these HOR reducers when they appear in both places.
    #
    # NO this doesn't work! the HOR reducer still needs to know the name of the sub-reducers
    # it reference, even if it won't actually create the files.
    #
    # Ok, prepend a name with '-' to mean "This is sub-reducer, just don't create the actual file,
    # only the refs in the HOR to it"
    # non_leaf_nodes = remove_matching_elements(non_leaf_nodes)
    non_leaf_nodes = prepend_matching_elements(non_leaf_nodes)

    for parent_child_names_tuple in non_leaf_nodes:
        create_hor_reducer(parent_child_names_tuple)


@click.command(no_args_is_help=True)
@click.option('--two-files', is_flag=True, help="Put view and reducer into separate files")
@click.option('--sub-dirs', is_flag=True, help="Put each feature in a sub-directory")
@click.option('--preview-all', is_flag=True, help="Generate a single View that previews all feature Views")
@click.option('--make-hor', is_flag=True, help="Make first feature name a higher order reducer that scopes in the remaining ones as sub-reducers")
@click.option('--output-dir', default='.', help="Output directory (defaults to current dir)")
@click.option('--force-overwrite', is_flag=True, help="Force overwriting any existing files")
@click.option('--dry-run', is_flag=True, help="Don't generate files, just preview any actions")
@click.option('--customise-settings', is_flag=True, help="Generate a user-editable file to tweak file naming settings.")
@click.option('--version', is_flag=True, help="Print version and exit")
@click.argument('feature_names', nargs=-1)
def start(two_files, sub_dirs, preview_all, make_hor, output_dir, force_overwrite, dry_run, customise_settings, version, feature_names):

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
                        make_hor, output_dir, force_overwrite, dry_run, feature_names)

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


def create_simple_reducer(reducer_name):

    dbg(f"------------------------ create_simple_reducer, red name = {reducer_name}")

    ctx = click.Context(start)
    ctx.invoke(start,
               two_files=False,
               sub_dirs=False,
               preview_all=False,
               make_hor=False,
               output_dir='../XcodeTestProject/XcodeTestProject/TCA-beam-content',
               force_overwrite=True,
               dry_run=False,
               customise_settings=False,
               version=False,
               feature_names=[reducer_name]
       )


# # Example usage:
# data = [('apple', ['banana', 'apple', 'cherry']), ('banana', ['apple', 'banana', 'cherry'])]
# print(prepend_matching_elements(data))
#  --> [('apple', ['-banana', '-apple', 'cherry']), ('banana', ['-apple', '-banana', 'cherry'])]
def prepend_matching_elements(data):
    keys = [t[0] for t in data]
    return [(key, [('_' + val) if val in keys else val for val in values]) for key, values in data]


def create_hor_reducer(reducer_names):

    dbg(f"------------------------ create_hor_reducer, red names = {reducer_names}")

    # convert (str, [str]) to just a flat [str]
    reducer_names = [reducer_names[0]] + reducer_names[1]

    dbg(f"create_hor_reducer 2, red names = {reducer_names}")

    dry = False

    ctx = click.Context(start)
    ctx.invoke(start,
               two_files=False,
               sub_dirs=False,
               preview_all=False,
               make_hor=True,
               output_dir='../XcodeTestProject/XcodeTestProject/TCA-beam-content',
               force_overwrite=True,
               dry_run=dry,
               customise_settings=False,
               version=False,
               feature_names=reducer_names
       )


if __name__ == '__main__':
    start_test_tree()
    # start()
