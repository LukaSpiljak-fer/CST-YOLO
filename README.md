# CST-YOLO for Blood Cell Detection
This repository contains the implementation and experimentation of improved variants of the CST-YOLO model for automated detection and classification of blood cells in microscopic images. The project is part of a study on optimizing object detection networks for medical imaging, specifically focusing on red blood cells (RBC), white blood cells (WBC), and platelets.

# Project Overview
This project is an attempt, results and overview of optimizing a computer vision model for blood cell detection and classification.  

CST-YOLO is a hybrid architecture combining:  
YOLOv7's real-time object detection capabilities  
CNN-SWIN Transformer (CST) for improved detection of small and overlapping objects  

In this repository, several optimized variants of CST-YOLO are proposed to improve inference speed while maintaining accuracy:  
MCS2 and MCS3 (reduced complexity of MCS module)  
WELAN3 and WELAN4 (simplified Weighted ELAN modules)  

# Datasets Used
Three publicly available datasets were used:  
BCCD, CBC, BCD  

The images are labeled into three classes:  
Red Blood Cells (RBC), White Blood Cells (WBC) and Platelets  

# Model Variants
Model	Params    GFLOPS   mAP@.5   Inference Time  Notes  
CST-YOLO  100%  235.4    0.733    14.47 ms        Baseline  
MCS2      95.9% 156.1    0.699    14.20 ms        Fastest variant  
MCS3      95.9%	168.4    0.735    14.25 ms        Best precision-speed tradeoff  
WELAN3    94.8%	223.3    0.717    13.69 ms        Best platelet detection  
WELAN4    89.1%	226.9    0.748    13.80 ms        Highest accuracy  

# Key Contributions
Introduced and evaluated four optimized versions of CST-YOLO.  
Introduced new modules MCS2 and W-ELAN3.  

# Links
- original work:  
[CST-YOLO Paper (PDF)](https://arxiv.org/pdf/2306.14590v2)  
[CST-YOLO by mkang315 (Original Repo)](https://github.com/mkang315/CST-YOLO)  
- datasets:  
[BCCD dataset](https://github.com/Shenggan/BCCD_Dataset)  
[BCD dataset](https://paperswithcode.com/dataset/blood-cell-detection-dataset-1)  
[CBC dataset](https://github.com/MahmudulAlam/Complete-Blood-Cell-Count-Dataset)  
