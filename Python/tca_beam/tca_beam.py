import os
import sys
from pathlib import Path
from collections import namedtuple
from jinja2 import Environment, FileSystemLoader
import click
from trogon import tui

beam_version = "(beam is not packaged so no version)"

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

TemplateRender = namedtuple('TemplateRender', ['render_file', 'template', 'target_dir'],
                            defaults=['', '', '.'])


def dbg(string):
    pass
    # print(string)


def p(string = ""):
    print(string)


def error(string):
    print(string)


def make_abs_path(rel_path):
    script_dir = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(script_dir, rel_path))


def render_templates(templateRenders, substitutions, step_name, feature_name, two_files, dry_run, force_overwrite):

    console_prefix = "- (DRY RUN:) " if dry_run else "- "

    dbg(f"-------- render_templates: templateRenders = {templateRenders}")
    dbg(f"-------- render_templates: substitutions = {substitutions}")

    p(f"{console_prefix}{step_name}")

    for templateRender in templateRenders:

        stub_contents = templateRender.template.render(substitutions)

        # Open the file for writing
        filename2 = templateRender.render_file

        directory = Path(templateRender.target_dir)

        filepath = directory / filename2

        p(f"{console_prefix}   Creating file {filepath}")

        if not dry_run:
            if os.path.isdir(filepath):
                error(f'A directory named "{filepath}" already exists, refusing to overwrite.')
                error()
                sys.exit(1)

            if not force_overwrite and os.path.isfile(filepath):
                error(f'A file named "{filepath}" already exists, refusing to overwrite. Use --force-overwrite to suppress this error.')
                error()
                sys.exit(1)

            directory.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w') as f:
                f.write(stub_contents)


def process_template(env, two_files, sub_dirs, force_overwrite, dry_run, feature_name):
    dbg(f"start process_template, sub_dirs = {sub_dirs}")

    substitutions = {
        'viewName': f"{feature_name}View",
        'featureName': f"{feature_name}ViewFeature"
    }

    # Load the template
    view_template = env.get_template('View.swift')
    view_feature_template = env.get_template('ViewFeature.swift')

    view_content = view_template.render(substitutions)
    view_feature_content = view_feature_template.render(substitutions)

    substitutions['reducerContent'] = view_feature_content
    substitutions['viewContent'] = view_content

    template_renders = []

    target_dir = f"{feature_name}Feature" if sub_dirs else "."

    dbg(f"just made target_dir: {target_dir}, and sub_dirs == {sub_dirs}")
    if two_files:
        template_renders.append(TemplateRender(f"{feature_name}ViewFeature.swift", env.get_template('TwoFile_ReducerPart.swift'), target_dir))
        template_renders.append(TemplateRender(f"{feature_name}View.swift", env.get_template('TwoFile_ViewPart.swift'), target_dir))
    else:
        # for reducer + view in one file, we append just 'View' to feature name
        template_renders.append(TemplateRender(f"{feature_name}View.swift", env.get_template('OneFile.swift'), target_dir))

    step_name = f"Feature '{feature_name}':"
    render_templates(template_renders, substitutions, step_name, feature_name, two_files, dry_run, force_overwrite)


def generate_all_preview(env, feature_names, script_dir, two_files, sub_dirs, preview_all, force_overwrite, dry_run, feature_name):

    # a single View that has a preview for all the Views
    all_previews_substitutions = []

    for feature_name in feature_names:
        all_previews_substitutions.append({
            'viewName': f"{feature_name}View",
            'featureName': f"{feature_name}ViewFeature"
        })

    substitutions_all_previews = { 'allFeatures': all_previews_substitutions}

    template_render = TemplateRender(f"AllPreviews.swift", env.get_template('AllPreviews.swift'))

    render_templates([template_render], substitutions_all_previews, 'Preview for all features:', feature_name, two_files, dry_run, force_overwrite)


def run(env, script_dir, two_files, sub_dirs, preview_all, force_overwrite, dry_run, feature_names):
    for feature_name in feature_names:
        process_template(env, two_files, sub_dirs, force_overwrite, dry_run, feature_name)

    if preview_all:
        generate_all_preview(env, feature_names, script_dir, two_files, sub_dirs, preview_all, force_overwrite, dry_run, feature_name)

    p()
    p("Done")
    p()

@tui()
@click.group(invoke_without_command=True)
# @click.group()
@click.option('--two-files', is_flag=True, help="Put view and reducer into separate files")
@click.option('--sub-dirs', is_flag=True, help="Put each feature in a sub-directory")
@click.option('--preview-all', is_flag=True, help="Generate a single View that previews all feature Views")
@click.option('--force-overwrite', is_flag=True, help="Force overwriting any existing files")
@click.option('--dry-run', is_flag=True, help="Don't generate files, just preview any actions")
@click.option('--version', is_flag=True, help="Print version and exit")
@click.argument('feature_names', nargs=-1)
# @click.command(no_args_is_help=True)
# @click.pass_context
def start(two_files, sub_dirs, preview_all, force_overwrite, dry_run, version, feature_names):

    if version:
        p(beam_version)
        sys.exit(0)

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

    script_dir = os.path.abspath(os.path.dirname(__file__))

    templates_path = make_abs_path('templates')
    file_loader = FileSystemLoader(templates_path)
    env = Environment(loader=file_loader)

    run(env, script_dir, two_files, sub_dirs, preview_all, force_overwrite, dry_run, feature_names)


if __name__ == '__main__':
    start()
