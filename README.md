# Script for estimating 2D human pose from RGB images by using Openpose
**Code Author: Shih-Yao (Mike) Lin**

![](figs/demo2.gif)

## Features
+ Convert a video to images
+ Extract 2D human pose from 2D RGB images by using Openpose 
+ Convert the extracted Json files (body keypoints) into h5 files

## Dependencies
+ python3, glob2, opencv-python, ffmpeg, docker

## Installation

* Clone this repo

```bash
git https://github.com/mikeshihyaolin/2d_pose_openpose.git
```
The directory tree:
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
	+ dependencies
	```
	pip3 install -r ./requirements.txt
	```
	+ docker
	```
	sudo snap install docker
	```


## Usages
1. convert a video to images 
```
python video2img.py -i [video_path] -o [image_folder_path]  
```
2. download and run openpose docker
	0. pull a openpose docker
	```
	sudo docker pull wenwu449/openpose
	```
	1. run docker
	```
	docker run --runtime=nvidia --rm -e DISPLAY=$DISPLAY -v [data folder]:/data/ -v [results folder]:/res/  -w /openpose/ -it  1a739316c6a7 bash  
	```
	2. run openpose
	```
	/openpose/build/examples/openpose/openpose.bin --image_dir /data/ --write_json /res/json/ --write_images /res/img/ --display 0 --face --hand 
	```

3. convert and save json files to h5 files (optional)
```
python ./openpose_data_processing/json2h5.py -i [json folder] -o [output_h5_path]
```
4. crop images to make the detected person in the center of images (optional)



