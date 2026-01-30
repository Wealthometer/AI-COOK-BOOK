from PIL import Image


def resize_image(image_path: str, target_size: tuple[int, int] = (720, 1280)) -> str:
    img = Image.open(image_path)
    width, height = img.size
    target_width, target_height = target_size

    scale = max(target_width / width, target_height / height)
    new_width, new_height = int(width * scale), int(height * scale)
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    img_cropped = img_resized.crop(
        (left, top, left + target_width, top + target_height)
    )

    img_cropped.save(image_path)
    return image_path
