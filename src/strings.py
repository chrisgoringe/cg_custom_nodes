from src.base import Base

class String(Base):
    CATEGORY = "CG/strings"
    REQUIRED = {"string": ("STRING", {"default":""})}
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, string):
        return (string,)
     
class SimpleLog(Base):
    CATEGORY = "CG/strings"
    REQUIRED = { "label": ("STRING", {"default":""}) }
    OPTIONAL = { "anything": ("*", {}) }
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    def func(self, label, anything=""):
        print (f"{label}{anything}")
        return ()
    
class Substitute(Base):
    CATEGORY = "CG/strings"
    REQUIRED = {"template": ("STRING", {"default":"", "multiline": True })}
    OPTIONAL = { "x": ("*", {}), "y": ("*", {}), "z": ("*", {}), }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, template:str, x="", y="", z=""):
        return (template.replace("[X]",str(x)).replace("[Y]",str(y)).replace("[Z]",str(z)),)    

class Truncate(Base):
    CATEGORY = "CG/strings"
    REQUIRED = {"string": ("*", {}), "length": ("INT", {"default":40})}
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, string, length):
        return (str(string)[:length],) 
    
CLAZZES = [String, SimpleLog, Substitute, Truncate]