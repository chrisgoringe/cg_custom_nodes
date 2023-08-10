# All the nodes

Sorted by the subcategory they are located in (which correspond to the `.py` files )

## Base

Not a category, this contains a `Base` class that I use to abstract away a lot of the repetitive stuff.

## BLIP

### BlipToText

BLIP text description of an image. This code is a simplified version of Paulo Coronado's (Comfy Clip Blip Node)[https://github.com/paulo-coronado/comfy_clip_blip_node].

It requires fairscale, which may automatically install. If not, then 
```
ComfyUI_windows_portable\python_embeded\python.exe -m pip install fairscale
```

- Inputs
    - Image
    - Minimum output length
    - Maximum output length
- Outputs
    - Textual description of the image

