import torch, torchvision
print(torch.__version__, torch.cuda.is_available())

#Check MMDetection installation
import mmdet

print(mmdet.__version__)

# # Check mmcv installation
from mmcv.ops import get_compiling_cuda_version, get_compiler_version
print(get_compiling_cuda_version())
print(get_compiler_version())
from mmdet.apis import inference_detector, init_detector, show_result_pyplot

def detection(img_path, out_path, thr, network):
        print('detection ' + str(network))
        thr = float(thr)
        config = 'mmdetection/configs/ssd/ssd300_coco.py'
        checkpoint = 'mmdetection/checkpoints/ssd300_coco_20200307-a92d2092.pth'
        if network == 'on':
                config = 'mmdetection/configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco.py'
                checkpoint = 'mmdetection/checkpoints/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth'
        model = init_detector(config, checkpoint, device='cpu')
        result = inference_detector(model, img_path)
        #res = show_result_pyplot(model, img_path, result, score_thr=0.3)
        # img = model.show_result(img_path, result, score_thr=0.3, thickness=1, show=False, out_file=out_path,
        #                         text_color='red', font_scale=1)
        model.show_result(
                img_path,
                result,
                score_thr=thr,
                show=False,
                out_file=out_path,
                wait_time=0,
                #fig_size=(15, 10),
                #win_name='result',
                bbox_color=(72, 101, 241),
                text_color=(72, 101, 241)
        )
