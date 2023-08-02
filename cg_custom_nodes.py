import random
import torch

class Divide:
    def __init__(self):
        pass

    @classmethod    
    def INPUT_TYPES(s):
        return {
            "required": { 
                "width": ("INT", {"default": 1024, "min": 640, "max": 1536, "step": 8}) 
            },
        }
    
    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("width","height")
    FUNCTION = "divide"
    CATEGORY = "CG"

    def divide(self, width):
        return(width,int(1024*1024/width))
    
class Concat:
    def __init__(self):
        pass

    @classmethod    
    def INPUT_TYPES(s):
        return {
            "required": { 
                "s1": ("STRING", {"default": "", "multiline": True}),
                "s2": ("STRING", {"default": "", "multiline": True}), 
                "sep": ("STRING", {"default": "", "multiline": False}), 
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "concat"
    CATEGORY = "CG"

    def concat(self, s1, s2, sep):
        return (f"{s1}{sep}{s2}",)
    
class ToString:
    def __init__(self):
        pass

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "x2s"
    CATEGORY = "CG"
    PP = { "prefix": ("STRING", {"default":""}), "postfix": ("STRING", {"default":""}), }

    
class XToString(ToString):
    @classmethod    
    def INPUT_TYPES(s):
        return { "required": s.PP,
                 "optional": { 
                    "int": ("INT", {}), 
                    "float": ("FLOAT", {}),
                    "string": ("STRING", {})
                 }}
    def x2s(self, prefix, postfix, int, float, string):
        return (f"{prefix}{int or ''}{float or ''}{string or ''}{postfix}",)  

class IntToString(ToString):
    @classmethod    
    def INPUT_TYPES(s):
        return { "required": { "input": ("INT", {"default": 0}), } | s.PP }
    def x2s(self, input, prefix, postfix):
        return (f"{prefix}{input}{postfix}",)   
class FloatToString(ToString):
    @classmethod    
    def INPUT_TYPES(s):
        return { "required": { "input": ("FLOAT", {"default": 0.0}), } | s.PP }
    
class RandomFloats:
    def __init__(self):
        pass

    @classmethod    
    def INPUT_TYPES(s):
        return {
            "required": { 
                "minimum": ("FLOAT", {"default": 0.0}), 
                "maximum": ("FLOAT", {"default": 1.0}), 
                "seed": ("INT",{"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            }
        }
    RETURN_TYPES = ("FLOAT","FLOAT","FLOAT")
    RETURN_NAMES = ("f1","f2","f3")
    FUNCTION = "rand"
    CATEGORY = "CG"

    def rand(self, minimum, maximum, seed):
        state = random.getstate()
        random.seed(seed)
        rands = [random.uniform(minimum, maximum) for _ in range(3)]
        random.setstate(state=state)
        return rands
    
class ImageSize:
    def __init__(self):
        pass

    @classmethod    
    def INPUT_TYPES(s):
        return { "required": { "image": ("IMAGE",), }, }
    
    def image_size(self, image:torch.Tensor):
        print(image.shape)
        return (image.shape[2],image.shape[1],)

    RETURN_TYPES = ("INT","INT",)
    RETURN_NAMES = ("width","height",)
    FUNCTION = "image_size"
    CATEGORY = "CG"    
    OUTPUT_NODE = True    


