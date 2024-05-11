from PIL.Image import open as image_open, Image


async def image_open_async(path: str):
    return image_open(path)


async def image_save_async(avatar: Image, path: str):
    avatar.save(path)


async def square_crop_logo(path: str | bytes, size=300):
    logo = await image_open_async(path)

    if logo.height > size or logo.width > size:
        output_size = (size, size)
        logo.thumbnail(output_size)
        await image_save_async(logo, path)
