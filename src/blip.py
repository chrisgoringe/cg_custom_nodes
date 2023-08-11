from src.base import Base

class TextDescriptionOfImage(Base):
    CATEGORY = "CG/blip"
    REQUIRED = { "image": ("IMAGE",),
                 "min_length": ("INT", {"default":5, "min":0, "max":100}), 
                 "max_length": ("INT", {"default":5, "min":0, "max":100}) }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text")
    pass