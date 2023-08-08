import random

class Stash:
    stashed_items = {}

    def __init__(self):
        pass

    @classmethod    
    def INPUT_TYPES(s):
        return {"required":  { "latent": ("LATENT",), "id": ("STRING", { "default":"stash"} ), "purge": (("yes", "no"), {})}}

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    OUTPUT_NODE = True
    CATEGORY = "CG/stash"
    FUNCTION = "func"

    def func(self, latent, id, purge):
        if purge=="yes":
            Stash.stashed_items = {}
        
        Stash.stashed_items[id] = ({x:latent[x] for x in latent}, random.random())
        return ()
    
class UnStash:
    def __init__(self):
        pass

    @classmethod    
    def INPUT_TYPES(s):
        return {"required": { "id": ("STRING", { "default":"stash" } ), "initial": ("LATENT",), "skip": (("no", "yes"), {})} } 

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    CATEGORY = "CG/stash"
    FUNCTION = "func"

    def func(self, id, initial, skip):
        return (Stash.stashed_items[id][0] if (skip=="no" and id in Stash.stashed_items) else initial ,)
    
    @classmethod
    def IS_CHANGED(cls, id, **kwargs):
        return Stash.stashed_items[id][1] if id in Stash.stashed_items else 0.0