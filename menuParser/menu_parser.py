# -*- coding: utf-8 -*-
from PIL import Image
import os
import time
import calendar

print (os.getcwd())

def get_h_size(convert_image, color):
    load_image = convert_image.load()
    pixel_count = 0
    for h in range(convert_image.size[1]):
        for w in range(convert_image.size[0]):
            if color == load_image[w, h]:
                pixel_count = pixel_count + 1
                if pixel_count > 50:
                    return h

def get_w_size(convert_image, color):
    load_image = convert_image.load()
    pixel_count = 0
    for w in range(convert_image.size[0]):
        for h in range(convert_image.size[1]):
            if color == load_image[w, h]:
                pixel_count = pixel_count + 1
                if pixel_count > 50:
                    return w

def crop_save_meal_image(day, menu_image, color):
    convert_image = menu_image.convert('RGB')
    load_image = menu_image.load()
    crop_h = 0
    pixel_count = 0

    for w in range(convert_image.size[0]):
        for h in range(convert_image.size[1]):
            if color == load_image[w, h]:
                pixel_count = pixel_count + 1
                if pixel_count > 50:
                    crop_h = h
                    break
    # 점심메뉴 자르기
    lunch_menu_image = menu_image.crop((0, 0, convert_image.size[0], crop_h))
    lunch_menu_image.save(day + '_lunch_menu.png')

    # 저녁메뉴 자르기
    dinner_menu_temp_image = menu_image.crop((0, crop_h + 5, convert_image.size[0], convert_image.size[1]))
    convert_image = dinner_menu_temp_image.convert('RGB')

    crop_h = 0
    pixel_count = 0
    load_image = convert_image.load()
    for w in range(convert_image.size[0]):
        for h in range(convert_image.size[1]):
            if color == load_image[w, h]:
                pixel_count = pixel_count + 1
                if pixel_count > 50:
                    crop_h = h
                    break
    dinner_menu_image = dinner_menu_temp_image.crop((0, 0, convert_image.size[0], crop_h))
    dinner_menu_image.save(day + '_dinner_menu.png')

'''
    type 0: launch, 1:dinner
    usage : get_day_meal_image("menu.png", time.strftime('%A'), 0).save("test.png")
'''
def get_day_meal_image(whole_menu_image, day, type):
    today_menu_image = crop_day_meal_image(whole_menu_image, day)

    if today_menu_image is None:
        return None

    #black
    color = (45, 45, 45)
    convert_image = today_menu_image.convert('RGB')
    load_image = today_menu_image.load()

    crop_h = 0
    pixel_count = 0
    for w in range(convert_image.size[0]):
        for h in range(convert_image.size[1]):
            if color == load_image[w, h]:
                pixel_count = pixel_count + 1
                if pixel_count > 50:
                    crop_h = h
                    break

    if type == 0:
        return today_menu_image.crop((0, 0, convert_image.size[0], crop_h))

    elif type == 1:
        dinner_menu_temp_image = today_menu_image.crop((0, crop_h + 5, convert_image.size[0], convert_image.size[1]))
        convert_image = dinner_menu_temp_image.convert('RGB')

        crop_h = 0
        pixel_count = 0
        load_image = convert_image.load()
        for w in range(convert_image.size[0]):
            for h in range(convert_image.size[1]):
                if color == load_image[w, h]:
                    pixel_count = pixel_count + 1
                    if pixel_count > 50:
                        crop_h = h
                        break
        return dinner_menu_temp_image.crop((0, 0, convert_image.size[0], crop_h))
    else:
        return None



def crop_day_meal_image(image, day):
    green = (16, 152, 89)
    deep_green = (8, 99, 39)

    convert_image = image.convert('RGB')
    crop_h = get_h_size(convert_image, green)
    crop_image = image.crop((0, crop_h, convert_image.size[0], convert_image.size[1]))

    # 요일별 자르기
    convert_image = crop_image.convert('RGB')
    crop_w = get_w_size(convert_image, deep_green)
    day_index = list(calendar.day_name).index(time.strftime('%A'))
    category_image = crop_image.crop((0, 0, crop_w - (130 * 2), convert_image.size[1]))

    if day_index == 0:
        return merge_image(category_image, crop_image.crop((crop_w - (130 * 2), 0, crop_w - 130 , convert_image.size[1])))
    elif day_index == 1:
        return merge_image(category_image, crop_image.crop((crop_w - 130       , 0, crop_w             , convert_image.size[1])))
    elif day_index == 2:
        return merge_image(category_image, crop_image.crop((crop_w             , 0, crop_w + 130       , convert_image.size[1])))
    elif day_index == 3:
        return merge_image(category_image, crop_image.crop((crop_w + 130       , 0, crop_w + (130 * 2) , convert_image.size[1])))
    elif day_index == 4:
        return merge_image(category_image, crop_image.crop((crop_w + (130 * 2) , 0, crop_w + (130 * 3) , convert_image.size[1])))
    else:
        return None;

def merge_image(image1, image2):
    images = [image1, image2]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    return new_im

# crop_w = 0
# crop_h = 0
#
# green = (16, 152, 89)
# deep_green = (8, 99, 39)
# black = (45, 45, 45)
#
# #이미지 로드
# image = Image.open("menu.png")
# convert_image = image.convert('RGB')
#
# crop_h = get_h_size(convert_image, green)
# crop_image = image.crop((0, crop_h, convert_image.size[0], convert_image.size[1]))
#
# #요일별 자르기
# convert_image = crop_image.convert('RGB')
# crop_w = get_w_size(convert_image, deep_green)
#
# monday_menu_image =     crop_image.crop((crop_w - (130 * 2) , 0, crop_w - 130       , convert_image.size[1]))
# tuesday_menu_image =    crop_image.crop((crop_w - 130       , 0, crop_w             , convert_image.size[1]))
# wednesday_menu_image =  crop_image.crop((crop_w             , 0, crop_w + 130       , convert_image.size[1]))
# thursday_menu_image =   crop_image.crop((crop_w + 130       , 0, crop_w + (130 * 2) , convert_image.size[1]))
# friday_menu_image =     crop_image.crop((crop_w + (130 * 2) , 0, crop_w + (130 * 3) , convert_image.size[1]))
# category_image =        crop_image.crop((0                  , 0, crop_w - (130 * 2) , convert_image.size[1]))
#
# #요일별 점심 저녁별 자르고 저장하기
# crop_save_meal_image('monday', merge_image(category_image, monday_menu_image), black)
# crop_save_meal_image('tuesday', merge_image(category_image, tuesday_menu_image), black)
# crop_save_meal_image('wednesday', merge_image(category_image, wednesday_menu_image), black)
# crop_save_meal_image('thursday', merge_image(category_image, thursday_menu_image), black)
# crop_save_meal_image('friday', merge_image(category_image, friday_menu_image), black)
# crop_save_meal_image('category', merge_image(category_image, category_image), black)

# get_day_meal_image("menu.png", time.strftime('%A'), 0).save("test.png")