from sqlitedict import SqliteDict
import json
import os
import re
import random
import urllib
from pathlib import Path
from hoshino import R, logger

# 储存数据位置（初次使用后不可改动）
# file_path = R.img('xqa').path  # 数据在res文件夹里


file_path = os.path.dirname(__file__)  # 数据在插件文件夹里


# 判断是否在群里
async def judge_ismember(bot, group_id: str, user_id: str) -> bool:
    member_list = await bot.get_group_member_list(group_id=int(group_id))
    user_list = []
    for member in member_list:
        user_id_tmp = member['user_id']
        user_list.append(str(user_id_tmp))
    if user_id in user_list:
        return True
    else:
        return False


# 获取数据库
async def get_database() -> SqliteDict:
    # 创建目录
    img_path = os.path.join(file_path, 'img/')
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    db_path = os.path.join(file_path, 'data.sqlite')
    # 替换默认的pickle为josn的形式读写数据库
    db = SqliteDict(db_path, encode=json.dumps, decode=json.loads, autocommit=True)
    return db


# 获取群列表
async def get_g_list(bot) -> list:
    group_list = await bot.get_group_list()
    g_list = []
    for group in group_list:
        group_id = group['group_id']
        g_list.append(str(group_id))
    return g_list


# 搜索问答
async def get_search(que_list: list, search_str: str) -> list:
    if not search_str:
        return que_list
    search_list = []
    for question in que_list:
        if re.search(rf'\S*{search_str}\S*', question):
            search_list.append(question)
    return search_list


# 匹配替换字符
async def replace_message(match_que: re.Match, match_dict: dict, que: str) -> str:
    ans_tmp = match_dict.get(que)
    # 随机选择
    ans = random.choice(ans_tmp)
    flow_num = re.search(r'\S*\$([0-9])\S*', ans)
    if not flow_num:
        return ans
    for i in range(int(flow_num.group(1))):
        ans = ans.replace(f'${i + 1}', match_que.group(i + 1))
    return ans


# 调整转义分割字符 “#”
async def adjust_list(list_tmp: list, char: str) -> list:
    ans_list = []
    str_tmp = list_tmp[0]
    i = 0
    while i < len(list_tmp):
        if list_tmp[i].endswith('\\'):
            str_tmp += char + list_tmp[i + 1]
        else:
            ans_list.append(str_tmp)
            str_tmp = list_tmp[i + 1] if i + 1 < len(list_tmp) else list_tmp[i]
        i += 1
    return ans_list


# 下载以及分类图片
async def doing_img(bot, img: str, is_ans: bool, save: bool) -> str:
    img_path = os.path.join(file_path, 'img/')
    if save:
        try:
            img_url = await bot.get_image(file=img)
            file = os.path.join(img_path, img)
            if not os.path.isfile(img_path + img):
                urllib.request.urlretrieve(url=img_url['url'], filename=file)
                logger.critical(f'XQA: 已下载图片{img}')
        except:
            logger.critical(f'XQA: 图片{img}已经过期，请重新设置问答')
            pass
    if is_ans:  # 保证保存图片的完整性，方便迁移和后续做操作
        return 'file:///' + img_path + img
    return img


async def remove_path(file: str) -> str:
    try:
        file = file.replace('file:///', '')
        img_path = os.path.split(file)[0]
        file = file.replace(str(img_path), '')
        return file.replace('/', '')
    finally:
        return file


# 进行图片处理
async def adjust_img(bot, str_raw: str, is_ans: bool = False, save: bool = False) -> str:  # 应该可以用了
    image_list = re.findall(r'(\[CQ:image,file=(\S+?)\,url=(\S+?)\,subType\S*?\])', str_raw)
    old_image_list = re.findall(r'(\[CQ:image,file=(\S+?)\.image])', str_raw)
    if old_image_list:  # 尝试缓存之前的图片
        for image in old_image_list:
            image[1] = remove_path(image[1])
            img = doing_img(bot, image[1] + '.image', is_ans, save)
            str_raw = str_raw.replace(image[0], f'[CQ:image,file={img}]')
    if image_list:
        for image in image_list:
            img = doing_img(bot, image[1], is_ans, save)
            str_raw = str_raw.replace(image[0], f'[CQ:image,file={img}]')
    return str_raw


# 匹配消息
async def match_ans(info: dict, message: str, ans: str) -> str:
    list_tmp = list(info.keys())
    list_tmp.reverse()
    for que in list_tmp:
        # 优先完全匹配
        if que == message:
            ans = random.choice(info[que])
            break
        # 其次正则匹配
        try:
            if re.match(que + '$', message):
                ans = await replace_message(re.match(que + '$', message), info, que)
                break
        except re.error:
            # 如果que不是re.pattern的形式就跳过
            continue
    return ans


# 删除图片缓存
async def delete_img(file: list):
    try:
        file = str(file)
        img_file = re.findall(r'(\[CQ:image,file=(.+?)\.image])', file)
        for img in img_file:
            file = os.path.abspath(file_path + '/img/' + img[1])
            os.remove(file + '.image')
    except:
        pass
    return
