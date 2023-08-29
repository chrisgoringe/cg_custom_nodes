from base import Base_custom, classproperty

PARAMETERS = {}

class SetParameters(Base_custom):
    CATEGORY = "CG/parameters"
    PRIORITY = 1  # see pull request 1348 on ComfyUI
    @classproperty
    def OPTIONAL(cls):
        optional = {}
        for i in (1,2,3):
            optional[f"label{i}"] = ("STRING", {"default":f"label{i}"})
            optional[f"value{i}"] = ("STRING", {"default":""})
        return optional

    def func(self, **kwargs):
        for i in (1,2,3):
            if f"label{i}" in kwargs and f"value{i}" in kwargs:
                PARAMETERS[kwargs[f"label{i}"]] = kwargs[f"value{i}"]
        return ()

    OUTPUT_NODE = True

class GetParameter(Base_custom):
    CATEGORY = "CG/parameters"
    REQUIRED = { "label": ("STRING",{"default":""}) }
    def func(self, label):
        try:
            return (self.CAST(PARAMETERS[label]),)
        except:
            return (self.DEFAULT,)

class GetParameterInt(GetParameter):
    RETURN_TYPES = ("INT",)
    CAST = int
    DEFAULT = 0
    
class GetParameterFloat(GetParameter):
    RETURN_TYPES = ("FLOAT",)
    CAST = float
    DEFAULT = 0.0

class GetParamterString(GetParameter):
    RETURN_TYPES = ("STRING",)
    CAST = str
    DEFAULT = ""


    
CLAZZES = [ SetParameters, GetParameterInt, GetParameterFloat, GetParamterString ]