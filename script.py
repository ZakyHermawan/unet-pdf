from pypdf import PdfReader
from pathlib import Path
import os
import cv2
from glob import glob

def find_ext(dr, ext):
    """
    get all file with extension ext in directory dr
    """
    return glob(os.path.join(dr,"*.{}".format(ext)))

def remove_empty_dirs(path):
    for root, dirnames, filenames in os.walk(path, topdown=False):
        for dirname in dirnames:
            remove_empty_dir(os.path.realpath(os.path.join(root, dirname)))

# # make new directories with pdf's filename in current directory as dirname
list_of_pdfs = find_ext('.', "pdf")
dirnames = []
for filename in list_of_pdfs:
  dirname = filename.split('.')[1][1:]
  dirnames.append(dirname)
  # make output dirs
  if not os.path.exists(f"ext_{dirname}"):
    os.makedirs(f"ext_{dirname}")

detector = cv2.FaceDetectorYN.create('face_detection_yunet_2023mar.onnx', "", (320, 320))

"""
get images from each pdf files
if the image contain face, then write the image
"""
for dirname in dirnames:
   print(dirname)
   image_names = os.listdir(dirname)
   for image_name in image_names:
      im = cv2.imread(f"{dirname}/{image_name}")
      channels = 1 if len(im.shape) == 2 else  im.shape[2]

      img_W = int(im.shape[1])
      img_H = int(im.shape[0])

      detector.setInputSize((img_W, img_H))
      if channels % 3 != 0:
        continue

      _, faces = detector.detect(im)
      faces = faces if faces is not None else []

      # just check if image contains face, then just write the original image
      if len(faces):
        cv2.imwrite(f"ext_{dirname}/{image_name}", im)

for p in Path(".").glob('**/*'):
    if p.is_dir() and len(list(p.iterdir())) == 0:
        os.removedirs(p)
