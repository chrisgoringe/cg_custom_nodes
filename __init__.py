from .src.sizes import *
from .src.strings import *
from .src.randoms import *
from .src.images import *

classes = ["CreatePair","SplitPair","CommonSizes",
           "RandomFloats", 
           "CompareImages", "ImageSize", "HardMask", "ResizeImage", 
           "Loggit", "Stringify", "String", "Substitute" 
           ]

NODE_CLASS_MAPPINGS = { c:eval(c) for c in classes }
NODE_DISPLAY_NAME_MAPPINGS = { c:c for c in classes }
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
