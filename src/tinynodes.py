class classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)
    
class TinyNode():
    CATEGORY = "utilities/tinynodes"
    FUNCTION = "func"
    DESCRIPTION = "tinynode"
    @classmethod    
    def INPUT_TYPES(cls):
        return {"required": { cls.LABEL:(cls.TYPE, {"forceInput": True})}}
    @classproperty
    def RETURN_TYPES(cls):
        return (cls.TYPE,)
    @classproperty
    def RETURN_NAMES(cls):
        return (cls.LABEL,)

    def func(self,**kwargs):
        return (kwargs[self.label],)
    
CLAZZES = [ type(f"Tiny{x.capitalize()}", (TinyNode,), {'TYPE':x, 'LABEL':x[0].lower()}) for x in ['STRING', 'INT', 'FLOAT'] ]
pass