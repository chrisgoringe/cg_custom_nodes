from src.base import Base_custom
import torch
from comfy.sample import prepare_noise

class MergeLatents(Base_custom):
    CATEGORY = "CG/latents"
    REQUIRED = { 
        "latent1": ("LATENT",) ,
        "latent2": ("LATENT",) ,
        "latent2weight": ("FLOAT",{"default":0.5, "min":0.0, "max":1.0, "step":0.01}),
    }
    RETURN_TYPES = ("LATENT", )
    RETURN_NAMES = ("latent", )

    def func(self, latent1:dict, latent2:dict, latent2weight:float):
        keys = set(latent1.keys()) | set(latent2.keys())
        def merge(a,b,k,f):
            return (a[k]*(1-f) + b[k]*f) if k in a and k in b else a[k] if a in a else b[k]
        result = {key:merge(latent1, latent2, key, latent2weight) for key in keys}
        return (result, )
    
class MergeLatentsSettings(Base_custom):
    CATEGORY = "CG/latents"  
    REQUIRED = { 
        "latent2weight": ("FLOAT",{"default":0.5, "min":0.0, "max":1.0, "step":0.01}),
        "denoise_stage1": ("FLOAT",{"default":0.4, "min":0.0, "max":1.0, "step":0.01}),
        "denoise_stage2": ("FLOAT",{"default":0.4, "min":0.0, "max":1.0, "step":0.01}),
    }
    RETURN_TYPES = ("FLOAT", "FLOAT", "FLOAT", )
    RETURN_NAMES = ("latent2weight", "denoise_stage1", "denoise_stage2", )
    def func(self, latent2weight, denoise_stage1, denoise_stage2):
        return (latent2weight, denoise_stage1, denoise_stage2)

class CombineSamples(Base_custom):
    CATEGORY = "CG/latents"
    REQUIRED = { 
        "latent1": ("LATENT",) ,
        "latent2": ("LATENT",) ,
    }
    OPTIONAL = {
        "latent3": ("LATENT",) ,
        "latent4": ("LATENT",) ,
    }
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("samples",)
    def func(self, latent1, latent2, latent3={}, latent4={}):
        result = {}
        for key in latent1:
            list = [l[key] for l in (latent1, latent2, latent3, latent4) if key in l]
            if isinstance(list[0], torch.Tensor):
                result[key] = torch.cat(tuple(list),0)
            else:
                result[key] = list[0]
        return (result,)
        
CLAZZES = [MergeLatents, MergeLatentsSettings, CombineSamples]