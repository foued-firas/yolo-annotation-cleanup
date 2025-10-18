# YOLO Dataset Manager

A comprehensive Python toolkit for managing and cleaning YOLO format datasets. Includes utilities for synchronizing images with labels and removing empty annotation files.

##  Features

###  Label-Image Synchronizer (`label_sync.py`)
- **Smart Synchronization**: Automatically matches images with their corresponding labels
- **Multi-format Support**: Handles various image (JPG, PNG, BMP, etc.) and label (TXT, XML, JSON, etc.) formats
- **Safe Backup**: Creates automatic backups before deletion operations
- **Detailed Reporting**: Generates comprehensive synchronization reports
- **Dataset Validation**: Validates dataset structure before processing

###  Empty Label Cleaner (`cleanup_labels.py`)
- **Automatic Cleanup**: Removes empty YOLO label files (.txt)
- **Image Synchronization**: Deletes corresponding images to maintain dataset consistency
- **Multi-format Image Support**: Handles JPG, PNG, JPEG, JPG extensions
- **Progress Tracking**: Provides detailed operation logs

##  Project Structure
yolo-dataset-manager/
├── label_sync.py # Main synchronization utility
├── cleanup_labels.py # Empty label cleaner
└── README.md

## 🛠️ Installation

```bash
git clone https://github.com/foued-firas/yolo-dataset-manager.git
cd yolo-dataset-manager

⚙️ Requirements
Python 3.6+

No external dependencies (uses only built-in modules)

🔧 Configuration
Supported Image Formats
.jpg, .jpeg, .png, .bmp, .gif, .webp, .tiff

Supported Label Formats
.txt (YOLO), .xml (Pascal VOC), .json (COCO), .yaml, .yml

🤝 Contributing
Contributions are welcome! Please feel free to submit issues and pull requests.
