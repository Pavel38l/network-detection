FROM python:3
#FROM python:3.6

# Grab requirements.txt.

# Install dependencies

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

#ADD ./webapp /usr/src/webapp/
ADD ./app /usr/src/app
#WORKDIR /usr/src/webapp
WORKDIR /usr/src/app
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

#RUN pip install torch==1.7.1+cpu torchvision==0.8.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install mmcv-full==1.2.6 -f https://download.openmmlab.com/mmcv/dist/cpu/torch1.7.0/index.html
RUN git clone https://github.com/open-mmlab/mmdetection.git

WORKDIR /usr/src/app/mmdetection
RUN git reset --hard f07de13b82b746dde558202f720ec2225f276d73
RUN pip install -r requirements/build.txt
RUN pip install -v -e .
#RUN mkdir checkpoints
# Mask-RCNN weights
#RUN wget -c https://open-mmlab.s3.ap-northeast-2.amazonaws.com/mmdetection/v2.0/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth -O checkpoints/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth
# SSD weights
RUN wget -c http://download.openmmlab.com/mmdetection/v2.0/ssd/ssd300_coco/ssd300_coco_20200307-a92d2092.pth -O checkpoints/ssd300_coco_20200307-a92d2092.pth
WORKDIR /usr/src/app

CMD gunicorn --bind 0.0.0.0:$PORT main