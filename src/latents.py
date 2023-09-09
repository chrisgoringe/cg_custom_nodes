from src.base import Base_custom

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
          
CLAZZES = [MergeLatents]