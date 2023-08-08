class Base:
    def __init__(self):
        pass
    FUNCTION = "func"
    OPTIONAL = None
    @classmethod    
    def INPUT_TYPES(s):
        types = {"required": s.REQUIRED}
        if s.OPTIONAL:
            types["optional"] = s.OPTIONAL
        return types