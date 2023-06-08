from .template_rendering import *


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
        # could do replacement inside TemplateRender? Or make method helper in this file, more likely
        reducer_filename = config.permanent_settings.two_files_reducer_part_filename.replace("{{featureName}}", feature_name)
        dbg(f"Made RF: {reducer_filename}")
        template_renders.append(TemplateRender(reducer_filename,
                                               config.jinja_env.get_template('TwoFile_ReducerPart.swift'),
                                               target_dir))

        view_filename = config.permanent_settings.two_files_view_part_filename.replace("{{featureName}}", feature_name)
        dbg(f"Made VF: {view_filename}")
        template_renders.append(TemplateRender(view_filename,
                                               config.jinja_env.get_template('TwoFile_ViewPart.swift'),
                                               target_dir))
    else:
        one_file_filename = config.permanent_settings.one_file_filename.replace("{{featureName}}", feature_name)
        dbg(f"Made OFF: {one_file_filename}")
        # for reducer + view in one file, we append just 'View' to feature name
        template_renders.append(TemplateRender(one_file_filename,
                                               config.jinja_env.get_template('OneFile.swift'),
                                               target_dir))

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

    preview_all_filename = config.permanent_settings.preview_all_filename.replace("{{featureName}}", feature_name)

    template_render = TemplateRender(preview_all_filename,
                                     config.jinja_env.get_template('AllPreviews.swift'))

    render_templates(config, [template_render], substitutions_all_previews, 'Preview for all features:')


def run(config):
    for feature_name in config.feature_names:
        process_template(config, feature_name)

    if config.preview_all:
        generate_all_preview(config)

    p()
    p("Done")
    p()
