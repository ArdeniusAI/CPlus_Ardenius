"""
@author: initials AMA
@title: Ardenius
@nickname: Ardenius
@description: CPlus control box is designed to gather workflow variables into 1 node.
"""
#  this software and code © 2024 initals AMA nickname Ardenius is licensed under GPL V3.0 
#  ( author contact information ardenius7@gmail.com attribution link https://ko-fi.com/ardenius )
#  ➡️ follow me at https://ko-fi.com/ardenius on the top right corner (follow)
#  📸 Change the mood ! by Visiting my AI Image Gallery
#  🏆 Premium Memebers only Perks (Premium SD Models, ComfyUI custom nodees, and more to come)
#  the below code is in part or in full based upon ComfyUI code licensed under General Public License v3.0 https://www.gnu.org/licenses/gpl-3.0.txt by
#  contributers found here https://github.com/comfyanonymous/ComfyUI

from .CPlus_control_box import Control_Box


NODE_CLASS_MAPPINGS = {
    "Control_Box": Control_Box,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Control_Box": "CPlus Control Box",
}


