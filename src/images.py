import torch
from src.base import Base_custom

def mask_to_image(mask:torch.tensor):
    return mask.reshape((-1, 1, mask.shape[-2], mask.shape[-1])).movedim(1, -1).expand(-1, -1, -1, 3)

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

        
CLAZZES = [ HardMask]