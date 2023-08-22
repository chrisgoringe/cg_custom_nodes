import random
from src.base import Base
import torch

class Stash(Base):
    stashed_items = {}
    previous = {}

    REQUIRED = { "stashable": ("*",), "id": ("STRING", { "default":"stash"} ), "purge": (("yes", "no"), {})}

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True
    CATEGORY = "CG/stash"

    def func(self, stashable, id, purge):
        if purge=="yes":
            Stash.previous = {}
        Stash.previous[id] = Stash.stashed_items[id] if id in Stash.stashed_items else None
        if purge=="yes":
            Stash.stashed_items = {}
        
        if isinstance(stashable,dict):
            Stash.stashed_items[id] = (stashable.copy(), random.random())
        elif isinstance(stashable,torch.Tensor):
            Stash.stashed_items[id] = (stashable.clone(), random.random())
        else:
            Stash.stashed_items[id] = (stashable, random.random())

        return ()
    
class UnStash(Base):
    REQUIRED = { "id": ("STRING", { "default":"stash" } ), "initial": ("",), "use": (("latest", "initial", "previous"), {})}  
    CATEGORY = "CG/stash"

    def func(self, id, initial, use):
        if (use=="latest" and id in Stash.stashed_items and Stash.stashed_items[id] is not None):
            return (Stash.stashed_items[id][0],)
        elif (use=="previous" and id in Stash.previous and Stash.previous[id] is not None):
            return (Stash.previous[id][0],)
        return (initial,)
    
    @classmethod
    def IS_CHANGED(cls, id, initial, use):
        if (use=="latest" and id in Stash.stashed_items and Stash.stashed_items[id] is not None):
            return (Stash.stashed_items[id][1],)
        elif (use=="previous" and id in Stash.previous and Stash.previous[id] is not None):
            return (Stash.previous[id][1],)
        return random.random()
    
class UnstashLatent(UnStash):
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    REQUIRED = UnStash.REQUIRED
    REQUIRED['initial'] = ("LATENT",)

CLAZZES = [Stash, UnstashLatent]