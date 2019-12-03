# Script for extracting 2D human pose from images
**Code Author: Shih-Yao (Mike) Lin**


## Features
+ Convert a video to images


## Dependencies
+ python3
+ glob2==0.6
+ opencv-python > 3.4.4.19

## Installation

* Clone this repo

```bash
git https://github.com/mikeshihyaolin/2d_pose_openpose.git
```
The directory tree should look like this:
```

```

* Install dependencies
```
pip3 install -r ./requirements.txt
```

## Usages
+ Step 1: convert a video to images (if necessary)
```
python video2img.py -i [video_path] -o [image_folder_path]  
```
+ Step 2: download and run openpose docker
	+ Step 2.1 pull docker
	```
	docker pull david800131s/openpose_t10_2:latest
	```



