import sys, os
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))

from .src.sizes import *
from .src.strings import *
from .src.randoms import *
from .src.images import *
from .src.stash import *
from .src.latents import *

classes = ["CreatePair","SplitPair","CommonSizes",
           "RandomFloats", 
           "CompareImages", "ImageSize", "HardMask", "ResizeImage", "ExactResizeImage", "MergeImages",
           "MergeLatents", "MergeLatentsSettings",
           "Loggit", "Stringify", "String", "Substitute",
           "Stash", "UnStash",
           ]

NODE_CLASS_MAPPINGS = { c:eval(c) for c in classes }
NODE_DISPLAY_NAME_MAPPINGS = { c:c for c in classes }
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
