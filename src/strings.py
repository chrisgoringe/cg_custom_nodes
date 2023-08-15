from src.base import Base

class String(Base):
    CATEGORY = "CG/strings"
    REQUIRED = {"string": ("STRING", {"default":""})}
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, string):
        return (string,)
    
class Stringify(Base):
    CATEGORY = "CG/strings"
    REQUIRED = { }
    OPTIONAL = { "anything": ("*", {}), "anything2": ("*", {}), "anything3": ("*", {}), "anything4": ("*", {}), }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, **kwargs):
        return ("".join([(f"{kwargs[s]}") for s in kwargs]),)
    
class Loggit(Stringify):
    CATEGORY = "CG/strings"
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    def func(self, **kwargs):
        print ("\x1b[38;21m"+"".join([(f"{kwargs[s]}") for s in kwargs])+"\x1b[0m")
        return ()
    
class SimpleLog(Loggit):
    REQUIRED = { "label": ("STRING", {"default":""}) }
    OPTIONAL = { "anything": ("*", {}) }
    
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
        return (str(string)[:length]) 