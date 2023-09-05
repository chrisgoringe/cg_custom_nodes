from src.base import Base_custom
import os, random

class Stringify(Base_custom):
    CATEGORY = "CG/strings"
    OPTIONAL = {"thing": ("*", {})}
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, thing=None):
        return (str(thing),)
    
class String(Base_custom):
    CATEGORY = "CG/strings"
    REQUIRED = {"string": ("STRING", {"default":""})}
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, string):
        return (string,)
    
class StringPair(Base_custom):
    CATEGORY = "CG/strings"
    REQUIRED = {"string1": ("STRING", {"default":""}), "string2": ("STRING", {"default":""})}
    RETURN_TYPES = ("STRING","STRING",)
    RETURN_NAMES = ("string1","string2",)
    def func(self, string1, string2):
        return (string1, string2)
     
class SimpleLog(Base_custom):
    CATEGORY = "CG/strings"
    REQUIRED = { "label": ("STRING", {"default":""}) }
    OPTIONAL = { "anything": ("*", {}) }
    RETURN_TYPES = ()
    OUTPUT_NODE = True
    def func(self, label, anything=""):
        print (f"{label}{anything}")
        return ()
    
class Substitute(Base_custom):
    CATEGORY = "CG/strings"
    REQUIRED = {"template": ("STRING", {"default":"", "multiline": True })}
    OPTIONAL = { "x": ("*", {}), "y": ("*", {}), "z": ("*", {}), }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, template:str, x="", y="", z=""):
        return (template.replace("[X]",str(x)).replace("[Y]",str(y)).replace("[Z]",str(z)),)    

class Truncate(Base_custom):
    CATEGORY = "CG/strings"
    REQUIRED = {"string": ("*", {}), "length": ("INT", {"default":40})}
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, string, length):
        return (str(string)[:length],) 
    
class SaveDescription(Base_custom):
    CATEGORY = "CG/strings"
    REQUIRED = {"description": ("STRING", {}), "image_filepath": ("STRING", {})}
    OUTPUT_NODE = True
    def func(self, description, image_filepath):
        text_filepath = os.path.splitext(image_filepath)[0] + ".txt"
        print(description, file=open(file=text_filepath,mode="w"))
        return ()

    
CLAZZES = [String, StringPair, Stringify, SimpleLog, Substitute, Truncate, SaveDescription]