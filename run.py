import logging
import time

import numpy as np
import rembg
import torch
from PIL import Image
from rotate import rotate

from system import TSR
from utils import remove_background, resize_foreground

def convert_to_3d(image_path, output_filename='', isHuman=False, isCloth=False, cloth_cat=''):
    class Timer:
        def __init__(self):
            self.items = {}
            self.time_scale = 1000.0  # ms
            self.time_unit = "seconds"

        def start(self, name: str) -> None:
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            self.items[name] = time.time()
            logging.info(f"{name} ...")

        def end(self, name: str) -> float:
            if name not in self.items:
                return
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            start_time = self.items.pop(name)
            delta = time.time() - start_time
            t = delta * self.time_scale
            logging.info(f"{name} finished in {(t / 1000):.2f} {self.time_unit}.")

    timer = Timer()

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    if not torch.cuda.is_available():
        device = "cpu"
    else:
        device = "cuda:0"

    timer.start("Initializing model")
    model = TSR.from_pretrained(
        config_path="config.yaml",
        weight_path="model.ckpt"
    )

    model.renderer.set_chunk_size(10_000) # 0 for no chunking; default is 8192
    model.to(device)
    timer.end("Initializing model")

    timer.start("Removing background")
    if isHuman:
        rembg_session = rembg.new_session(model_name="u2net_human_seg")
    elif isCloth:
        rembg_session = rembg.new_session(model_name="u2net_cloth_seg")
    else:
        rembg_session = rembg.new_session()

    if isCloth and cloth_cat != '':
        image = remove_background(Image.open(image_path), rembg_session, cloth_category=cloth_cat)
    else:
        image = remove_background(Image.open(image_path), rembg_session)
    image = resize_foreground(image, 0.85)
    image = np.array(image).astype(np.float32) / 255.0
    image = image[:, :, :3] * image[:, :, 3:4] + (1 - image[:, :, 3:4]) * 0.5
    image = Image.fromarray((image * 255.0).astype(np.uint8))

    timer.end("Removing background")

    timer.start("Running model on image")
    with torch.no_grad():
        scene_codes = model([image], device=device)
    timer.end("Running model on image")

    timer.start("Extracting mesh")
    mesh = model.extract_mesh(scene_codes, resolution=256)[0]
    timer.end("Extracting mesh")
    
    timer.start("Rotating object")
    mesh = rotate(mesh)
    timer.end("Rotating object")
    
    timer.start("Saving generated object")
    if output_filename == '':
        output_filename = f"{image_path.split('.')[-2]}_out"
    mesh.export(f"{output_filename}.glb")
    timer.end("Saving generated object")
    
    return f"{output_filename}.glb"
