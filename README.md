# CST-YOLO for Blood Cell Detection
This repository contains the implementation and experimentation of improved variants of the CST-YOLO model for automated detection and classification of blood cells in microscopic images. The project is part of a study on optimizing object detection networks for medical imaging, specifically focusing on red blood cells (RBC), white blood cells (WBC), and platelets.

# Project Overview
This project is an attempt, results and overview of optimizing a computer vision model for blood cell detection and classification.  

CST-YOLO is a hybrid architecture combining:  
- YOLOv7's real-time object detection capabilities  
- CNN-SWIN Transformer (CST) for improved detection of small and overlapping objects  

In this repository, several optimized variants of CST-YOLO are proposed to improve inference speed while maintaining accuracy:  
- MCS2 and MCS3 (reduced complexity of MCS module)  
- WELAN3 and WELAN4 (simplified Weighted ELAN modules)  

# Datasets Used
Three publicly available datasets were used:  
BCCD, CBC, BCD  

The images are labeled into three classes:  
Red Blood Cells (RBC), White Blood Cells (WBC) and Platelets  

# Model Variants
| Model   | Params | GFLOPS | mAP@.5 | Inference Time | Notes                         |
|---------|--------|--------|--------|----------------|-------------------------------|
| CST-YOLO | 100%  | 235.4  | 0.733  | 14.47 ms       | Baseline                      |
| MCS2     | 95.9% | 156.1  | 0.699  | 14.20 ms       | Fastest variant               |
| MCS3     | 95.9% | 168.4  | 0.735  | 14.25 ms       | Best precision-speed tradeoff |
| WELAN3   | 94.8% | 223.3  | 0.717  | 13.69 ms       | Best platelet detection       |
| WELAN4   | 89.1% | 226.9  | 0.748  | 13.80 ms       | Highest accuracy              |

# Key Contributions
Introduced and evaluated four optimized versions of CST-YOLO.  
Introduced new modules MCS2 and W-ELAN3.  

# Installation
Install requirements.txt with recommended dependencies Python >= 3.8 environment including Torch <= 1.7.1 and CUDA <= 11.1:  
`pip install -r requirements.txt`
  
**Training**  
The hyperparameter setting file is hyp.scratch.p5.yaml in the directory ./data/.  

Single GPU training:  
`python train.py --workers 2 --project /app/output --epochs 100 --device 0 --data data/all.yaml --cfg cfg/training/cst-yolo.yaml --name cstyolo` 

Multiple GPU training:  
`python -m torch.distributed.launch --nproc_per_node 4 --master_port 9527 train.py --workers 2 --device 0,1,2,3 --sync-bn --batch-size 128 --data data/all.yaml --img 640 640 --cfg cfg/training/cst-yolo.yaml --weights '' --name cst-yolo --hyp data/hyp.scratch.p5.yaml`

**Testing**
`python test.py --data data/alltesst.yaml --img 640 --batch 32 --conf 0.001 --iou 0.65 --device 0 --weights output/model/weights/best.pt --name test`

**Single image detection**
`python detect.py --weights output/cstyolo/weights/best.pt \
--source datasets/all/test/images/BloodImage_00137bccd.jpg \
--conf-thres 0.287 --device 0 --project cstyolodevs --name MCS2`

**Multiple model comparison**
`python deviations.py --weights output/model1/weights/best.pt output/model2/weights/best.pt output/model3/weights/best.pt --data data/alltest.yaml --conf-thres-list 0.6 conf2 conf3 --device 0 --labels-dir datasets/all/test/labels`

# Links
- original work:  
[CST-YOLO Paper (PDF)](https://arxiv.org/pdf/2306.14590v2)  
[CST-YOLO by mkang315 (Original Repo)](https://github.com/mkang315/CST-YOLO)  
- datasets:  
[BCCD dataset](https://github.com/Shenggan/BCCD_Dataset)  
[BCD dataset](https://paperswithcode.com/dataset/blood-cell-detection-dataset-1)  
[CBC dataset](https://github.com/MahmudulAlam/Complete-Blood-Cell-Count-Dataset)  
