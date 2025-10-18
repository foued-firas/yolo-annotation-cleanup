# YOLO Dataset Cleaner

A Python utility tool to automatically clean and synchronize YOLO format datasets by removing empty label files and their corresponding images.

##  Features

- **Automated Cleanup**: Removes empty `.txt` label files from YOLO datasets
- **Image Synchronization**: Deletes corresponding image files to maintain dataset consistency
- **Multi-format Support**: Handles various image formats (JPG, PNG, JPEG)
- **Safe Operations**: Verifies file existence before deletion
- **Progress Tracking**: Provides detailed output of cleanup operations

##  Project Structure
yolo-dataset-cleaner/
├── yolo-annotation-cleanup.py
├── README.md

## 🛠️ Installation

```bash
git clone https://github.com/foued-firas/yolo-annotation-cleanup.git
cd yolo-annotation-cleanup
