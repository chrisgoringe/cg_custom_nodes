import random
import torch
from collections import namedtuple
import math

class Base:
    def __init__(self):
        pass
    CATEGORY = "CG"
    FUNCTION = "func"
    OPTIONAL = None
    @classmethod    
    def INPUT_TYPES(s):
        types = {"required": s.REQUIRED}
        if s.OPTIONAL:
            types["optional"] = s.OPTIONAL
        return types
    
Pair = namedtuple('Pair', ['x', 'y'])
Region = namedtuple('Region', ['x','y','width','height'])

class CreatePair(Base):
    REQUIRED = { "x": ("INT", {"default": 512}), "y": ("INT", {"default": 512}) }
    RETURN_TYPES = ("PAIR",)
    RETURN_NAMES = ("pair",)
    def func(self,x,y):
        return (Pair(x, y),)

class SplitPair(Base):
    REQUIRED = { "pair": ("PAIR", {}), }
    RETURN_TYPES = ("INT","INT",)
    RETURN_NAMES = ("x or width","y or height",)
    def func(self,pair):
        return (pair.x, pair.y,)
    
class CommonSizes(Base):
    REQUIRED = { "size": (("512x512", "512x768", "512x1014", "768x512", "768x768", "768x1024", "1024x512", "1024x768", "1024x1024"), {}) }
    RETURN_TYPES = ("PAIR","INT","INT")
    RETURN_NAMES = ("size","width","height")
    def func(self,size:str):
        x, y = [int(v) for v in size.split('x')]
        return (Pair(x,y),x,y)

class Fractions(Base):
    REQUIRED = { "value": ("INT", {"default": 1024}) } 
    RETURN_TYPES = ("INT","INT","INT","INT","INT","INT","INT","INT","INT")
    RETURN_NAMES = ("0","1/6","1/4","1/3","1/2","2/3","3/4","5/6","1")
    def func(self, value:int):
        return(0,value//6,value//4,value//3,value//2,2*value//3,3*value//4,5*value//6,value)  

class String(Base):
    REQUIRED = {"string": ("STRING", {"default":""})}
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, string):
        return (string,)
    
class Stringify(Base):
    REQUIRED = { }
    OPTIONAL = { "anything": ("*", {}), "anything2": ("*", {}), "anything3": ("*", {}), "anything4": ("*", {}), }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, **kwargs):
        return ("".join([(f"{kwargs[s]}") for s in kwargs]),)
    
class Loggit(Stringify):
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    def func(self, *args):
        print (super().func(args)[0])
        return ()

class RandomFloats(Base):
    REQUIRED = { 
                "minimum": ("FLOAT", {"default": 0.0}), 
                "maximum": ("FLOAT", {"default": 1.0}), 
                "seed": ("INT",{"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
    RETURN_TYPES = ("FLOAT","FLOAT","FLOAT")
    RETURN_NAMES = ("f1","f2","f3")

    def func(self, minimum, maximum, seed):
        state = random.getstate()
        random.seed(seed)
        rands = [random.uniform(minimum, maximum) for _ in range(3)]
        random.setstate(state=state)
        return rands
    
class ImageSize(Base):
    REQUIRED = { "image": ("IMAGE",), }
    RETURN_TYPES = ("INT","INT",)
    RETURN_NAMES = ("width","height",)
    def func(self, image:torch.Tensor):
        print(image.shape)
        return (image.shape[2],image.shape[1],)
    
class CompareImages(Base):
    REQUIRED = { "image1": ("IMAGE",), "image2": ("IMAGE",), }
    RETURN_TYPES = ("IMAGE","IMAGE")
    RETURN_NAMES = ("i1,i2,diff","diff")

    def func(self, image1:torch.Tensor, image2:torch.Tensor):
        diff = torch.abs(image1-image2)
        mean = torch.mean(diff,3)
        result = torch.stack([mean for _ in range(3)],3)
        combined = torch.cat((image1,image2,result),0)
        return (combined, result, )

def mask_to_image(mask):
    return mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3)

class HardMask(Base):
    REQUIRED = { "threshold": ("FLOAT",{"default": 0.5, "min": 0.0, "max": 1.0}) }
    OPTIONAL = {
        "mask": ("MASK",),
        "image": ("IMAGE",)
    }
    RETURN_TYPES = ("MASK","IMAGE",)

    def func(self, threshold, mask=None, image=None):
        mask = mask if mask is not None else torch.mean(image,3)
        m = torch.where(mask>threshold,1.0,0.0)
        return (m, mask_to_image(m),)

class ResizeImage(Base):
    REQUIRED = { 
        "image": ("IMAGE",) ,
        "x8": (["Yes", "No"],)
    }
    OPTIONAL = { "max_dimension": ("INT", {"default": 0}),  }
    RETURN_TYPES = ("IMAGE",)

    def func(self, image:torch.tensor, x8:str, max_dimension:int=0):
        b,h,w = image.shape[0:3]

        too_big_by = max(h/max_dimension, w/max_dimension, 1.0) if max_dimension else 1.0
        new_h = math.floor(h/too_big_by)
        new_w = math.floor(w/too_big_by)

        if x8=="Yes":
            new_h = ((4+new_h)//8) * 8
            new_w = ((4+new_w)//8) * 8

        if (h==new_h and w==new_w):
            return (image,)
        
        permed = torch.permute(image,(0, 3, 1, 2))
        scaled = torch.nn.functional.interpolate(permed, size=(new_h, new_w))
        return (torch.permute(scaled, (0, 2, 3, 1)),)
        
    