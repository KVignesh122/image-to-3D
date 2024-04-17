# 2D Image-to-3D Object conversion

[![GitHub Repo](https://img.shields.io/badge/GitHub-TripoSR-<black>?style=flat-square&logo=github)](https://github.com/VAST-AI-Research/TripoSR)

**_*This is a replication of VAST-AI-Research's TripoSR model and codebase (I have reorganised the code files to a more simple file structure, and created an easy-to-use UI using Tkinter.)_**

The aim of this project is to take in a 2D image file and convert it into a 3D object of file type .glb.

## Technical Info
 
The tool is built based on Stability.AI's TripoSR model [Advanced version of the Large Reconstruction Model], alongside various flavours of the u2net model for object segmentation and background removal.
 
### Enhancements made from base model:
* Reoriented final object to match the same direction of input image.
* Added functionality to convert clothing and only human beings present in image. [But the face of humans in 3D object is not great.]
* Improved efficiency of background removal model.
* Reduced output .glb filesize by 75% from original TripoSR model.
* Made .glb fileformat the default output file type and removed .obj format. [.obj fileformat does not store color info, so 3D objects are just the mesh with no colors.]

## How To Use
![image](https://github.com/KVignesh122/image-to-3D/assets/55841532/ee12db5f-2868-42fd-a9a5-0665afca2b31)

1. Download converter.exe.
2. Download model.ckpt and config.yaml files from [HuggingFace](https://huggingface.co/stabilityai/TripoSR/tree/main)
3. Store all three files in the SAME LOCATION on your computer.
4. Double click converter.exe to run the program. It will take roughly 2 mins to startup. Ignore all ONNX-related errors.
5. When the program window pops up, upload desired image file, and select the type of object in the image [Normal, Human Beingm or Clothing] you want to convert into a 3D Object.
6. Click the convert button, and wait 3-4 minutes. There will be info and log displayed in the Terminal window.
7. If "desired filename" field is not specified, the output 3D object file will be saved in same folder of the input 2D image. If specified, it will be saved in the same folder in which the .exe file is running from.
 
## Other tips:
- On average, it takes around 3-4 minutes to convert the image into 3D object, using local CPU alone.
- Download 3d viewer onto Windows to view the 3d object in your local file explorer: https://www.microsoft.com/store/productId/9NBLGGH42THS?ocid=pdpshare
- Use small and simple images that you feel might be great in 3D. The model is quite primitive so it can't handle complex images/objects or intricate patterns/textures. Pictures with solid color backgrounds behind the actual object in the image work best.
