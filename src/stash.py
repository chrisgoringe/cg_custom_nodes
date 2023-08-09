import random

class Stash:
    stashed_items = {}
    previous = {}

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
            Stash.previous = {}
        Stash.previous[id] = Stash.stashed_items[id] if id in Stash.stashed_items else None
        if purge=="yes":
            Stash.stashed_items = {}
        
        Stash.stashed_items[id] = ({x:latent[x] for x in latent}, random.random())
        return ()
    
class UnStash:
    def __init__(self):
        pass

    @classmethod    
    def INPUT_TYPES(s):
        return {"required": { "id": ("STRING", { "default":"stash" } ), "initial": ("LATENT",), "use": (("latest", "previous", "initial"), {})} } 

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    CATEGORY = "CG/stash"
    FUNCTION = "func"

    def func(self, id, initial, use):
        if (use=="latest" and id in Stash.stashed_items):
            return (Stash.stashed_items[id][0],)
        elif (use=="previous" and id in Stash.previous):
            return (Stash.previous[id][0],)
        return (initial,)
    
    @classmethod
    def IS_CHANGED(cls, id, initial, use):
        if (use=="latest" and id in Stash.stashed_items):
            return (Stash.stashed_items[id][1],)
        elif (use=="previous" and id in Stash.previous):
            return (Stash.previous[id][1],)
        return 0.0