from pathlib import Path
import json
import shutil
from datetime import datetime

class LabelImageSync:
    
    
    def __init__(self, images_folder, labels_folder, backup=True):
      
        self.images_folder = Path(images_folder)
        self.labels_folder = Path(labels_folder)
        self.backup = backup
        self.backup_folder = None
        
        if backup:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.backup_folder = Path(f"labels_backup_{timestamp}")
            self.backup_folder.mkdir(exist_ok=True)
        
        # Supported formats
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'}
        self.label_extensions = {'.txt', '.xml', '.json', '.yaml', '.yml'}
    
    def get_image_files(self):
        """Get all image files from the images folder."""
        image_files = {}
        for ext in self.image_extensions:
            for img_path in self.images_folder.glob(f"*{ext}"):
                # Store without extension as key
                image_files[img_path.stem] = img_path
            for img_path in self.images_folder.glob(f"*{ext.upper()}"):
                image_files[img_path.stem] = img_path
        return image_files
    
    def get_label_files(self):
        """Get all label files from the labels folder."""
        label_files = {}
        for ext in self.label_extensions:
            for label_path in self.labels_folder.glob(f"*{ext}"):
                label_files[label_path.stem] = label_path
            for label_path in self.labels_folder.glob(f"*{ext.upper()}"):
                label_files[label_path.stem] = label_path
        return label_files
    
    def sync_labels(self, delete_orphaned=True, report_only=False):
        
        print("=" * 80)
        print("LABEL-IMAGE SYNCHRONIZATION")
        print("=" * 80)
        print(f"Images folder: {self.images_folder}")
        print(f"Labels folder: {self.labels_folder}")
        print(f"Mode: {'REPORT ONLY' if report_only else 'DELETE MODE'}\n")
        
        # Get all files
        image_files = self.get_image_files()
        label_files = self.get_label_files()
        
        print(f"Total images found: {len(image_files)}")
        print(f"Total labels found: {len(label_files)}\n")
        
        # Find labels with corresponding images
        matched_labels = []
        orphaned_labels = []
        
        for label_name, label_path in label_files.items():
            if label_name in image_files:
                matched_labels.append((label_name, label_path, image_files[label_name]))
            else:
                orphaned_labels.append((label_name, label_path))
        
        # Find images without labels
        images_without_labels = []
        for img_name, img_path in image_files.items():
            if img_name not in label_files:
                images_without_labels.append((img_name, img_path))
        
        # Print statistics
        print("=" * 80)
        print("SYNCHRONIZATION RESULTS")
        print("=" * 80)
        print(f"✓ Labels with matching images: {len(matched_labels)}")
        print(f"✗ Orphaned labels (no image): {len(orphaned_labels)}")
        print(f"⚠ Images without labels: {len(images_without_labels)}\n")
        
        # Show orphaned labels
        if orphaned_labels:
            print("=" * 80)
            print("ORPHANED LABELS (will be deleted):")
            print("=" * 80)
            for idx, (name, path) in enumerate(orphaned_labels, 1):
                print(f"{idx:4d}. {path.name}")
            print()
        
        # Show images without labels
        if images_without_labels:
            print("=" * 80)
            print("IMAGES WITHOUT LABELS (labels will be kept if they exist):")
            print("=" * 80)
            for idx, (name, path) in enumerate(images_without_labels[:20], 1):
                print(f"{idx:4d}. {path.name}")
            if len(images_without_labels) > 20:
                print(f"... and {len(images_without_labels) - 20} more")
            print()
        
        # Delete orphaned labels if requested
        deleted_count = 0
        if delete_orphaned and orphaned_labels and not report_only:
            print("=" * 80)
            print("DELETING ORPHANED LABELS")
            print("=" * 80)
            
            for name, label_path in orphaned_labels:
                try:
                    # Backup if enabled
                    if self.backup:
                        backup_path = self.backup_folder / label_path.name
                        shutil.copy2(label_path, backup_path)
                    
                    # Delete the label
                    label_path.unlink()
                    deleted_count += 1
                    print(f"✗ Deleted: {label_path.name}")
                except Exception as e:
                    print(f"✗ Error deleting {label_path.name}: {e}")
            
            print(f"\n✓ Deleted {deleted_count} orphaned labels")
            if self.backup:
                print(f"✓ Backup saved to: {self.backup_folder}")
        
        # Return statistics
        stats = {
            'total_images': len(image_files),
            'total_labels': len(label_files),
            'matched_labels': len(matched_labels),
            'orphaned_labels': len(orphaned_labels),
            'images_without_labels': len(images_without_labels),
            'deleted_labels': deleted_count
        }
        
        return stats
    
    def generate_report(self, stats):
        """Generate a detailed text report."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = Path(f"label_sync_report_{timestamp}.txt")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("LABEL-IMAGE SYNCHRONIZATION REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Images Folder: {self.images_folder}\n")
            f.write(f"Labels Folder: {self.labels_folder}\n\n")
            
            f.write("SUMMARY\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Images: {stats['total_images']}\n")
            f.write(f"Total Labels: {stats['total_labels']}\n")
            f.write(f"Matched (Image + Label): {stats['matched_labels']}\n")
            f.write(f"Orphaned Labels (No Image): {stats['orphaned_labels']}\n")
            f.write(f"Images Without Labels: {stats['images_without_labels']}\n")
            f.write(f"Labels Deleted: {stats['deleted_labels']}\n\n")
            
            # Calculate percentages
            if stats['total_labels'] > 0:
                match_rate = (stats['matched_labels'] / stats['total_labels']) * 100
                f.write(f"Match Rate: {match_rate:.1f}%\n")
        
        print(f"\n📄 Report saved to: {report_path}")
        return report_path
    
    def validate_dataset(self):
        
        print("\n" + "=" * 80)
        print("DATASET VALIDATION")
        print("=" * 80)
        
        issues = []
        
        # Check if folders exist
        if not self.images_folder.exists():
            issues.append(f" Images folder not found: {self.images_folder}")
        else:
            print(f"✓ Images folder exists: {self.images_folder}")
        
        if not self.labels_folder.exists():
            issues.append(f" Labels folder not found: {self.labels_folder}")
        else:
            print(f"✓ Labels folder exists: {self.labels_folder}")
        
        # Check if folders are empty
        image_files = self.get_image_files()
        label_files = self.get_label_files()
        
        if len(image_files) == 0:
            issues.append(" No images found in images folder")
        else:
            print(f"✓ Found {len(image_files)} images")
        
        if len(label_files) == 0:
            issues.append(" No labels found in labels folder")
        else:
            print(f"✓ Found {len(label_files)} labels")
        
        # Print issues
        if issues:
            print("\n  ISSUES FOUND:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("\n✓ No issues found")
        
        return len(issues) == 0


def main():
    """Main function with example usage."""
    
    # Configuration
    IMAGES_FOLDER = r""          # Folder with images
    LABELS_FOLDER = r""          # Folder with labels
    
    # Initialize synchronizer
    sync = LabelImageSync(
        images_folder=IMAGES_FOLDER,
        labels_folder=LABELS_FOLDER,
        backup=True  # Set to False to disable backup (NOT RECOMMENDED)
    )
    
    # Validate dataset first
    print("Validating dataset structure...\n")
    is_valid = sync.validate_dataset()
    
    if not is_valid:
        print("\n Please fix the issues above before continuing.")
        return
    
    # Automatically delete orphaned labels
    print("\n" + "=" * 80)
    print("AUTOMATIC DELETION MODE")
    print("=" * 80)
    stats = sync.sync_labels(delete_orphaned=True, report_only=False)
    
    # Generate report
    sync.generate_report(stats)
    
    print("\n✓ Synchronization complete!")
    print(f"✓ Deleted {stats['deleted_labels']} orphaned labels")
    print(f"✓ Kept {stats['matched_labels']} labels with matching images")


if __name__ == "__main__":
    # Example 1: Basic usage
    print("Example 1: Basic Synchronization\n")
    main()
    
   