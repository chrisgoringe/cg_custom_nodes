import sys, os
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))

from .src.number import *
from .src.strings import *
from .src.images import *
from .src.stash import *
from .src.latents import *
from .src.dev import *
from .src.img2txt import *
from .src.conditioning import *
from .src.extensions import *

classes = ["CommonSizes", "RandomFloat", "RandomInt", 
           "CompareImages", "ImageSize", "HardMask", "ResizeImage", "ExactResizeImage", "MergeImages", "TextToImage",
           "MergeLatents", "MergeLatentsSettings",
           "MergeConditionings", "TwoClipTextEncode", 
           "String", "Substitute", "SimpleLog", "Truncate",
           "Stash", "UnStash",
           "TextDescriptionOfImage",
           ]
classes.extend(DEV_CLASSES)
classes.extend(EXT_CLASSES)

NODE_CLASS_MAPPINGS = { c:eval(c) for c in classes }
NODE_DISPLAY_NAME_MAPPINGS = { c:c for c in classes }
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
