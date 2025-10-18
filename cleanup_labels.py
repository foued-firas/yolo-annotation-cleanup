import os
import os.path

# Paths - using raw strings for Windows paths
images_dir = r'' # path of images
labels_dir = r'' # path of labels

print("Cleaning empty label files...")

empty_count = 0
for label_file in os.listdir(labels_dir):
    if label_file.endswith('.txt'):
        label_path = os.path.join(labels_dir, label_file)
        
        # Check if file is empty or has no valid bounding boxes
        if os.path.getsize(label_path) == 0:
            # Remove empty label file
            os.remove(label_path)
            
            # Also remove corresponding image file if it exists
            image_name = os.path.splitext(label_file)[0] + '.jpg'
            image_path = os.path.join(images_dir, image_name)
            
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"Removed: {label_file} and {image_name}")
            else:
                # Try other image extensions
                for ext in ['.png', '.jpeg', '.JPG', '.jpeg']:
                    image_path = os.path.join(images_dir, os.path.splitext(label_file)[0] + ext)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                        print(f"Removed: {label_file} and {os.path.basename(image_path)}")
                        break
                else:
                    print(f"Removed: {label_file} (no corresponding image found)")
            
            empty_count += 1

print(f"✅ Cleanup complete! Removed {empty_count} empty label files and their images.")