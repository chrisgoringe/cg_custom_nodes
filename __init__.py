import sys, os, importlib, shutil
module_root_directory = os.path.dirname(os.path.realpath(__file__))
module_src_directory = os.path.join(module_root_directory,'src')
module_resource_directory = os.path.join(module_src_directory,'resources')

sys.path.insert(0,module_root_directory)

NODE_CLASS_MAPPINGS= {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for module in [os.path.splitext(f)[0] for f in os.listdir(os.path.join(module_root_directory,'src')) if f.endswith('.py')]:
    imported_module = importlib.import_module(f"src.{module}")
    if 'CLAZZES' in imported_module.__dict__:
        for clazz in imported_module.CLAZZES:
            name = clazz.__name__
            NODE_CLASS_MAPPINGS[name] = clazz
            NODE_DISPLAY_NAME_MAPPINGS[name] = name

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

import folder_paths

src = os.path.join(module_root_directory, "js")
dst = os.path.join(os.path.dirname(folder_paths.__file__), "web", "extensions")
shutil.copytree(src, dst, dirs_exist_ok=True)