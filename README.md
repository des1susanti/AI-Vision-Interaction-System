# Computer Vision & Interaction System
**Desi Susanti** | *Python Developer & Computer Vision Enthusiast*

This repository features a collection of modules focused on developing intelligent interaction systems using Computer Vision. The project demonstrates the practical implementation of real-time object detection and motion tracking, enhanced with custom optimization logic.

## 📊 Project Status & Proficiency Level
* **Difficulty:** Beginner to Intermediate
* **Model Status:** **Pre-trained** (Leveraging YOLOv8 & MediaPipe)
* **Focus:** Implementation of post-detection logic to enhance visual data relevance and classification accuracy.

## 📁 Project Structure

### 1. [Virtual Paint System](./01_Virtual_Paint)
A touchless interaction system utilizing **MediaPipe** for 3D hand tracking.
* **Core Feature:** Enables users to draw in a virtual space (air) via camera input in an interactive and fluid manner.
* **Technical Detail:** Implements landmark detection to map fingertip coordinates into dynamic graphical inputs within OpenCV.

### 2. [Real-time Object Detection with Logic Optimization](./02_Object_Detection)
An object detection implementation based on **YOLOv8**, optimized with post-detection algorithms for higher classification precision.
* **Heuristic Spatial Filtering:** Integrates geometry-based logic (pixel dimensions and aspect ratios) to mitigate misclassification of visually similar objects. Example: Validating the distinction between a *Smartwatch* and a *Cell Phone* based on spatial bounding box scales.
* **Contextual Label Mapping:** A mechanism to transform standard labels (COCO Dataset) into more specific and functional terminology, such as converting *Bottle* to *Tumbler* or *Toothbrush* to *Pen*.

## 🛠️ Technology Stack
* **Language:** Python 3.x
* **Frameworks:** OpenCV, Ultralytics (YOLOv8), MediaPipe
* **Version Control:** Git & GitHub

## 🚀 Getting Started

Follow these steps to set up the project locally:

### 1. Clone the Repository
Clone this project to your local machine using the command below:
```bash
git clone [https://github.com/des1susanti/AI-Vision-Interaction-System.git](https://github.com/des1susanti/AI-Vision-Interaction-System.git)