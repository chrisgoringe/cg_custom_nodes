from src.base import Base, classproperty
from nodes import LoadImage
import folder_paths
from PIL import Image
import json
from common import read_config

DICTIONARY_NAME = read_config('dictionary_name')[0]
LABELS = list(read_config('dictionary_labels'))

class LoadImageWithDictionary(LoadImage):
    CATEGORY = 'CG/metadata'
    FUNCTION = 'func'
    RETURN_TYPES = ("IMAGE", "MASK", "DICTIONARY",)
    RETURN_NAMES = ("image", "mask", "dictionary",)

    def func(self, image):
        outputs = super().load_image(image)
        image_path = folder_paths.get_annotated_filepath(image)
        i = Image.open(image_path)
        try:
            dict = json.loads(i.text[DICTIONARY_NAME])
        except:
            dict = {}
        return outputs + (dict,)

class ExtractFromDictionary(Base):
    CATEGORY = 'CG/metadata'
    REQUIRED = { "dictionary": ("DICTIONARY", {}) }
    RETURN_TYPES = tuple("STRING" for _ in LABELS)
    RETURN_NAMES = tuple(LABELS)
    
    def func(self, dictionary:dict):
        return tuple(dictionary.get(label,"") for label in LABELS)

class MakeDictionary(Base):
    CATEGORY = "CG/metadata"
    OPTIONAL = { label:("*", {"forceInput":True}) for label in LABELS}
    RETURN_TYPES = ("DICTIONARY",)

    def func(self, **kwargs):
        dictionary = {label:kwargs[label] for label in LABELS if label in kwargs and kwargs[label]}
        return (dictionary,)

class AddExtraPngInfo(Base):
    CATEGORY = "CG/metadata"
    REQUIRED = { "image": ("IMAGE", {}), "dictionary": ("DICTIONARY", {}) }
    HIDDEN = { "extra_pnginfo": "EXTRA_PNGINFO" }
    RETURN_TYPES = ("IMAGE",)
    def func(self, image, dictionary:dict, extra_pnginfo:dict=None):
        extra_pnginfo[DICTIONARY_NAME] = dictionary
        return (image,)
    
CLAZZES = [MakeDictionary, AddExtraPngInfo, LoadImageWithDictionary, ExtractFromDictionary]