from src.base import Base
from nodes import ConditioningSetMask, CLIPTextEncode

class MergeConditionings(Base):
    CATEGORY = "CG/conditioning"
    REQUIRED = {"conditioning1": ("CONDITIONING", ), "conditioning2": ("CONDITIONING", ),"mask": ("MASK", ), }
    RETURN_TYPES = ("CONDITIONING", )
    RETURN_NAMES = ("conditioning", )
    apply_mask = ConditioningSetMask().append

    def func(self, conditioning1, conditioning2, mask):
        c1 = self.apply_mask(conditioning1, mask, "default", 1.0)[0]
        c2 = self.apply_mask(conditioning2, 1.0-mask, "default", 1.0)[0]
        return (c1+c2, )
    
class TwoClipTextEncode(Base):
    CATEGORY = "CG/conditioning"
    REQUIRED = {"clip": ("CLIP", {}), "positive": ("STRING", {"default":""}), "negative": ("STRING", {"default":""})}
    RETURN_TYPES = ("CONDITIONING", "CONDITIONING",)
    RETURN_NAMES = ("positive", "negative",)
    encoder = CLIPTextEncode().encode

    def func(self, clip, positive, negative):
        return(self.encoder(clip,positive)[0], self.encoder(clip,negative)[0], )

CLAZZES = [MergeConditionings, TwoClipTextEncode]