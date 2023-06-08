import os
import sys

from pathlib import Path
from collections import namedtuple
from jinja2 import Environment, FileSystemLoader
import click

from .config import BeamConfig

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

# For docs:
#  tca-beam won't complain if the output_dir already exists, regardless of force_overwrite flag (which only applies to files).
#

TemplateRender = namedtuple('TemplateRender', ['render_file', 'template', 'target_dir'],
                            defaults=['', '', '.'])

def dbg(string):
    pass
    # print(string)


def p(string=""):
    print(string)


def error(string):
    print(string)


def make_abs_path(rel_path):
    script_dir = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(script_dir, rel_path))


def render_templates(config, templateRenders, substitutions, step_name):

    console_prefix = "- (DRY RUN:) " if config.dry_run else "- "

    dbg(f"-------- render_templates: templateRenders = {templateRenders}")
    dbg(f"-------- render_templates: substitutions = {substitutions}")

    p(f"{console_prefix}{step_name}")

    for templateRender in templateRenders:

        stub_contents = templateRender.template.render(substitutions)

        # Open the file for writing
        filename = templateRender.render_file

        structure_directory = Path(templateRender.target_dir)

        abs_directory = config.output_dir / structure_directory
        filepath = abs_directory / filename

        p(f"{console_prefix}   Creating file {filepath}")

        if not config.dry_run:
            if os.path.isdir(filepath):
                error(f'A directory named "{filepath}" already exists, refusing to overwrite.')
                error()
                sys.exit(1)

            if not config.force_overwrite and os.path.isfile(filepath):
                error(f'A file named "{filepath}" already exists, refusing to overwrite. Use --force-overwrite to suppress this error.')
                error()
                sys.exit(1)

            abs_directory.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'w') as f:
                f.write(stub_contents + '\n')


def process_template(config, feature_name):
    dbg(f"start process_template, config = {config}, sub_dirs = {config.sub_dirs}")

    substitutions = {
        'viewName': f"{feature_name}View",
        'featureName': f"{feature_name}ViewFeature"
    }

    # Load the template
    view_template = config.jinja_env.get_template('View.swift')
    view_feature_template = config.jinja_env.get_template('ViewFeature.swift')

    view_content = view_template.render(substitutions)
    view_feature_content = view_feature_template.render(substitutions)

    substitutions['reducerContent'] = view_feature_content
    substitutions['viewContent'] = view_content

    template_renders = []

    target_dir = f"{feature_name}Feature" if config.sub_dirs else "."

    dbg(f"just made target_dir: {config.target_dir}, and sub_dirs == {config.sub_dirs}")
    if config.two_files:
        template_renders.append(TemplateRender(f"{feature_name}ViewFeature.swift", config.jinja_env.get_template('TwoFile_ReducerPart.swift'), target_dir))
        template_renders.append(TemplateRender(f"{feature_name}View.swift", config.jinja_env.get_template('TwoFile_ViewPart.swift'), target_dir))
    else:
        # for reducer + view in one file, we append just 'View' to feature name
        template_renders.append(TemplateRender(f"{feature_name}View.swift", config.jinja_env.get_template('OneFile.swift'), target_dir))

    step_name = f"Feature '{feature_name}':"
    render_templates(config, template_renders, substitutions, step_name)


def generate_all_preview(config):

    # a single View that has a preview for all the Views
    all_previews_substitutions = []

    for feature_name in config.feature_names:
        all_previews_substitutions.append({
            'viewName': f"{feature_name}View",
            'featureName': f"{feature_name}ViewFeature"
        })

    substitutions_all_previews = { 'allFeatures': all_previews_substitutions}

    template_render = TemplateRender(f"AllPreviews.swift", config.jinja_env.get_template('AllPreviews.swift'))

    render_templates(config, [template_render], substitutions_all_previews, 'Preview for all features:')


def run(config):
    for feature_name in config.feature_names:
        process_template(config, feature_name)

    if config.preview_all:
        generate_all_preview(config)

    p()
    p("Done")
    p()


@click.command(no_args_is_help=True)
@click.option('--two-files', is_flag=True, help="Put view and reducer into separate files")
@click.option('--sub-dirs', is_flag=True, help="Put each feature in a sub-directory")
@click.option('--preview-all', is_flag=True, help="Generate a single View that previews all feature Views")
@click.option('--output-dir', default='.', help="Output directory (defaults to current dir)")
@click.option('--force-overwrite', is_flag=True, help="Force overwriting any existing files")
@click.option('--dry-run', is_flag=True, help="Don't generate files, just preview any actions")
@click.option('--version', is_flag=True, help="Print version and exit")
@click.argument('feature_names', nargs=-1)
def start(two_files, sub_dirs, preview_all, output_dir, force_overwrite, dry_run, version, feature_names):

    if version:
        p(beam_version)
        sys.exit(0)

    script_dir = os.path.abspath(os.path.dirname(__file__))

    templates_path = make_abs_path('templates')
    file_loader = FileSystemLoader(templates_path)
    jinja_env = Environment(loader=file_loader)

    config = BeamConfig(script_dir, output_dir, jinja_env, two_files, sub_dirs, preview_all, output_dir, force_overwrite, dry_run, feature_names)

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
