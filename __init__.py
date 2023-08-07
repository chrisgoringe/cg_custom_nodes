from .cg_custom_nodes import *

classes = ["RandomFloats","ImageSize","Fractions",
           "CreatePair","SplitPair","CommonSizes","Loggit","CompareImages",
           "HardMask", "ResizeImage", "Stringify","String" ]

NODE_CLASS_MAPPINGS = { c:eval(c) for c in classes }
NODE_DISPLAY_NAME_MAPPINGS = { c:c for c in classes }
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
