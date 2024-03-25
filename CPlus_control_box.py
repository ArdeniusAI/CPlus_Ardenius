"""
@author: initials AMA
@title: Ardenius
@nickname: Ardenius
@description: CPlus control box is designed to gather workflow variables into 1 node for easier control of your workflow.
"""
#  this software and code © 2024 initals AMA nickname Ardenius is licensed under GPL V3.0 
#  ( author contact information ardenius7@gmail.com attribution link https://ko-fi.com/ardenius )
#  ➡️ follow me at https://ko-fi.com/ardenius on the top right corner (follow)
#  📸 Change the mood ! by Visiting my AI Image Gallery
#  🏆 Premium Memebers only Perks (Premium SD Models, ComfyUI custom nodees, and more to come)
#  the below code is in part or in full based upon ComfyUI code licensed under General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.txt by
#  contributers found here https://github.com/comfyanonymous/ComfyUI


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
                    "cfg": ("FLOAT", {"default": 8, "min": 0.1, "max": 15, "step": 0.1}),
                    "steps": ("INT", {"default": 20, "min": 1, "max": 100, "step": 1}),
                    "denoise": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 1.0, "step": 0.01}),
                    "scaler": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 4.0, "step": 0.01}),
                    "seed": ("INT", {"default": 1234567891, "min": 1, "max": 9999999999, "step": 1}),
                    "positive_prompt": ("CONDITIONING", {"default": ""}),
                    "negative_prompt": ("CONDITIONING", {"default": ""}),
                    "model": ("MODEL",),
                    "vae": ("VAE",),
                    "width": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                    "height": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                    "latent_width": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                    "latent_height": ("INT", {"default": 1024, "min": 64, "max": MAX_RESOLUTION, "step": 8}),
                    "latent_batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
                    },
                }

    RETURN_NAMES = ("model", "positive", "negative", "latent_out", "seed", "cfg", "steps", "denoise", "scaler", "vae", "width", "height", "latent_width", "latent_height",)
    RETURN_TYPES = ("MODEL", "CONDITIONING", "CONDITIONING", "LATENT", "INT", "FLOAT", "INT", "FLOAT", "FLOAT", "VAE", "INT", "INT", "INT", "INT",)

    FUNCTION = "output_function"

    OUTPUT_NODE = True

    CATEGORY = "CPlus"

    def output_function(self, cfg, steps, denoise, scaler, seed, positive_prompt, negative_prompt, model, vae, width, height, latent_width, latent_height, latent_batch_size):

        remainder = width % 8
        width = width + remainder

        remainder = height % 8
        height = height + remainder

        remainder = latent_width % 8
        latent_width = latent_width + remainder

        remainder = latent_height % 8
        latent_height = latent_height + remainder

        latent_out = self.generate_latent(latent_width, latent_height, latent_batch_size)

        return model, positive_prompt, negative_prompt, latent_out, seed, cfg, steps, denoise, scaler, vae, width, height, latent_width, latent_height

    def generate_latent(self, width, height, latent_batch_size=1):
        latent = torch.zeros([latent_batch_size, 4, height // 8, width // 8], device=self.device)
        return {"samples":latent}
