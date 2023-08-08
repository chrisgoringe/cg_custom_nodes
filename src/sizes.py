from collections import namedtuple
from src.base import Base
    
Pair = namedtuple('Pair', ['x', 'y'])
Region = namedtuple('Region', ['x','y','width','height'])

class CreatePair(Base):
    CATEGORY = "CG/sizes"
    REQUIRED = { "x": ("INT", {"default": 512}), "y": ("INT", {"default": 512}) }
    RETURN_TYPES = ("PAIR",)
    RETURN_NAMES = ("pair",)
    def func(self,x,y):
        return (Pair(x, y),)

class SplitPair(Base):
    CATEGORY = "CG/sizes"
    REQUIRED = { "pair": ("PAIR", {}), }
    RETURN_TYPES = ("INT","INT",)
    RETURN_NAMES = ("x or width","y or height",)
    def func(self,pair):
        return (pair.x, pair.y,)
    
class CommonSizes(Base):
    CATEGORY = "CG/sizes"
    REQUIRED = { "size": (("512x512", "512x768", "512x1024", "768x512", "768x768", "768x1024", "1024x512", "1024x768", "1024x1024"), {}) }
    RETURN_TYPES = ("PAIR","INT","INT")
    RETURN_NAMES = ("size","width","height")
    def func(self,size:str):
        x, y = [int(v) for v in size.split('x')]
        return (Pair(x,y),x,y)
