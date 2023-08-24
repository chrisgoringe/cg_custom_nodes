import os, yaml

module_root_directory = os.path.dirname(os.path.realpath(__file__))
module_src_directory = os.path.join(module_root_directory,'src')
module_resource_directory = os.path.join(module_src_directory,'resources')

config_file = os.path.join(module_resource_directory,'configuration.yaml')

def read_config(item):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)[item]