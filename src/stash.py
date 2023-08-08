from src.base import Base
import torch
import random

class Stash(Base):
    stashed_items = {}
    CATEGORY = "CG/stash"
    REQUIRED = { "latent": ("LATENT",), "id": ("STRING", { "default":"stash"} ), "purge": (("yes", "no"), {})}
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True

    def func(self, latent:torch.Tensor, id, purge):
        if purge=="yes":
            Stash.stashed_items = {}
        Stash.stashed_items[id] = (latent.clone(), random.random())
        return ()
    
class UnStash(Base):
    CATEGORY = "CG/stash"
    REQUIRED = { "id": ("STRING", { "default":"stash" } ), "initial": ("IMAGE",) }
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    def func(self, id, initial:torch.Tensor):
        return (Stash.stashed_items[id][0] if id in Stash.stashed_items else initial ,)
    
    @classmethod
    def IS_CHANGED(cls, id, **kwargs):
        return Stash.stashed_items[id][1] if id in Stash.stashed_items else 0.0