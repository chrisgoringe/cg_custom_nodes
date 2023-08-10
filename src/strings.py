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
        print ("".join([(f"{kwargs[s]}") for s in kwargs]))
        return ()
    
class SimpleLog(Loggit):
    REQUIRED = { "label": ("STRING", {"default":""}) }
    OPTIONAL = { "anything": ("*", {}) }
    
class Substitute(Base):
    CATEGORY = "CG/strings"
    REQUIRED = {"template": ("STRING", {"default":"", "multiline": True })}
    OPTIONAL = { "x": ("String", {}), "y": ("String", {}), "z": ("String", {}), }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, template:str, x="", y="", z=""):
        return (template.replace("[X]",x).replace("[Y]",y).replace("[Z]",z),)    
