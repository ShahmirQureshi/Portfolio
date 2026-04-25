import os
import shutil
import random

# Paths to the image and label folders
image_folder = r"C:\Users\20MTE034\Downloads\data\images"
label_folder = r"C:\Users\20MTE034\Downloads\data\obj_train_data"

# Paths to save the new dataset structure
output_folder = r'D:\AI_Course\30DaycvChallenge\Day21\data'
images_output = os.path.join(output_folder, 'images')
labels_output = os.path.join(output_folder, 'labels')

# Create train and val folders
for subset in ['train', 'val']:
    os.makedirs(os.path.join(images_output, subset), exist_ok=True)
    os.makedirs(os.path.join(labels_output, subset), exist_ok=True)

# Get all image files and shuffle them for splitting
images = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
random.shuffle(images)

# Split dataset (80% train, 20% val)
train_split = int(0.8 * len(images))

train_images = images[:train_split]
val_images = images[train_split:]

def move_files(image_list, subset):
    for image_name in image_list:
        label_name = image_name.replace('.jpg', '.txt').replace('.png', '.txt')
        
        # Paths
        image_path = os.path.join(image_folder, image_name)
        label_path = os.path.join(label_folder, label_name)
        
        # Output paths
        image_dest = os.path.join(images_output, subset, image_name)
        label_dest = os.path.join(labels_output, subset, label_name)

        # Move files
        if os.path.exists(label_path):
            shutil.copy(image_path, image_dest)
            shutil.copy(label_path, label_dest)

# Move train and val sets
move_files(train_images, 'train')
move_files(val_images, 'val')

print(f"Train images: {len(train_images)}, Val images: {len(val_images)}")
