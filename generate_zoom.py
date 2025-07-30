import os
import subprocess
import shutil

large_dir = "./profile/gallery_large"

# generate dzi files from large images using vips
thumb_dir = os.path.join(large_dir, "thumbnails")
thumb_size = 400
tile_size = 1024

os.makedirs(thumb_dir, exist_ok=True)
valid_images = ('.png', '.jpg', '.webp', '.avif')
valid_zoomable = ('dzi')

for filename in os.listdir(large_dir):
    if filename.lower().endswith(valid_images):
        name, ext = os.path.splitext(filename)
        source_path = os.path.join(large_dir, filename)
        thumb_path = os.path.join(thumb_dir, f"{name}_thumb.webp")
        #thumb_path = os.path.relpath(thumb_path, start=os.path.dirname(large_dir))

        # check the size of the image
        subprocess.run(["vips", "thumbnail", source_path, thumb_path, f"{thumb_size}x{thumb_size}", "--crop=centre"], check=True)

        # check if zip file with same name exists
        if name+".dzi.zip" in os.listdir(large_dir):
            print(f"Skipping {filename} as zip file already exists.")
        else:
            # zip the thumbnail
            subprocess.run(["vips", "dzsave", source_path, os.path.join(large_dir, name), "--suffix=.avif[Q=80]", f"--tile-size={tile_size}", "--layout=dz", "--overlap=1"], check=True)
            # zip the dzi files
            subprocess.run(["zip", "-r", f"{name}.dzi.zip", f"{name}.dzi", f"{name}_files"], cwd=large_dir, check=True)
        # remove the original files and directories
        if os.path.exists(os.path.join(large_dir, f"{name}.dzi")):
            os.remove(os.path.join(large_dir, f"{name}.dzi"))
            shutil.rmtree(os.path.join(large_dir, f"{name}_files"), ignore_errors=True)

        output_path = os.path.join(large_dir, f"{name}.dzi")
        print(f"Processed {source_path} -> {thumb_path}, {output_path}")

subprocess.run(["zip", "-r", f"thumbnails.zip", 'thumbnails'], cwd=large_dir, check=True)
if os.path.exists(thumb_dir):
    shutil.rmtree(thumb_dir, ignore_errors=True)
