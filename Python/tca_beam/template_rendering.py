from collections import namedtuple
from pathlib import Path
from .helpers import *

TemplateRender = namedtuple('TemplateRender', ['render_file', 'template', 'target_dir'],
                            defaults=['', '', '.'])


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
