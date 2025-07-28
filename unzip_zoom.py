import os
import subprocess
import shutil

# unzip the zoom images
large_dir = "./profile/gallery_large"

# find zip files in the large directory
zip_files = [f for f in os.listdir(large_dir) if f.endswith('.zip')]

for zip_file in zip_files:
    zip_path = os.path.join(large_dir, zip_file)
    try:
        subprocess.run(["unzip", "-o", zip_path, "-d", large_dir], check=True)
        print(f"Unzipped {zip_path} successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error unzipping {zip_path}: {e}")
