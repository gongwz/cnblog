import random
import os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from cnblog.settings import BASE_DIR


def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_valid_code_img(request):
    img = Image.new("RGB", (225, 34), color=get_random_color())
    draw = ImageDraw.Draw(img)
    
    # kumo_font = ImageFont.truetype("/static/bootstrap/fonts/kumo.ttf", 22)
    # 报错：cannot open resource
    kumo_font = ImageFont.truetype(os.path.join(BASE_DIR, 'static/bootstrap/fonts/kumo.ttf'), 22)
    # 这里使用拼接的路径是没报错了，不要用相对路径
    
    # kumo_font = ImageFont.load_default().font # 这样使用默认的字体不是太方便，怎么改字体大小也没找到
    
    valid_code_str = ""
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(95, 122))  # 小写字母的assic
        random_upper_alpha = chr(random.randint(65, 90))  # 大写字母
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((i * 40 + 20, 5), random_char, get_random_color(), font=kumo_font)
        
        # 保存验证码字符串
        valid_code_str += random_char
    
    # 噪点噪线技术
    width = 225
    height = 34
    for i in range(2): # 噪线个数
        
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())
    
    for i in range(8): # 噪点个数
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())
    
    # print("valid_code_str", valid_code_str)
    
    request.session["valid_code_str"] = valid_code_str
    
    '''
    1 sdajsdq33asdasd
    2 COOKIE {"sessionid":sdajsdq33asdasd}
    3 django-session
      session-key       session-data
      sdajsdq33asdasd   {"valid_code_str":"12345"}
    '''
    
    # 内存操作比硬盘操作要快很多
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    
    return data
