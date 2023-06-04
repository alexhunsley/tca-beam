import os
from jinja2 import Environment, FileSystemLoader

def process_template(script_dir):

    os.chdir(script_dir)

    # Define the template directory
    file_loader = FileSystemLoader('templates')

    # Create the environment
    env = Environment(loader=file_loader)


    # Prepare the substitutions
    feature_name = "Thingo"
    substitutions = {
        'viewClass': f"{feature_name}View",
        'featureClass': f"{feature_name}ViewFeature"
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
    output = one_file_template.render(main_file_substitutions)

    print(output)

    # output = view_feature_template.render(substitutions)
    # print(output)


def start():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    process_template(script_dir)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
