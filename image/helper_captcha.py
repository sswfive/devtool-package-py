"""
# @Time     : 2022/3/1 7:50 上午
# @Author   : ssw
# @File     : helper_captcha.py
# @Desc      : 
"""
import os
import random
import string
import time

from PIL import Image, ImageDraw, ImageFont


class Captcha1:
    """
    图片验证码 不使用第三方插件库的情况下
    """

    # 生成的验证码的个数
    number = 4
    # 图片的宽度和高度
    size = (90, 38)
    # 字体大小
    fontsize = 35
    # 干扰线条数
    line_number = 3

    SOURCE = list(string.ascii_letters)
    SOURCE.extend(map(str, list(range(0, 2))))

    @classmethod
    def __gen_line(cls, draw, width, height):
        """
        绘制干扰线
        """
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.__gen_random_color(), width=2)

    @classmethod
    def __gen_random_color(cls, start=0, end=255):
        """
        产生随机颜色
        颜色的取值范围是0~255
        """
        random.seed()
        return (
            random.randint(start, end),
            random.randint(start, end),
            random.randint(start, end),
        )

    @classmethod
    def __gen_points(cls, draw, point_chance, width, height):
        """
        绘制干扰点
        """
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                temp = random.randint(0, 100)
                if temp > 100 - chance:
                    draw.point((w, h), fill=cls.__gen_random_color())

    @classmethod
    def __gen_random_font(cls):
        """
        采用随机字体
        :return:
        """
        # /usr/share/fonts/dejavu/DejaVuSansCondensed-Oblique.ttf
        # /usr/share/fonts/dejavu/DejaVuSansCondensed-Bold.ttf
        # /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf
        fonts = ["consola.ttf", "consolab.ttf", "consolai.ttf"]
        font = random.choice(fonts)
        return "helper/captcha/" + font

    @classmethod
    def gen_text(cls, number):
        """
        随机生成一个字符串
        :param number: 字符串数量
        """
        return "".join(random.sample(cls.SOURCE, number))

    @classmethod
    def gen_graph_captcha(cls):
        width, height = cls.size
        # A表示透明度
        image = Image.new("RGBA", (width, height), cls.__gen_random_color(0, 100))
        # 字体
        font = ImageFont.truetype(cls.__gen_random_font(), cls.fontsize)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 生成随机字符串
        text = cls.gen_text(cls.number)
        # 字体大小
        font_width, font_height = font.getsize(text)
        # 填充字符串
        draw.text(
            ((width - font_width) / 2, (height - font_height) / 2),
            text,
            font=font,
            fill=cls.__gen_random_color(150, 255),
        )
        # 绘制干扰线
        for x in range(0, cls.line_number):
            cls.__gen_line(draw, width, height)
        # 绘制噪点
        cls.__gen_points(draw, 10, width, height)

        return text, image


class Captcha2:
    """
    Image: 画布
    ImageDraw: 画笔
    ImageFont: 字体
    """
    # 把常亮抽取成类属性
    # 字体的位置
    font_path = os.path.join(os.path.dirname(__file__), 'simhei.ttf')
    # 生成几位数的验证码
    number = 4
    # 生成验证码的宽度和高度
    size = (100, 40)
    # 背景颜色，默认白色RGB(red,green,blue)
    bgcolor = (0, 0, 0)
    # 随机字体颜色
    random.seed(int(time.time()))
    fontcolor = (random.randint(200, 255), random.randint(100, 255), random.randint(100, 255))
    # 验证码字体大小
    fontsize = 20
    # 随机干扰线颜色
    linecolor = (random.randint(0, 250), random.randint(0, 255), random.randint(0, 250))
    # 是否要加入干扰线
    draw_line = True
    # 是否回执干扰线
    draw_point = True
    # 加入干扰线的条数
    line_number = 3

    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))

    # 用来随机生成一个字符串（包括英文和数字）
    # 定义成类方法，然后是私有的，对象在外面不能直接调用
    @classmethod
    def gene_text(cls):
        return "".join(random.sample(cls.SOURCE, cls.number))

    # 用来回执干扰线
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.linecolor)

    # 用来回执干扰点
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    # 生成验证码
    @classmethod
    def gene_code(cls):
        width, height = cls.size
        image = Image.new('RGBA', (width, height), cls.bgcolor)  # 创建画板
        font = ImageFont.truetype(cls.font_path, cls.fontsize)  # 验证码字体
        draw = ImageDraw.Draw(image)  # 创建画笔
        text = cls.gene_text()  # 生成字符串
        font_width, font_height = font.getsize(text)
        draw.text(((width - font_width) / 2, (height - font_height) / 2), text, font=font, fill=cls.fontcolor)
        if cls.draw_line:
            # 遍历line_number次，就是画line_number根条线
            for x in range(0, cls.line_number):
                cls.__gene_line(draw, width, height)
        # 如果要回执噪点
        if cls.draw_point:
            cls.__gene_points(draw, 10, width, height)
        return (text, image)


class Captcha3:
    # 生成4位数的验证码
    numbers = 4
    # 验证码图片的宽度和高度
    size = (100, 30)
    # 验证码字体大小
    fontsize = 25
    # 加入干扰线的条数
    line_number = 2

    # 构建一个验证码源文本
    SOURCE = list(string.ascii_letters)
    for index in range(0, 10):
        SOURCE.append(str(index))

    # 用来绘制干扰线
    @classmethod
    def __gene_line(cls, draw, width, height):
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=cls.__gene_random_color(), width=2)

    # 用来绘制干扰点
    @classmethod
    def __gene_points(cls, draw, point_chance, width, height):
        # 大小限在【0， 100】中
        chance = min(100, max(0, int(point_chance)))
        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=cls.__gene_random_color())

    # 生成随机颜色
    @classmethod
    def __gene_random_color(cls, start=0, end=255):
        random.seed()
        return (random.randint(start, end),
                random.randint(start, end),
                random.randint(start, end))

    # 随机选择一个字体
    @classmethod
    def __gene_random_font(cls):
        fonts = [
            "PAPYRUS.TTF",
            "CENTAUR.TTF",
            "Inkfree.ttf",
            "verdana.ttf",
        ]
        font = random.choice(fonts)
        return "helper/captcha/" + font

    # 用来随机生成一个字符串（包括英文和数字）
    @classmethod
    def gene_text(cls, numbers):
        # numbers是生成验证码的位数
        return " ".join(random.sample(cls.SOURCE, numbers))

    # 生成验证码
    @classmethod
    def gene_graph_captcha(cls):
        # 验证码图片的宽高
        width, height = cls.size
        # 创建图片
        image = Image.new("RGBA", (width, height), cls.__gene_random_color(0, 100))
        # 验证码的字体
        font = ImageFont.truetype(cls.__gene_random_font(), cls.fontsize)
        # 创建画笔
        draw = ImageDraw.Draw(image)
        # 生成字符串
        text = cls.gene_text(cls.numbers)
        # 获取字体的尺寸
        font_width, font_height = font.getsize(text)
        # 填充字符串
        draw.text(((width - font_width) / 2, (height - font_height) / 2),
                  text, font=font, fill=cls.__gene_random_color(150, 255))
        # 绘制干扰线
        for x in range(0, cls.line_number):
            cls.__gene_line(draw, width, height)
        # 绘制干扰点
        cls.__gene_points(draw, 10, width, height)
        with open("captcha.png", "wb") as fp:
            image.save(fp)
        return text, image


if __name__ == '__main__':
    pass
    # from io import BytesIO
    # from flask import Blueprint, request, make_response, session
    #
    #
    # # @route_admin.route('/Captcha', methods=['GET'])
    # def GetCaptcha():
    #     text, image = Captcha().gen_graph_captcha()
    #     out = BytesIO()
    #     image.save(out, 'png')
    #     out.seek(0)
    #     resp = make_response(out.read())
    #     resp.content_type = 'image/png'
    #     # 存入session
    #     # session['Captcha'] = text
    #     return resp