import os
from PIL import Image

# 설정
source_dir = "./profile/gallery"
large_dir = "./profile/gallery_large"
thumb_dir = "./thumbnails"
thumb_size = 400
output_file = "./profile/gallery.html"

os.makedirs(thumb_dir, exist_ok=True)

valid_images = ('.png', '.jpg', '.webp', 'dzi', '.avif')
valid_zoomable = ('dzi')
valid_videos = ('.mp4', '.webm')

with open("profile/gallery_template.html", "r", encoding="utf-8") as f:
    HTML_TEMPLATE = f.read()
html_content = HTML_TEMPLATE

#num_papers = len(papers)
images_html = "<h2>Images</h2>"
Image.MAX_IMAGE_PIXELS = None

def crop_center_square(img):
    width, height = img.size
    min_side = min(width, height)
    left = (width - min_side) // 2
    top = (height - min_side) // 2
    right = left + min_side
    bottom = top + min_side
    return img.crop((left, top, right, bottom))

for filename in sorted(os.listdir(source_dir)):
    if filename.lower().endswith(valid_images):
        source_path = os.path.join(source_dir, filename)
        name, ext = os.path.splitext(filename)
        thumb_path = os.path.join(source_dir, thumb_dir, f"{name}_thumb.webp")
        os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
        try:
            with Image.open(source_path) as img:
                img = img.convert("RGBA")
                square_img = crop_center_square(img)
                resized = square_img.resize((thumb_size, thumb_size), Image.LANCZOS)
                resized.save(thumb_path, "WEBP")
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
        source_path = os.path.relpath(source_path, start=os.path.dirname(output_file))
        thumb_path = os.path.relpath(thumb_path, start=os.path.dirname(output_file))
        images_html += f"""
        <a href="{source_path}"><img src="{thumb_path}" alt="{name}" height="{thumb_size}px"></a>
        """
html_content = html_content.replace("{list_images}", images_html)

large_html = ""
for filename in sorted(os.listdir(large_dir)):
    if filename.lower().endswith(valid_zoomable):
        source_path = os.path.join(large_dir, filename)
        name, ext = os.path.splitext(filename)
        thumb_path = os.path.join(large_dir, thumb_dir, name+"_thumb.webp")
        source_path = os.path.relpath(source_path, start=os.path.dirname(output_file))
        thumb_path = os.path.relpath(thumb_path, start=os.path.dirname(output_file))
        large_html += f"""
        <img src="{thumb_path}" data-dzi="{source_path}" alt="{name}" height="{thumb_size}px">
        """
html_content = html_content.replace("{list_large_images}", large_html)

videos_html = "<h2>Videos</h2>"
for filename in sorted(os.listdir(source_dir)):
    if filename.lower().endswith(valid_videos):
        source_path = os.path.join(source_dir, filename)
        name, ext = os.path.splitext(filename)
        source_path = os.path.relpath(source_path, start=os.path.dirname(output_file))
        videos_html += f"""
        <video controls height="300">
            <source src="{source_path}" type="video/{ext[1:]}">
            Your browser does not support the video tag.
        </video>
        """
html_content = html_content.replace("{list_videos}", videos_html)

# Write to file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"HTML file generated: {output_file}")
