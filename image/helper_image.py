"""
# @Time     : 2022/3/1 7:47 上午
# @Author   : ssw
# @File     : helper_image.py
# @Desc      : 
"""

from PIL import Image as image


def resize_img(img_path, save_path, width=1024, height=1600, quality=50):
    """等比例压缩图片"""
    im = image.open(img_path)
    ori_w, ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and width and ori_w > width) or (ori_h and height and ori_h > height):
        if width and ori_w > width:
            widthRatio = float(width) / ori_w  # 正确获取小数的方式
        if height and ori_h > height:
            heightRatio = float(height) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h

    im.resize((newWidth, newHeight), image.ANTIALIAS).save(save_path, quality=quality)