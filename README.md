# Script for extracting 2D human pose from images
**Code Author: Shih-Yao (Mike) Lin**

## Features
+ Convert a video to images
+ Extract 2D human pose from 2D RGB images by using Openpose 
+ Convert the extracted Json files (body keypoints) into h5 files

## Dependencies
+ python3
+ glob2
+ opencv-python 
+ docker

## Installation

* Clone this repo

```bash
git https://github.com/mikeshihyaolin/2d_pose_openpose.git
```
The directory tree should look like this:
```
${ROOT}
├── README.md
├── openpose_data_processing
│   ├── img2h5.py
│   └── json2h5.py
├── requirements.txt
└── video2img.py
```

* Install dependencies
```
pip3 install -r ./requirements.txt
```

## Usages
1. convert a video to images 
```
python video2img.py -i [video_path] -o [image_folder_path]  
```
2. download and run openpose docker
	1. pull docker
	```
	docker pull david800131s/openpose_t10_2:latest
	```
	2. run openpose
	```
	/openpose/build/examples/openpose/openpose.bin --image_dir /data/img --write_json /data/json/ --write_images /data/img/ --display 0 --face --hand 
	```

3. convert and save json files to h5 files (optional)
```
python ./openpose_data_processing/json2h5.py -i [json folder] -o [output_h5_path]
```



