import os, yaml
import folder_paths

application_root_directory = os.path.dirname(folder_paths.__file__)
application_web_extensions_directory = os.path.join(application_root_directory, "web", "extensions")

module_root_directory = os.path.dirname(os.path.realpath(__file__))
module_src_directory = os.path.join(module_root_directory,'src')
module_resource_directory = os.path.join(module_src_directory,'resources')
module_js_directory = os.path.join(module_root_directory, "js")

config_file = os.path.join(module_resource_directory,'configuration.yaml')

def read_config(item):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)[item]