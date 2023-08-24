from src.base import Base, classproperty
from nodes import LoadImage
import folder_paths
from PIL import Image
import json
from common import read_config

class LoadImageWithDictionary(LoadImage):
    CATEGORY = 'CG/metadata'
    FUNCTION = 'func'
    RETURN_TYPES = ("IMAGE", "MASK", "DICTIONARY",)
    RETURN_NAMES = ("image", "mask", "dictionary",)

    @classmethod
    def INPUT_TYPES(s):
        inputs = LoadImage.INPUT_TYPES()
        inputs['required']['label'] = ("STRING", {"default":"cg"})
        return inputs

    def func(self, image, label):
        outputs = super().load_image(image)
        image_path = folder_paths.get_annotated_filepath(image)
        i = Image.open(image_path)
        try:
            dict = json.loads(i.text[label])
        except:
            dict = {}
        return outputs + (dict,)
    
    @classmethod
    def IS_CHANGED(s, image, label):
        return LoadImage.IS_CHANGED(image)

    @classmethod
    def VALIDATE_INPUTS(s, image, label):
        return LoadImage.VALIDATE_INPUTS(image)

class ExtractFromDictionary(Base):
    LABELS = list(read_config('dictionary_labels'))
    CATEGORY = 'CG/metadata'
    REQUIRED = { "dictionary": ("DICTIONARY", {}) }

    @classproperty
    def OPTIONAL(cls):
        return { f"label{i+1}": ("STRING", {"default":label}) for i, label in enumerate(cls.LABELS) }
    
    @classproperty
    def RETURN_TYPES(cls):
        return tuple("STRING" for _ in cls.LABELS)
    
    def func(self, dictionary:dict, **kwargs):
        return tuple(dictionary.get(kwargs.get(f"label{i+1}","")) or "" for i in range(len(self.LABELS)))

class MakeDictionary(Base):
    CATEGORY = "CG/metadata"
    REQUIRED = {}
    OPTIONAL = { "append_to": ("DICTIONARY", {}),
                 "label1": ("STRING", {}), "object1": ("*", {}),
                 "label2": ("STRING", {}), "object2": ("*", {}),
                 "label3": ("STRING", {}), "object3": ("*", {}),
                 "label4": ("STRING", {}), "object4": ("*", {}),                  
                }
    RETURN_TYPES = ("DICTIONARY",)
    def func(self, append_to=None, **kwargs):
        dictionary = append_to or {}
        for (label,object) in [(kwargs.get(f"label{i}",None), kwargs.get(f"object{i}",None)) for i in range(1,5)]:
            if label and object:
                dictionary[label] = object
        return (dictionary,)

class AddExtraPngInfo(Base):
    CATEGORY = "CG/metadata"
    REQUIRED = { "image": ("IMAGE", {}), "label": ("STRING", {"default":"cg"}) }
    OPTIONAL = { "dictionary": ("DICTIONARY", {}) }
    HIDDEN = { "extra_pnginfo": "EXTRA_PNGINFO" }
    RETURN_TYPES = ("IMAGE",)
    def func(self, image, label:str, dictionary:dict=None, extra_pnginfo:dict=None):
        if label and dictionary:
            if extra_pnginfo:
                extra_pnginfo[label] = dictionary
            else:
                print("ERROR - AddExtraPngInfo didn't receive extra_pnginfo")
        return (image,)
    
CLAZZES = [MakeDictionary, AddExtraPngInfo, LoadImageWithDictionary, ExtractFromDictionary]