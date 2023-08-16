import torch
from src.base import Base
import math, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def mask_to_image(mask:torch.tensor):
    return mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3)
    
class ImageSize(Base):
    CATEGORY = "CG/images"
    REQUIRED = { "image": ("IMAGE",), }
    RETURN_TYPES = ("INT","INT","INT","INT")
    RETURN_NAMES = ("width","height","batch","channels")
    def func(self, image:torch.Tensor):
        return (image.shape[2],image.shape[1],image.shape[0],image.shape[3])
    
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

class MergeImages(Base):
    CATEGORY = "CG/images"
    REQUIRED = { 
        "image1": ("IMAGE",) ,
        "image2": ("IMAGE",) ,
        "image2weight": ("FLOAT",{"default":0.5, "min":0.0, "max":1.0, "step":0.01}),
    }
    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )

    def func(self, image1:torch.Tensor, image2:torch.Tensor, image2weight:float) -> torch.Tensor:
        return (image1*(1-image2weight)+image2*image2weight, )

def pillow_to_tensor(image: Image.Image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class TextToImage(Base):
    CATEGORY = "CG/images"
    REQUIRED = { 
        "text": ("STRING", {}),
        "width": ("INT", {"default":512}),
        "height": ("INT", {"default":32}), 
        "font_size": ("INT", {"default":24}),  
    }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    OUTPUT_NODE = True

    def func(self, text:str, width:int, height:int, font_size:int):
        image = Image.new("RGB",(width,height),color="white")
        draw = ImageDraw.Draw(image)
        draw.font = ImageFont.truetype( os.path.join(os.path.dirname(os.path.realpath(__file__)),"font","Roboto-Regular.ttf"), size=font_size)
        draw.text(xy=(4,4), text=text, fill="black")
        return (pillow_to_tensor(image),)