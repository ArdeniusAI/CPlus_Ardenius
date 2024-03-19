"""
@author: AMA
@title: Ardenius
@nickname: Ardenius
@description: CPlus control box is designed to gather workflow variables into 1 node.
"""
#  this software and code © 2024 is licensed under Attribution-NonCommercial-NoDerivatives 4.0 International
#  ( owner contact information ardenius7@gmail.com attribution link https://ko-fi.com/ardenius )
#  FREE FOR PERSONAL USE -- FOR COMMERCIAL USE 	visit https://ko-fi.com/ardenius
#  and is based upon code licensed under General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.txt by 
#  contributers found here https://github.com/comfyanonymous/ComfyUI
#  thus all code here is released to the user.


import os.path
import folder_paths
import numpy as np
import torch
import comfy.model_management
import comfy.samplers

MAX_RESOLUTION = 8192

class Control_Box:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 0
        self.device = comfy.model_management.intermediate_device()

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {
                    "width": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                    "height": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                    "latent_batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
                    "cfg": ("FLOAT", {"default": 8, "min": 0.1, "max": 15, "step": 0.1}),
                    "steps": ("INT", {"default": 20, "min": 1, "max": 100, "step": 1}),
                    "denoise": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 1.0, "step": 0.01}),
                    "scaler": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 4.0, "step": 0.01}),
                    "seed": ("INT", {"default": 1234567891, "min": 1, "max": 9999999999, "step": 1}),
                    "positive_prompt": ("CONDITIONING", {"default": ""}),
                    "negative_prompt": ("CONDITIONING", {"default": ""}),
                    "model": ("MODEL",),
                    "clip": ("CLIP",),
                    "vae": ("VAE",),
                    },
                }

    RETURN_NAMES = ("model", "positive", "negative", "latent_out", "seed", "cfg", "steps", "denoise", "scaler", "clip", "vae", "width", "height",)
    RETURN_TYPES = ("MODEL", "CONDITIONING", "CONDITIONING", "LATENT", "INT", "FLOAT", "INT", "FLOAT", "FLOAT", "CLIP", "VAE", "INT", "INT",)

    FUNCTION = "output_function"

    OUTPUT_NODE = True

    CATEGORY = "CPlus"

    def output_function(self, width, height, latent_batch_size, cfg, steps, denoise, scaler, seed, positive_prompt, negative_prompt, model, clip, vae):

        remainder = width % 8
        width = width + remainder

        remainder = height % 8
        height = height + remainder

        latent_out = self.generate_latent(width, height, latent_batch_size)

        return model, positive_prompt, negative_prompt, latent_out, seed, cfg, steps, denoise, scaler, clip, vae, width, height

    def generate_latent(self, width, height, latent_batch_size=1):
        latent = torch.zeros([latent_batch_size, 4, height // 8, width // 8], device=self.device)
        return {"samples":latent}
