import os
from glob import glob
from pathlib import Path
from ironpdf import PdfDocument

def find_ext(dr, ext):
  """
  get all file with extension ext in directory dr
  """
  return glob(os.path.join(dr,"*.{}".format(ext)))

# make new directories with pdf's filename in current directory as dirname
list_of_pdfs = find_ext('.', "pdf")
for filename in list_of_pdfs:
  dirname = filename.split('.')[1][1:]
  if not os.path.exists(dirname):
    os.makedirs(dirname)

workdir = "."
for each_path in os.listdir(workdir):
  if ".pdf" in each_path:
    print(each_path)
    try:
      pdf = PdfDocument.FromFile(each_path)
      # Extract all pages to a folder as image files
      pdf.RasterizeToImageFiles(f"{each_path[:-4]}/*.png",DPI=96)
    except:
      print(f"{each_path} failed")
