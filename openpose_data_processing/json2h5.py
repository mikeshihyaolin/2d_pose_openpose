# -*-coding:utf-8-*-
# @file   read_json.py
# @author Shih-Yao (Mike) Lin
# @email  mike.lin@ieee.org
# @date   2019-11-22
# @brief  read openpose json files and convert them to h5 files
# @usage  python json2h5.py --input_json [json_path] --output_h5_path [h5_path]    


import json
import glob
import argparse
import h5py
import numpy as np

def json2h5(input_json, output_h5):

	jfiles = sorted(glob.glob(input_json+"/*.json"))

	for i, _ in enumerate(jfiles):

		file_name = jfiles[i]
		file_name = file_name.replace(".json","")
		file_name = file_name.replace(input_json,"")
		print(file_name)

		with open(jfiles[i],'r') as f:
			data = json.load(f)
			person = data['people']
			body = person[0]["pose_keypoints_2d"]
			face = person[0]["face_keypoints_2d"]
			left_hand = person[0]["hand_left_keypoints_2d"]
			right_hand = person[0]["hand_right_keypoints_2d"]

		h5f = h5py.File(output_h5+"/"+file_name+".h5", 'w')

		h5f.create_dataset('body', data=body)
		h5f.create_dataset('face', data=face)
		h5f.create_dataset('left_hand', data=left_hand)
		h5f.create_dataset('right_hand', data=right_hand)
		h5f.close()

		hf = h5py.File(output_h5+"/"+file_name+".h5", 'r')
		data = hf['body']
		print(data)
		keypoint_list = []
		for j, keypoint in enumerate(data):
			keypoint_list.append(keypoint)
			print(keypoint)
		

parser = argparse.ArgumentParser()
parser.add_argument("--input_json_folder","-i", type=str, default="/Users/shihyaolin/Desktop/res/json/")
parser.add_argument("--output_h5_folder", "-o", type=str, default="/Users/shihyaolin/Desktop/res/")
args = parser.parse_args()

json2h5(args.input_json_folder, args.output_h5_folder)





