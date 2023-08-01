import random

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
    
class FloatToString:
    def __init__(self):
        pass

    @classmethod    
    def INPUT_TYPES(s):
        return {
            "required": { "float": ("FLOAT", {"default": 0.0}), }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "f2s"
    CATEGORY = "CG"

    def f2s(self, float):
        return (f"{float}",)   
    
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

NODE_CLASS_MAPPINGS = {
    "Divide": Divide,
    "Concat": Concat,
    "FloatToString": FloatToString,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Divide": "Divide",
    "Concat": "Concat",
    "FloatToString": "FloatToString",
}
