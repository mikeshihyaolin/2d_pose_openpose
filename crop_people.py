#author: Shih-Yao (Mike) Lin
#email: mike.lin@ieee.org
#date: 2019-12-04
#input: image folder path & kjson folder path 
#output: cropped images with zero padding boundary (all the person in the image will be located at the center of each image)
#usage: python3 crop_people.py -i [image path] -j [kjson path] -o [output image path]

import glob
import argparse
import numpy as np
import os, sys
from os import listdir, makedirs
import os,json
import shutil
import cv2

import statistics

POSDIM = 25
FACEDIM = 70
HANDDIM = 21
fix_size = 500

def reset(reset_path):
    path = reset_path
    if os.path.isdir(path):
        shutil.rmtree(path)
        makedirs(path)
    else:
        makedirs(path)

def load_pose_keypoints_2d(kjson_file):
	keypoint = []
	with open(kjson_file) as jf:
		dataDict = json.load(jf)
		people = dataDict.get("people")
		if type(dataDict) is dict and type(people) is list and len(people)>0:
			for person in people:
				a = np.asarray(person["pose_keypoints_2d"]).reshape((POSDIM,3))
				keypoint.append(a)
	return keypoint


def find_bbox_and_center(keypoints, img_w, img_h):

	x = []
	y = []
	c = 0
	padding_w = 50

	bbox = []
	center = []

	print(keypoints)
	print(keypoints[0])

	for  i in range(POSDIM):

		if keypoints[0][i][0] > 0 and keypoints[0][i][1] > 0:
			x.append(int(keypoints[0][i][0]))
			y.append(int(keypoints[0][i][1]))

	if x != [] and y != [] and len(x)>16 and len(y)>16 :
		c_x = int(statistics.median(x))
		c_y = int(statistics.median(y))
		center = (c_x, c_y)

		b_x_0 = int(min(x))-padding_w
		b_x_1 = int(max(x))+padding_w
		b_y_0 = int(min(y))-padding_w
		b_y_1 = int(max(y))+padding_w

		if b_x_0 < 0:
			b_x_0 = 0
		if b_x_1 >img_w:
			b_x_1 = img_w
		if b_y_0 < 0:
			b_y_0 = 0
		if b_y_1 > img_h:
			b_y_1 = img_h

		bbox = [(b_x_0, b_y_0), (b_x_1, b_y_1)]

	return center, bbox

def preprocessing(input_img_folder, input_keypoint_folder, output_folder):

	# parameters setting
	radius = 10
	color = (0, 0, 255)
	thickness = -1

	reset(output_folder)

	img_list = sorted(glob.glob(input_img_folder+"/*"))
	print("image files: "+ str(len(img_list)))
	keypoint_list = sorted(glob.glob(input_keypoint_folder+"/*"))
	print("kjson files: " +str(len(keypoint_list)))

	for i, _ in enumerate(img_list):

		img = cv2.imread(img_list[i])
		keypoint = load_pose_keypoints_2d(keypoint_list[i])

		img_w = len(img[0])
		img_h = len(img)

		# calculate bbox and bbox center
		center, bbox = find_bbox_and_center(keypoint, img_w, img_h)

		if bbox != []:
			img_copy = img.copy()
			cv2.circle(img_copy, center, radius, color, thickness) 
			cv2.rectangle(img_copy, bbox[0], bbox[1], (0,255,0), 2)
			cv2.imwrite(output_folder+"/_bbox_%04d.jpg"%i,img_copy)

		# resize image
		resized_img = img.copy()
		resized_img = img[bbox[0][1]:bbox[1][1],bbox[0][0]:bbox[1][0] ]
		w = len(resized_img[0])
		h = len(resized_img)
		new_w = int(fix_size * w /h)
		new_h = fix_size

		if new_w % 2 == 1:
			new_w += 1
		resized_img = cv2.resize(resized_img, (new_w, new_h), interpolation = cv2.INTER_AREA)
		# cv2.imwrite(output_folder+"/_resize_%04d.jpg"%i,resized_img)

		# zero padding
		blank_image = np.zeros(shape=[fix_size, fix_size, 3], dtype=np.uint8)
		blank_center = int(fix_size/2)
		x_s = int(blank_center-new_w/2)
		x_e = int(blank_center+new_w/2)
		y_s = 0
		y_e = fix_size

		new_bbox = (x_s, x_e, y_s, y_e)
		blank_image[y_s:y_e,x_s:x_e] = resized_img[0:new_h, 0:new_w]
		cv2.imwrite(output_folder+"/res_%04d.jpg"%i,blank_image)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_img_folder", type=str,default="./res/img/")
parser.add_argument("-j", "--input_keypoint_folder", type=str,default="./res/kjson/")
parser.add_argument("-o", "--output_folder", type=str, default="./res/crop/")

args = parser.parse_args()

preprocessing(args.input_img_folder, args.input_keypoint_folder, args.output_folder)
