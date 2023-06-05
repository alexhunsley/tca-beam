import os
from collections import namedtuple
from jinja2 import Environment, FileSystemLoader
import click
import sys
from pathlib import Path

# TODO:
# -[ ] impl two files
# -[ ] flags for 'features in subdirs'
# -[ ] bump, upload to real pyPi
# -[ ] make bbtest for it
# -[x] make script use abs path to the templates, no chdir!
# -[x] --dry-run
# -[ ] optional allPreviews view
TemplateRender = namedtuple('TemplateRender', ['render_file', 'template', 'substitutions', 'target_dir'],
                            defaults=['', '', '', '.'])


def dbg(string):
    pass
    # print(string)


def make_abs_path(rel_path):
    script_dir = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(script_dir, rel_path))


def render_templates(templateRenders, substitutions, feature_name, two_files, dry_run, force_overwrite):

    console_prefix = "- (DRY RUN:) " if dry_run else "- "

    dbg(f"templateRenders = {templateRenders}")

    print(f"{console_prefix}Feature '{feature_name}':")

    for templateRender in templateRenders:
        # Render the template with the substitutions
        stub_contents = templateRender.template.render(substitutions)

        # When saving to disk, make the single file one end with View, not ViewFeature!
        # print(output)

        #TODO dry_run check before here!

        # Open the file for writing
        filename2 = templateRender.render_file

        directory = Path(templateRender.target_dir)

        filepath = directory / filename2

        # filepath = os.path.join(f"{feature_name}Feature", filename2) if sub_dirs else filename2
        # filepath = os.path.join(templateRender.target_dir, filename2)

        print(f"{console_prefix}   Creating file {filepath}")

        if not dry_run:
            if os.path.isdir(filepath):
                print(f'A directory named "{filepath}" already exists, refusing to overwrite.')
                print()
                sys.exit(1)

            if not force_overwrite and os.path.isfile(filepath):
                print(f'A file named "{filepath}" already exists, refusing to overwrite. Use --force-overwrite to suppress this error.')
                print()
                sys.exit(1)

            # Create the directories if they don't exist
            directory.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w') as f:
                f.write(stub_contents)


def process_template(env, script_dir, two_files, sub_dirs, preview_all, force_overwrite, dry_run, feature_name):
    dbg(f"start process_template, sub_dirs = {sub_dirs}")

    # Prepare the substitutions
    substitutions = {
        'viewName': f"{feature_name}View",
        'featureName': f"{feature_name}ViewFeature"
    }

    # Load the template
    view_template = env.get_template('View.swift')
    view_feature_template = env.get_template('ViewFeature.swift')

    view_content = view_template.render(substitutions)
    view_feature_content = view_feature_template.render(substitutions)

    template_renders = []

    target_dir = f"{feature_name}Feature" if sub_dirs else "."

    dbg(f"just made target_dir: {target_dir}, and sub_dirs == {sub_dirs}")
    if two_files:
        # f"{feature_name}View.swift"

        template_renders.append(TemplateRender(f"{feature_name}ViewFeature.swift", env.get_template('TwoFile_ReducerPart.swift'), substitutions, target_dir))
        template_renders.append(TemplateRender(f"{feature_name}View.swift", env.get_template('TwoFile_ViewPart.swift'), substitutions, target_dir))
    else:
        # for reducer + view in one file, we append just 'View' to feature name
        template_renders.append(TemplateRender(f"{feature_name}View.swift", env.get_template('OneFile.swift'), substitutions, target_dir))

    substitutions = {
        'reducerContent': view_feature_content,
        'viewContent': view_content
    }

    render_templates(template_renders, substitutions, feature_name, two_files, dry_run, force_overwrite)


def generate_all_previews(env, feature_names, script_dir, two_files, sub_dirs, preview_all, force_overwrite, dry_run, feature_name):

    # a single View that has a preview for all the Views
    all_previews_substitutions = []

    for feature_name in feature_names:
        all_previews_substitutions.append({
            'viewName': f"{feature_name}View",
            'featureName': f"{feature_name}ViewFeature"
        })

    substitions = { 'allFeatures': all_previews_substitutions}

    template_render = TemplateRender(f"AllPreviews.swift", env.get_template('AllPreviews.swift'), []) # all_previews_substitutions) // TODO is this subs actually needed here>
        # ['render_file', 'template', 'substitutions', 'target_dir'],

    # template_renders.append(TemplateRender(f"AllPreviewsView.swift", env.get_template('AllPreviews.swift'), all_previews_substitutions))
    render_templates([template_render], substitions, feature_name, two_files, dry_run, force_overwrite)


@click.command(no_args_is_help=True)
@click.option('--two-files', is_flag=True, help="Put view and reducer into separate files.")
@click.option('--sub-dirs', is_flag=True, help="Put each feature in a sub-directory")
@click.option('--preview-all', is_flag=True, help="Generate a single View that previews all feature Views")
@click.option('--force-overwrite', is_flag=True, help="Force overwriting any existing files.")
@click.option('--dry-run', is_flag=True, help="Don't generate files, just preview any actions")
@click.argument('feature_names', nargs=-1)
def start(two_files, sub_dirs, preview_all, force_overwrite, dry_run, feature_names):

    if len(feature_names) < 1:
        print()
        print("This command must be given one or more feature name arguments (after any option flags).")
        print()

        echo = click.echo
        echo(start.get_help(click.get_current_context()))
        sys.exit(1)

    script_dir = os.path.abspath(os.path.dirname(__file__))

    templates_path = make_abs_path('templates')
    file_loader = FileSystemLoader(templates_path)
    env = Environment(loader=file_loader)

    for feature_name in feature_names:
        process_template(env, script_dir, two_files, sub_dirs, preview_all, force_overwrite, dry_run, feature_name)

    if preview_all:
        generate_all_previews(env, feature_names, script_dir, two_files, sub_dirs, preview_all, force_overwrite, dry_run, feature_name)

    print()
    print("Done")
    print()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
