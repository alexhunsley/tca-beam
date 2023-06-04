import os
from jinja2 import Environment, FileSystemLoader
import click
import sys

def process_template(script_dir, two_files, force_overwrite, feature_name):

    os.chdir(script_dir)

    # Define the template directory
    file_loader = FileSystemLoader('templates')

    # Create the environment
    env = Environment(loader=file_loader)

    # Prepare the substitutions
    substitutions = {
        'viewName': f"{feature_name}View",
        'featureName': f"{feature_name}ViewFeature"
    }

    # Load the template
    view_template = env.get_template('View.swift')
    view_feature_template = env.get_template('ViewFeature.swift')

    one_file_template = env.get_template('OneFile.swift')

    view_content = view_template.render(substitutions)
    view_feature_content = view_feature_template.render(substitutions)

    main_file_substitutions = {
        'reducerContent': view_feature_content,
        'viewContent': view_content
    }

    # Render the template with the substitutions
    stub_contents = one_file_template.render(main_file_substitutions)

    # When saving to disk, make the single file one end with View, not ViewFeature!
    # print(output)

    # Open the file for writing
    filename = f"{feature_name}View.swift"
    print(f"Creating stub for {feature_name}")

    if os.path.isdir(filename):
        print(f'Output destination "{filename}" already exists and is a directory, refusing to overwrite.')
        print()
        sys.exit()

    if not force_overwrite and os.path.isfile(filename):
        print(f'Output destination "{filename}" already exists, refusing to overwrite. Use --force-overwrite to ignore existing files.')
        print()
        sys.exit()

    with open(filename, 'w') as f:
        f.write(stub_contents)

    # output = view_feature_template.render(substitutions)
    # print(output)

@click.command(no_args_is_help=True)
@click.option('--two-files', is_flag=True, help='Put view and reducer into separate files (UNIMPLEMENTED)')
@click.option('--force-overwrite', is_flag=True, help='Force overwriting any existing files')
@click.argument('feature_names', nargs=-1)
def start(two_files, force_overwrite, feature_names):
    # print(f"Args: {feature_names}")

    if len(feature_names) < 1:
        print()
        print("This command must be given one or more feature name arguments (after any option flags).")
        print()

        echo = click.echo
        echo(start.get_help(click.get_current_context()))
        sys.exit(1)

    script_dir = os.path.abspath(os.path.dirname(__file__))

    for feature_name in feature_names:
        process_template(script_dir, two_files, force_overwrite, feature_name)

    print()
    print("Done")
    print()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
