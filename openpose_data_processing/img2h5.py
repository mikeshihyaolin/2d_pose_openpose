# -*-coding:utf-8-*-
# @file   img2h5.py
# @author Shih-Yao (Mike) Lin
# @email  mike.lin@ieee.org
# @date   2019-11-22
# @brief  read images and convert them to h5 files
# @usage  python img2h5.py --input_img [json_path] --output_h5_path [h5_path]    

import cv2
import glob
import argparse
import h5py
import numpy as np

def img2h5(input_img, folder_name, output_h5):

	img_files = sorted(glob.glob(input_img+"/*"))

	img_list = []

	for i, _ in enumerate(img_files):

		img = cv2.imread(img_files[i])
		img = cv2.resize(img, (320,320), interpolation=cv2.INTER_CUBIC)
		img_list.append(img)

	h5f = h5py.File(output_h5+"/"+folder_name+".h5", 'w')

	h5f.create_dataset(name='images', data=img_list, compression="gzip",)
	# h5f.close()
		
parser = argparse.ArgumentParser()
parser.add_argument("--input_img_folder","-i", type=str, default="/Users/shihyaolin/Desktop/res/img/")
parser.add_argument("--input_folder_name","-f", type=str, default="img")
parser.add_argument("--output_h5_folder", "-o", type=str, default="/Users/shihyaolin/Desktop/res/")
args = parser.parse_args()

img2h5(args.input_img_folder, args.input_folder_name, args.output_h5_folder)





