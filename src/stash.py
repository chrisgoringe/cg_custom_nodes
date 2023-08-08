from src.base import Base
import torch

class Stash(Base):
    stashed_items = {}
    CATEGORY = "CG/stash"
    REQUIRED = { "image": ("IMAGE",), "id": ("STRING", { "default":"stash"} )}
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def func(self, image:torch.Tensor, id):
        Stash.stashed_items[id] = image.clone()
        return ()
    
class UnStash(Base):
    CATEGORY = "CG/stash"
    REQUIRED = { "id": ("STRING", { "default":"stash" } ), "initial": ("IMAGE",) }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    def func(self, id, initial:torch.Tensor):
        Stash.stashed_items[id] = image.clone()
        return (Stash.stashed_items[id] if id in Stash.stashed_items else initial ,)