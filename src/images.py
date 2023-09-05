import torch
from src.base import Base_custom
import math, os, random
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
from common_custom import module_resource_directory

def mask_to_image(mask:torch.tensor):
    return mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3)
     
class CompareImages(Base_custom):
    CATEGORY = "CG/images"
    REQUIRED = { "image1": ("IMAGE",), "image2": ("IMAGE",), }
    RETURN_TYPES = ("IMAGE","IMAGE")
    RETURN_NAMES = ("i1_i2_diff","diff")

    def func(self, image1:torch.Tensor, image2:torch.Tensor):
        diff = torch.abs(image1-image2)
        mean = torch.mean(diff,3)
        result = torch.stack([mean for _ in range(3)],3)
        combined = torch.cat((image1,image2,result),0)
        return (combined, result, )

class HardMask(Base_custom):
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

        
CLAZZES = [CompareImages, HardMask]