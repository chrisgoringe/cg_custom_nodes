import sys, os, importlib, re
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
from common_custom import module_src_directory

NODE_CLASS_MAPPINGS= {}
NODE_DISPLAY_NAME_MAPPINGS = {}

def pretty(name:str):
    return " ".join(re.findall("[A-Z][a-z]*", name))

for module in [os.path.splitext(f)[0] for f in os.listdir(module_src_directory) if f.endswith('.py')]:
    imported_module = importlib.import_module(f"src.{module}")
    if 'CLAZZES' in imported_module.__dict__:
        for clazz in imported_module.CLAZZES:
            name = clazz.__name__
            NODE_CLASS_MAPPINGS[name] = clazz
            NODE_DISPLAY_NAME_MAPPINGS[name] = pretty(name)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

import shutil
import folder_paths

module_js_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")
application_root_directory = os.path.dirname(folder_paths.__file__)
application_web_extensions_directory = os.path.join(application_root_directory, "web", "extensions", "A_UNIQUE_NAME")

shutil.copytree(module_js_directory, application_web_extensions_directory, dirs_exist_ok=True)
