import torch
from src.base import Base
import math

def mask_to_image(mask:torch.tensor):
    return mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3)
    
class ImageSize(Base):
    CATEGORY = "CG/images"
    REQUIRED = { "image": ("IMAGE",), }
    RETURN_TYPES = ("INT","INT",)
    RETURN_NAMES = ("width","height",)
    def func(self, image:torch.Tensor):
        return (image.shape[2],image.shape[1],)
    
class CompareImages(Base):
    CATEGORY = "CG/images"
    REQUIRED = { "image1": ("IMAGE",), "image2": ("IMAGE",), }
    RETURN_TYPES = ("IMAGE","IMAGE")
    RETURN_NAMES = ("i1,i2,diff","diff")

    def func(self, image1:torch.Tensor, image2:torch.Tensor):
        diff = torch.abs(image1-image2)
        mean = torch.mean(diff,3)
        result = torch.stack([mean for _ in range(3)],3)
        combined = torch.cat((image1,image2,result),0)
        return (combined, result, )

class HardMask(Base):
    CATEGORY = "CG/images"
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

def resize(image, height, width):
    permed = torch.permute(image,(0, 3, 1, 2))
    scaled = torch.nn.functional.interpolate(permed, size=(height, width))
    return torch.permute(scaled, (0, 2, 3, 1))

class ExactResizeImage(Base):
    CATEGORY = "CG/images"
    REQUIRED = { 
        "image": ("IMAGE",) ,
        "width": ("INT", {"default": 512, "step":8}),  
        "height": ("INT", {"default": 512, "step":8}),  
    }
    RETURN_TYPES = ("IMAGE",)

    def func(self, image:torch.tensor, width:int, height:int):
        h,w = image.shape[1:3]
        return (image,) if (h==height and w==width) else (resize(image,height,width),)
    
class ResizeImage(Base):
    CATEGORY = "CG/images"
    REQUIRED = { 
        "image": ("IMAGE",) ,
        "x8": (["Yes", "No"],)
    }
    OPTIONAL = {
        "factor": ("FLOAT", {"default":1.0, "min":0.0, "step":0.1 }),
        "max_dimension": ("INT", {"default": 0, }),  
    }
    RETURN_TYPES = ("IMAGE",)

    def func(self, image:torch.tensor, x8:str, factor:float=1.0, max_dimension:int=0):
        h,w = image.shape[1:3]

        too_big_by = max(h*factor/max_dimension, w*factor/max_dimension, 1.0) if max_dimension else 1.0
        height = math.floor(h*factor/too_big_by)
        width = math.floor(w*factor/too_big_by)

        if x8=="Yes":
            height = ((4+height)//8) * 8
            width = ((4+width)//8) * 8
        
        return (image,) if (h==height and w==width) else (resize(image,height,width),)


class MergeLatents(Base):
    CATEGORY = "CG/images"
    REQUIRED = { 
        "latent1": ("LATENT",) ,
        "latent2": ("LATENT",) ,
        "weight_latent1": ("FLOAT",{"default":0.5, "min":0.0, "max":1.0, "step":0.05}),
        "weight_latent2": ("FLOAT",{"default":0.5, "min":0.0, "max":1.0, "step":0.05}),
        "weight_prompt": ("FLOAT",{"default":0.5, "min":0.0, "max":1.0, "step":0.05}),
    }
    RETURN_TYPES = ("LATENT","FLOAT",)
    RETURN_NAMES = ("latent","denoise,")

    def func(self, latent1:dict, latent2:dict, weight_latent1:float, weight_latent2:float, weight_prompt:float) -> tuple[dict]:
        mix = weight_latent2 / (weight_latent1+weight_latent2) if (weight_latent1+weight_latent2)!=0 else 0.5
        denoise = weight_prompt / (weight_prompt+weight_latent1+weight_latent2) if (weight_prompt+weight_latent1+weight_latent2) else 0.333
        keys = set(latent1.keys()) | set(latent2.keys())
        def merge(a,b,k,f):
            return (a[k]*(1-f) + b[k]*f) if k in a and k in b else a[k] if a in a else b[k]
        result = {key:merge(latent1, latent2, key, mix) for key in keys}
        return (result,denoise,)