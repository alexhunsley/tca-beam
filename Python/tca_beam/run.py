from .template_rendering import *


def process_template(config, feature_name, substitutions, extra_text_for_step_display=""):
    dbg(f"start process_template, config = {config}, sub_dirs = {config.sub_dirs}, subs = {substitutions}")

    # Load the template
    view_template = config.jinja_env.get_template('View.swift')
    view_feature_template = config.jinja_env.get_template('ViewFeature.swift')

    view_content = view_template.render(substitutions)
    view_feature_content = view_feature_template.render(substitutions)

    substitutions['reducerContent'] = view_feature_content
    substitutions['viewContent'] = view_content

    template_renders = []

    target_dir = config.permanent_settings.feature_subdirs_dir_name.replace("{{featureName}}", feature_name) if config.sub_dirs else '.'

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

    step_name = f"Feature {extra_text_for_step_display}'{feature_name}':"
    render_templates(config, template_renders, substitutions, step_name)


def generate_all_preview(config):

    # a single View that has a preview for all the Views
    all_previews_substitutions = []

    # If making a HOR, we omit the first reducer in all previews --
    # probably don't want it previewed
    feature_names = config.feature_names[1:] if config.make_hor else config.feature_names

    for feature_name in feature_names:
        all_previews_substitutions.append({
            'viewName': f"{feature_name}View",
            'featureName': f"{feature_name}ViewFeature"
        })

    substitutions_all_previews = { 'allFeatures': all_previews_substitutions}

    preview_all_filename = config.permanent_settings.preview_all_filename.replace("{{featureName}}", feature_name)

    template_render = TemplateRender(preview_all_filename,
                                     config.jinja_env.get_template('AllPreviews.swift'))

    render_templates(config, [template_render], substitutions_all_previews, 'Preview for all features:')


# CapitalNameStyleString -> capitalNameStyleString
def to_camel_case(string):
    return string[0].lower() + string[1:]


def make_sub_reducer_substitions(config):

    substitutions = {}

    for feature_name in [fName.replace('_', '') for fName in config.feature_names[1:]]:

        feature_name_as_var = to_camel_case(feature_name)

        substitutions.update(
            {
                feature_name:
                    {
                        # make 'varName' more specific! e.g. featureVarNameInHOR
                        'varName': f"{feature_name_as_var}",
                        'featureName': f"{feature_name}ViewFeature"
                    }
            }
        )

    return substitutions


def run(config):

    sub_reducer_feature_substitutions = make_sub_reducer_substitions(config) if config.make_hor else {}

    for index, feature_name in enumerate(config.feature_names):

        if feature_name[0] == '_':
            continue

        substitutions = {
            'viewName': f"{feature_name}View",
            'featureName': f"{feature_name}ViewFeature",
        }

        # main reducer in HOR mode has extra gubbins
        if index == 0:
            substitutions.update(
                {
                    'subReducerFeatures': sub_reducer_feature_substitutions
                }
            )

        process_template(config,
                         feature_name,
                         substitutions,
                         "(HOR) " if (config.make_hor and index == 0) else "")
                         # sub_reducer_feature_substitutions if is_main_reducer else {})

    if config.preview_all:
        generate_all_preview(config)

    p()
    p("Done")
    p()
