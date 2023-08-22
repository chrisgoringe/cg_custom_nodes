import sys, os, importlib
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))

NODE_CLASS_MAPPINGS= {}
NODE_DISPLAY_NAME_MAPPINGS = {}

for module in [os.path.splitext(f)[0] for f in os.listdir("src") if f.endswith('.py')]:
    imported_module = importlib.import_module(f"src.{module}")
    if 'CLAZZES' in imported_module.__dict__:
        for clazz in imported_module.CLAZZES:
            name = clazz.__name__
            NODE_CLASS_MAPPINGS[name] = clazz
            NODE_DISPLAY_NAME_MAPPINGS[name] = name

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']