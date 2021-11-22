import struct
import numpy as np
from PIL import Image
from pathlib import Path
import os
import shutil
import traceback
import sys

def run():
    # check if run from script or excutable
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    elif __file__:
        os.chdir(os.path.dirname(__file__))
    # directory structure prparation
    input_dir = 'input'
    output_dir = 'output'
    tmp_dir = 'tmp'
    assert os.path.exists(input_dir)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)
    # get list of .jpg files from input directory
    file_list = list(filter(lambda x:x.endswith((".jpg", ".JPG")), os.listdir(input_dir)))
    # iterate over files
    for file_name in file_list:
        # get temporary raw byte file by DJI Thermal SDK
        os.system(  f"dji_irp.exe -a measure \
                    --measurefmt float32 \
                    -s input\{file_name} -o tmp\{file_name}.raw")
        # get image size
        img = Image.open(f"input\{file_name}")
        size = img.size
        # decode temporary byte file to tiff
        arr = np.zeros(size[0]*size[1])
        with open(f"tmp\{file_name}.raw", "rb") as f:
            data = f.read()
            format = '{:d}f'.format(len(data)//4)
            arr=np.array(struct.unpack(format, data))
        arr = arr.reshape(size[1],size[0])
        im = Image.fromarray(arr)
        im.save(f"output\{file_name}.tiff")
        # copy exif data from original file to new tiff
        os.system(f"exiftool.exe -tagsfromfile input\{file_name} output\{file_name}.tiff -overwrite_original_in_place")

if __name__ == '__main__':
    try:
        run()
        print("Success!")
        input("Press Enter to continue...")
    except Exception:
        traceback.print_exc()
        input("Press Enter to continue...")