#2025-03-06 06:26:39
"""
* 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
* 猫猫看看 
* 版本号：V3.62
* 安装依赖：pycryptodome psutil

* 活动入口,微信打开：
* 如果连接过期了运行一下就出来了最新的入口！
* http://t51.17365231287fs.xrm6qy8i.cyou/kstief/2093a8936e8ab34e3a10c5b783b6a407?tsd=654
* 打开活动入口，抓包的任意接口cookies中的Cookie参数
* 
* 变量格式：
* 新建同名环境变量
* 变量名：mykkyd
* 变量值：
* # 3000 代表 3毛，后面两个推送参数可不填，那就必须配置全局推送！
* 账号备注#Cookie参数#提现金额如3000#wxpushApptoken#wxpushTopicId#支付宝姓名#支付宝账号#微信UA
============================================================
* 最简下级账户配置：账号备注#Cookie参数######微信UA
============================================================
* 
* 其他参数说明（脚本最下方填写参数）
* wxpusher全局参数：wxpusherAppToken、wxpusherTopicId
* 具体使用方法请看文档地址：https://wxpusher.zjiecode.com/docs/#/
* 
* 也可使用 微信机器人：wechatBussinessKey
* 
* 支持支付宝提现：账号备注#Cookie参数#提现金额如3000#wxpushApptoken#wxpushTopicId#支付宝姓名#支付宝账号
* 只想提现支付宝，不想填写其他参数，最少的参数就是：账号备注#Cookie参数####支付宝姓名#支付宝账号
*
* 增加 自定义检测文章等待时间：mykkydReadPostDelay，默认值是 15-20秒
* 增加 精简日志：mykkydReadPureLog，默认值是 true（也就是精简日志，如果需要显示完整的，请设置为 false）
*
* 定时运行每半小时一次
* 达到标准，自动提现
"""

# 仅做邀请任务（3000金币自动停止运行并禁止提现） 是否启用 True 或者 False
import getpass
import socket
import platform
import subprocess
from Crypto.Cipher import AES
from urllib.parse import parse_qs, urlsplit
import urllib
import urllib3
from urllib.parse import quote, unquote, urlparse, parse_qs
import re
import random
import requests
import time
import sys
from pathlib import Path
import os
import math
import json
import hashlib
import gzip
import datetime
from concurrent.futures import ThreadPoolExecutor
import base64
onlyDoInviteRewardJob = False


# import psutil
github_fast_proxy_url = "https://ghp.ci/https://raw.githubusercontent.com/Huansheng1/my-qinglong-js/main/"
scriptVersion = "V3.60"


def utf8_encode_decode(text):
    try:
        # 尝试将utf-8编码的字符串解码
        return unquote(text)
    except Exception as e:
        return text


def get_announce():
    try:
        txt = requests.get(
            github_fast_proxy_url + "announce.txt",
            verify=False,
            timeout=60,
        ).text
        print(txt or "广告区域（预留）: 啦啦啦~啦啦啦~，我是卖广告的小行家")
    except Exception as e:
        print(f"获取公告失败: {e}")


def get_lastest_version(
    script_url: str = "README.md", timeout: int = 20
):
    url = f"{github_fast_proxy_url}{script_url}"

    try:
        response = requests.get(
            url,
            timeout=timeout,
            verify=False,
        )
        response.raise_for_status()
        data = response.text

        regex = r'版本号：V\s*([\d.]+)'
        match = re.search(regex, data)
        script_version_latest = match.group(1) if match else ""
        print(
            f"当前版本:[{scriptVersion or '未知'}]>>>>>云端☁️版本:[{script_version_latest or '未知'}]"
        )
        return script_version_latest
    except requests.exceptions.RequestException as e:
        print(
            f"拉取仓库最新版本脚本失败: {utf8_encode_decode(str(e).replace(f'{github_fast_proxy_url}Huansheng1/my-qinglong-js@main/',''))}"
        )
        return None


def get_files_hash(directory):
    """对指定目录下的文件内容生成哈希值"""
    hasher = hashlib.sha256()
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        data = f.read()
                        hasher.update(data)
                except PermissionError:
                    # 忽略权限错误
                    pass
                except FileNotFoundError:
                    # 忽略文件不存在错误
                    pass
    except Exception as e:
        # print(f"Error reading files in {directory}: {e}")
        pass
    return hasher.hexdigest()


def get_username():
    """尝试获取当前Linux用户名，优先使用getpass.getuser()，如果失败则尝试os.getlogin()"""
    try:
        # 首选方法：使用getpass模块
        return getpass.getuser()
    except KeyError:  # getpass.getuser()在某些情况下可能抛出KeyError（尽管不太常见）
        pass
    try:
        # 备用方法：使用os.getlogin()，但捕获可能的异常
        return os.getlogin()
    except OSError:
        # 如果os.getlogin()失败，返回一个默认用户名或None
        return "unknown_user"


def get_mac_address():
    """获取系统的主要MAC地址（如果有的话）"""
    mac = "00:00:00:00:00:00"
    try:
        # 这只是获取MAC地址的一种方法，可能需要根据实际情况调整
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        mac = s.getsockname()[0]
        s.close()
        # 注意：上面的代码实际上并没有获取MAC地址，这里只是示例
        # 真正的MAC地址获取可能需要读取/sys/class/net/<interface>/address
        interfaces = [i for i in os.listdir("/sys/class/net/") if ":" not in i]
        for interface in interfaces:
            try:
                with open(f"/sys/class/net/{interface}/address", "r") as f:
                    mac = f.read().strip()
                    break
            except FileNotFoundError:
                pass
    except Exception as e:
        # print(f"Error getting MAC address: {e}")
        pass
    return mac


def generate_machine_id():
    """生成机器码"""
    # 获取/sys/devices/virtual目录的哈希值
    virtual_devices_hash = get_files_hash("/sys/devices/virtual")
    # 获取当前用户名
    username = get_username()
    # 获取MAC地址
    mac = get_mac_address()

    # 合并信息并生成最终的哈希值
    data = f"{virtual_devices_hash}{username}{mac}{platform.platform()}".encode(
        "utf-8")
    hasher = hashlib.sha256()
    hasher.update(data)
    return hasher.hexdigest()


def generate_random_ip(is_in_china=True):
    min_ip = "1.1.1.1" if is_in_china else "0.0.0.0"
    max_ip = "223.255.255.255" if is_in_china else "255.255.255.255"

    min_parts = list(map(int, min_ip.split(".")))
    max_parts = list(map(int, max_ip.split(".")))

    random_parts = [random.randint(min, max)
                    for min, max in zip(min_parts, max_parts)]

    return ".".join(map(str, random_parts))


urllib3.disable_warnings()

check_post_str = os.getenv("mykkydCheckPostIds") or "1"
checkPostIds = []
if check_post_str:
    checkPostIds = [int(check_post_str)]
if "," in check_post_str:
    for id in check_post_str.split(","):
        checkPostIds.append(int(id))
# 填wxpusher的appToken，配置在环境变量里这样没配置的账号会自动使用这个推送
wxpusherAppToken = os.getenv("wxpusherAppToken") or ""
wxpusherTopicId = os.getenv("wxpusherTopicId") or ""
wechatBussinessKey = os.getenv("wechatBussinessKey") or ""
mykkydDetectingSealStatus = True
mykkydDisabledDetectingSealSetting = os.getenv("mykkydDisabledDetectingSeal")
if mykkydDisabledDetectingSealSetting not in ["", None]:
    if mykkydDisabledDetectingSealSetting in ["1", "true", True]:
        mykkydDetectingSealStatus = False
readPostDelay = 0
if os.getenv("mykkydReadPostDelay") and os.getenv("mykkydReadPostDelay").isdecimal():
    readPostDelay = int(os.getenv("mykkydReadPostDelay"))
mykkydReadPureLog = True
if os.getenv("mykkydReadPureLog"):
    mykkydReadPureLog = os.getenv("mykkydReadPureLog") == "true"
# 设置代理地址和端口
proxies = None
if os.getenv("mykkydHttpProxyUrl"):
    proxies = {
        "http": os.getenv("mykkydHttpProxyUrl"),
        "https": os.getenv("mykkydHttpProxyUrl"),
    }
# 幻生接口
hs_api_origin = os.getenv('hs_read_project_api') or "https://huansheng.us.kg"
hs_api_card = os.getenv(
    'hs_read_project_api_card') or '9b735036dcac5c86ce4fbd9556fe94e82b138aca4d2bcc703799c1dc4a7fbc11:IhqAf39iNH5qfXbUFeLAYM7FJz9dt6uzIh2wL7Xp2aDB/uYX5FSkeljSDxPSm3/QCKlMJevTOarKn66aUgAJxxXgrfP1Rt2nrO0+exSt+6k='
hs_api_aes_key = "Bh2bgfp080pV+A6coEvPz8+JanUy4EQ/L6Gfjx91LFM="
hs_api_aes_iv = "lHAldWCTjP930SxProOz1w=="
thirdPartnerApiUrl = os.getenv("mykkydThirdPartnerApiUrl") or ""
check_bizs = [
    "MzkxNTE3MzQ4MQ==",
    "Mzg5MjM0MDEwNw==",
    "MzUzODY4NzE2OQ==",
    "MzkyMjE3MzYxMg==",
    "MzkxNjMwNDIzOA==",
    "Mzg3NzUxMjc5Mg==",
    "Mzg4NTcwODE1NA==",
    "Mzk0ODIxODE4OQ==",
    "Mzg2NjUyMjI1NA==",
    "MzIzMDczODg4Mw==",
    "Mzg5ODUyMzYzMQ==",
    "MzU0NzI5Mjc4OQ==",
    "Mzg5MDgxODAzMg==",
    "MzkxNDU1NDEzNw==",
    "MzkzNTYxOTgyMA==",
    "MzkxNDYzOTEyMw==",
    "MzkwMTYwNzcwMw==",
    "MzkyNjY0MTExOA==",
    "MzkyMjYxNzQ2NA==",
    "MzkzMTYyMDU0OQ==",
    "MzkzNDYxODY5OA==",
    "MzkwNzYwNDYyMQ==",
    "MzUyNjA1MTQ3Mg==",
    "MzkyNjMzNzQwNw==",
    "Mzg3NDYwNDE3MQ==",
    "MzkzMTY5MTM4MQ==",
    "MzU5ODkzMDAzNA==",
    "Mzk0NDcxMTk2MQ==",
    "MzIyNjM0MDg5Ng==",
    "MzA4Nzc5NjA1Mw=="
]

# 获取硬盘序列号
# def get_disk_serial():
#     partitions = psutil.disk_partitions()
#     for partition in partitions:
#         try:
#             partition_info = psutil.disk_usage(partition.mountpoint)
#             if partition_info.total > 0:
#                 disk_serial = psutil.disk_serial_number(partition.device)
#                 if disk_serial:
#                     return disk_serial
#         except Exception as e:
#             pass
#     return None


# # 获取主板序列号
# def get_mainboard_serial():
#     mainboard_serial = None
#     try:
#         with open("/sys/class/dmi/id/board_serial") as f:
#             mainboard_serial = f.read().strip()
#     except Exception as e:
#         pass
#     return mainboard_serial


# # 获取CPU序列号
# def get_cpu_serial():
#     cpu_serial = None
#     try:
#         with open("/proc/cpuinfo") as f:
#             for line in f:
#                 if line.strip().startswith("Serial"):
#                     cpu_serial = line.split(":")[1].strip()
#                     break
#     except Exception as e:
#         pass
#     return cpu_serial


# 获取硬件唯一码
# def get_hardware_unique_code():
#     disk_serial = get_disk_serial()
#     mainboard_serial = get_mainboard_serial()
#     cpu_serial = get_cpu_serial()

#     unique_code = f"{disk_serial}-{mainboard_serial}-{cpu_serial}"
#     return unique_code


def get_machine_code():
    # 获取制造商和型号
    manufacturer = (
        subprocess.check_output(
            "cat /sys/devices/virtual/dmi/id/sys_vendor",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
        .decode()
        .strip()
    )
    model = (
        subprocess.check_output(
            "cat /sys/devices/virtual/dmi/id/product_name",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
        .decode()
        .strip()
    )

    # 获取MAC地址
    mac_address = (
        subprocess.check_output(
            "cat /sys/class/net/$(ip route show default | awk '/default/ {print $5}')/address",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
        .decode()
        .strip()
    )

    # 获取CPU ID
    cpu_id = (
        subprocess.check_output(
            "cat /proc/cpuinfo | grep 'Serial' | awk '{print $3}'",
            shell=True,
            stderr=subprocess.DEVNULL,
        )
        .decode()
        .strip()
    )

    machine_code = f"{manufacturer}-{model}-{mac_address}-{cpu_id}"
    return machine_code


# AES 加密函数
def aes_encrypt(value, key_str, iv_str):
    key_bytes = base64.b64decode(key_str)
    iv_bytes = base64.b64decode(iv_str)

    # 确保 value 的长度是 AES 块大小的倍数，这里使用 PKCS7 填充
    if isinstance(value, str):
        value = value.encode("utf-8")  # 确保 value 是 bytes 类型
    pad_len = 16 - (len(value) % 16)
    value += bytes([pad_len]) * pad_len

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    encrypted_data = cipher.encrypt(value)

    # 返回 base64 编码的加密数据，便于传输和存储
    return base64.b64encode(encrypted_data).decode("utf-8")


def check_file_md5(url, expected_md5):
    # 获取文件内容
    response = safe_request("GET", url)
    data = response.content

    # 计算MD5
    md5 = hashlib.md5()
    md5.update(data)
    calculated_md5 = md5.hexdigest()
    # print("当前文件的MD5值为：", calculated_md5)
    # 比较MD5
    return calculated_md5 == expected_md5


def check_str_md5(str, expected_md5):
    # 计算MD5
    md5 = hashlib.md5()
    md5.update(str.encode("utf-8"))
    calculated_md5 = md5.hexdigest()
    # print("当前内容的MD5值为：", calculated_md5)
    # 比较MD5
    return calculated_md5 == expected_md5


def extract_middle_text(source, before_text, after_text, all_matches=False):
    results = []
    start_index = source.find(before_text)

    while start_index != -1:
        source_after_before_text = source[start_index + len(before_text):]
        end_index = source_after_before_text.find(after_text)

        if end_index == -1:
            break

        results.append(source_after_before_text[:end_index])
        if not all_matches:
            break

        source = source_after_before_text[end_index + len(after_text):]
        start_index = source.find(before_text)

    return results if all_matches else results[0] if results else ""


def push_to_third_party(link):
    try:
        p = safe_request(
            "get", url=f"{thirdPartnerApiUrl}{link}", verify=False)
        print(f"✅ 推送文章到第三方接口成功：{p.text}")
    except:
        print("❌ 推送文章到第三方接口失败，完犊子，要黑号了！")
        return False


def push(appToken, topicIds, title, link, text, type):
    datapust = {
        "appToken": appToken,
        "content": f"""<body onload="window.location.href='{link}'">出现检测文章！！！\n<a style='padding:10px;color:red;font-size:20px;' href='{link}'>点击我打开待检测文章</a>\n请尽快点击链接完成阅读\n备注：{text}</body>""",
        "summary": title or "猫猫看看阅读",
        "contentType": 2,
        "topicIds": [topicIds or "11686"],
        "url": link,
    }
    # print(datapust)
    urlpust = "http://wxpusher.zjiecode.com/api/send/message"
    try:
        p = safe_request("POST", url=urlpust, json=datapust, verify=False)
        # print(p)
        if p.json()["code"] == 1000:
            print("✅ 推送文章到微信成功，请尽快前往点击文章，不然就黑号啦！")
            return True
        else:
            print("❌ 推送文章到微信失败，完犊子，要黑号了！")
            return False
    except:
        print("❌ 推送文章到微信失败，完犊子，要黑号了！")
        return False


def pushWechatBussiness(robotKey, link):
    datapust = {"msgtype": "text", "text": {"content": link}}
    # print(datapust)
    urlpust = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + robotKey
    try:
        p = safe_request("POST", url=urlpust, json=datapust, verify=False)
        # print(p)
        if p.json()["errcode"] == 0:
            print("✅ 推送文章到企业微信成功！")
            return True
        else:
            print("❌ 推送文章到企业微信失败！")
            return False
    except:
        print("❌ 推送文章到企业微信失败！")
        return False


def trimSpaceCharacters(text):
    return "".join(text.split())


class LinkCache:
    def __init__(self, file_path):
        self.file_path = file_path
        self.cache = self.load_cache()

    def load_cache(self):
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_cache(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print("无法保存链接到本地缓存文件：", e)

    def add_link(self, link, date):
        if link not in self.cache:
            self.cache[link] = {"publishDate": date, "count": 1}
        else:
            self.cache[link]["count"] += 1
        self.save_cache()

    def get_link_info(self, link):
        return self.cache.get(link, None)

    def get_all_links(self):
        return list(self.cache.keys())


link_cache = LinkCache("huansheng_mykk_link_cache.json")


def fetch_wx_time_and_record(url, link_cache):
    max_retries = 3
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; RMX1971 Build/QKQ1.190918.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160083 MMWEBSDK/20231202 MMWEBID/8342 MicroMessenger/8.0.47.2560(0x28002F51) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
    }
    for i in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            wx = response.text
            wz_time_regex = r"var createTime = '(.*?)';"
            match = re.search(wz_time_regex, wx)
            if match:
                article_time = match.group(1)
                print(f"微信文章发布时间: {article_time}")
                link_info = link_cache.get_link_info(url)
                print(
                    f"该检测文章，已记录了 {link_info['count'] if link_info else 0 + 1} 次"
                )
                link_cache.add_link(url, article_time)
                return True
        except Exception as e:
            print(f"检测微信文章时间发生错误: {e}")
            return True


def safe_request(method, url, retries=3, **kwargs):
    for i in range(retries):
        try:
            if method.upper() == "GET":
                response = requests.get(url, **kwargs)
            elif method.upper() == "POST":
                response = requests.post(url, **kwargs)
            else:
                print(f"不支持的请求类型: {method}")
                return None
            # response.encoding = 'utf-8'
            return response
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            if i < retries - 1:  # 如果不是最后一次尝试，就等待一段时间再重试
                wait = random.randint(1, 5)  # 随机等待时间
                print(f"等待 {wait} 秒后重试...")
                time.sleep(wait)
            else:
                print("尝试请求失败，已达到最大尝试次数")
                return None  # 或者你可以返回一个特定的值或对象来表示请求失败


def ts():
    return str(int(time.time())) + "000"


machine_code = "unknown"
try:
    # linux服务器生成唯一机器码
    machine_code = get_machine_code()
except Exception as e:
    # 适配青龙模块生成机器码
    machine_code = generate_machine_id()


def is_not_timestamp(value):
    # 尝试将值转换为datetime对象
    try:
        # Unix时间戳是整数或浮点数
        if isinstance(value, (int, float)):
            # 转换为datetime对象
            datetime.datetime.fromtimestamp(value)
            return False  # 如果成功，则认为它是时间戳
        else:
            return True  # 不是整数或浮点数，所以它不是时间戳
    except (OverflowError, OSError, ValueError, TypeError):
        # 如果转换失败，则它不是一个有效的时间戳
        return True


class MMKKYD:
    def __init__(self, cg):
        self.Cookie = cg["Cookie"]
        self.txbz = cg["txbz"]
        self.topicIds = cg["topicIds"]
        self.appToken = cg["appToken"]
        global wechatBussinessKey
        self.wechatBussinessKey = wechatBussinessKey or ""
        self.aliAccount = cg["aliAccount"] or ""
        self.aliName = cg["aliName"] or ""
        self.name = cg["name"]
        self.domnainHost = "1698855139.hxiong.top"
        self.request_id = ""
        self.userAgent = cg["userAgent"]
        self.fakeIp = generate_random_ip()
        self.headers = {
            "Connection": "keep-alive",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": self.userAgent
            or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"http://{self.domnainHost}/",
            "Origin": f"http://{self.domnainHost}",
            # "Host": f"{self.domnainHost}",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": self.Cookie,
            "Client-Ip": self.fakeIp,
            "X-Forwarded-For": self.fakeIp,
            "Remote_Addr": self.fakeIp,
        }
        self.prevPostLink = ""
        self.readJumpPath = ""
        self.retryReading = False
        self.remain_gold = 0
        self.remain = 0
        self.readApiVersion = "8.0"
        self.addGoldPath = ""
        self.getReadUrlPath = ""
        self.arctilePostIndex = 1
        self.sy_value = ''
        self.sy_keyname = ''

    def user_info(self):
        u = f"http://{self.domnainHost}/haobaobao/user"
        r = ""
        try:
            r = safe_request("GET", u, headers=self.headers, proxies=proxies)
            rj = r.json()
            # print(r.text)
            if rj.get("errcode") == 0:
                print(
                    f"账号[{self.name}]获取信息成功，用户ID为 {r.json()['data']['userid']} 父级ID {r.json()['data']['pid']}"
                )
                return True
            else:
                print(
                    f"账号[{self.name}]获取用户信息失败，账号异常 或者 Cookie无效，请检测Cookie是否正确"
                )
                return False
        except:
            print(r.text)
            print(f"账号[{self.name}]获取用户信息失败,Cookie无效，请检测Cookie是否正确")
            return False

    def gold(self):
        r = ""
        try:
            u = f"http://{self.domnainHost}/haobaobao/workinfo"
            r = safe_request("GET", u, headers=self.headers, proxies=proxies)
            # print(r.json())
            rj = r.json()
            self.remain_gold = math.floor(
                int(rj.get("data").get("remain_gold")))
            self.remain = float(rj.get("data").get("remain"))
            if onlyDoInviteRewardJob and int(self.remain_gold) > 3000:
                print("✅ 账号[{self.name}]金币超过3000，停止阅读")
                return False
            print(
                f'账号[{self.name}] 今日已经阅读了{rj.get("data").get("dayreads")}篇文章 当前金币{rj.get("data").get("remain_gold")} 当前余额{self.remain}'
            )
            self.arctilePostIndex = int(rj.get("data").get("dayreads")) + 1
        except:
            print(f"账号[{self.name}]获取金币失败")
            return False

    def getKey(self):
        ukRes = None
        for i in range(10):
            u = f"http://{self.domnainHost}{self.readJumpPath}"
            # print("提示 getKey：", u)
            p = f""
            r = safe_request(
                "POST", u, headers=self.headers, data=p, verify=False, proxies=proxies
            )
            # print("getKey：", r.text)
            rj = r.json()
            domain = rj.get("data").get("domain")
            # print("请求中转页：", r.text)
            pp = parse_qs(urlparse(domain).query)
            hn = urlparse(domain).netloc
            ukRes = r.text
            for key, value in pp.items():
                if is_not_timestamp(value):
                    # print(f"{key}: {value}")
                    if len(value) and isinstance(value, (list, tuple)):
                        value = value[0]
                    self.sy_keyname = key
                    self.sy_value = value
                    break
            if not self.sy_value or not self.sy_keyname:
                print(f"账号[{self.name}] 初始化阅读参数失败，返回错误：{ukRes}")
                return
        time.sleep(0.5)
        r = safe_request(
            "GET",
            domain,
            headers={
                "Client-Ip": self.fakeIp,
                "X-Forwarded-For": self.fakeIp,
                "Remote_Addr": self.fakeIp,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "Host": None,
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "Content-Type": "text/html; charset=UTF-8",
                "User-Agent": self.userAgent
                or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
            },
            verify=False,
            proxies=proxies,
        )
        # <script src="https://image.hzysmyy.cn/yunsaoma/newproject/js/article.js?v4.0"></script>
        readJsVersion = extract_middle_text(r.text, "js/article.js?", '"')
        if readJsVersion:
            checkJsCodeChanged = (
                check_file_md5(
                    extract_middle_text(r.text, '<script src="', '"></scrip'),
                    "0674299674c2c54e4c9c8111012552a7",
                )
                == False
            )
            if (readJsVersion != "v11.0") or checkJsCodeChanged:
                print(
                    f"账号[{self.name}] 检测到接口版本发生变化，当前接口版本为：{readJsVersion}，拉响警报，台子搞事，要抓人了，开始撤退，退出程序 >> "
                )
                sys.exit(0)
            else:
                # print(f"账号[{self.name}] 阅读准备完成：{uk}，提取到的地址：{domain}")
                if mykkydReadPureLog == False:
                    print(
                        f"账号[{self.name}] 阅读准备成功，当前接口版本为：{readJsVersion} 即将开始阅读 ✅ ，阅读参数为：{self.sy_value}"
                    )
        else:
            resText = trimSpaceCharacters(r.text)
            getReadUrlStr = extract_middle_text(
                resText,
                trimSpaceCharacters("function read_jump_read() {"),
                trimSpaceCharacters(
                    "ocalStorage.setItem('art_start_time', art_start_time)"
                ),
            )
            if not getReadUrlStr:
                print(f"账号[{self.name}] 获取阅读返回页异常！", r.text)
                exit(0)
            checkGetPostUrlBeforeSignStr = ""
            self.getReadUrlPath = extract_middle_text(
                getReadUrlStr,
                trimSpaceCharacters('url: domain+"/'),
                trimSpaceCharacters("?time="),
            )
            if '"' in self.getReadUrlPath:
                self.getReadUrlPath = ""
            if not self.getReadUrlPath:
                self.getReadUrlPath = extract_middle_text(
                    getReadUrlStr,
                    trimSpaceCharacters('url: "'),
                    trimSpaceCharacters("?time="),
                )
                checkGetPostUrlBeforeSignStr = 'url: "'
            else:
                checkGetPostUrlBeforeSignStr = 'url: domain+"/'
            checkAddGoldUrlBeforeSignStr = ""
            addGoldStr = extract_middle_text(
                resText,
                trimSpaceCharacters("function getGold(time) {"),
                trimSpaceCharacters('$(".goldNum").html(res.data.gold);'),
            )
            self.addGoldPath = extract_middle_text(
                addGoldStr,
                trimSpaceCharacters('url: domain+"/'),
                trimSpaceCharacters("?time="),
            )
            if not self.addGoldPath:
                self.addGoldPath = extract_middle_text(
                    addGoldStr,
                    trimSpaceCharacters('url: "'),
                    trimSpaceCharacters("?time="),
                )
                checkAddGoldUrlBeforeSignStr = 'url: "'
            else:
                checkAddGoldUrlBeforeSignStr = 'url: domain+"/'
            # http://0f2bb1b650.t1713515229s.zach-iot.online/yd2.html?uk=e4bd143c3e2572da80c2dfd6e13e7a78&t=1713515256
            readApiVersion = extract_middle_text(
                resText,
                trimSpaceCharacters(
                    f'{checkGetPostUrlBeforeSignStr}{self.getReadUrlPath}?time="+ time +"&mysign=168&vs='
                ),
                trimSpaceCharacters(
                    f'&{self.sy_keyname}="+ {self.sy_keyname},'),
            )
            if readApiVersion:
                self.readApiVersion = readApiVersion
            # print(f'[{checkGetPostUrlBeforeSignStr}]',
            #       f'[{self.getReadUrlPath}]', f'[{self.readApiVersion}]', f'[{self.sy_keyname}]', f'[{self.sy_value}]')
            if (
                trimSpaceCharacters(
                    f'{checkGetPostUrlBeforeSignStr}{self.getReadUrlPath}?time="+ time +"&mysign=168&vs={self.readApiVersion}&{self.sy_keyname}="+ {self.sy_keyname},'
                )
                in resText
                and trimSpaceCharacters(
                    f'{checkAddGoldUrlBeforeSignStr}{self.addGoldPath}?time="+time+"&psign="+psign+"&{self.sy_keyname}="+{self.sy_keyname},'
                )
                in resText
                # and check_str_md5(
                #     extract_middle_text(
                #         resText, '<script type="text/javascript">', "</script>"
                #     ).replace(
                #         f'url: domain+"/wenzjks?time="+ time +"&mysign=168&vs=8.0&uk="+ uk,',
                #         f'url: domain+"/wenzjks?time="+ time +"&mysign=168&vs={self.readApiVersion}&uk="+ uk,',
                #     ),
                #     "f34ab3dd2d38a82baba3ac0a549407d9",
                # )
            ):
                print(
                    f"账号[{self.name}] 阅读准备完成，当前 加密代码hash值 与 预设值一致，加密内容未修改，可继续阅读 ✅ "
                )
            else:
                print(
                    f"账号[{self.name}] 检测到加密代码内容发生变化，拉响警报，台子搞事，要抓人了，开始撤退，退出程序 >> "
                )
                print(
                    "可能的报错信息，便于排查错误：",
                    checkGetPostUrlBeforeSignStr,
                    self.getReadUrlPath,
                )
                print(checkAddGoldUrlBeforeSignStr, self.addGoldPath)
                os._exit(0)
        time.sleep(3)
        h = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            # "Host": hn,
            "Origin": f"https://{hn}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "User-Agent": self.userAgent
            or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
        }
        return self.sy_keyname, h

    def read(self):
        global thirdPartnerApiUrl
        info = self.getKey()
        if len(info) == 0:
            print(f"账号[{self.name}]获取阅读参数失败，停止往后阅读！⚠️ ")
            return
        # print(info)
        time.sleep(2)
        self.retryReading = False
        while True:
            res = {"errcode": -1}
            # rawRes = ""
            refreshTime = 0
            while res["errcode"] != 0:
                self.retryReading = False
                timeStamp = str(ts())
                # mysign = hashlib.md5(
                #     (info[1]["Host"] + timeStamp + "Lj*?Q3#pOviW").encode()
                # ).hexdigest()
                self.params = {
                    "time": timeStamp,
                    "mysign": "168",
                    "vs": self.readApiVersion,
                    self.sy_keyname: self.sy_value,
                }
                u = ''
                if 'http' in self.getReadUrlPath:
                    u = self.getReadUrlPath
                else:
                    u = f"http://{info[1]['Host']}/{self.getReadUrlPath}"
                info[1]["Host"] = urlparse(u).hostname
                # print(u, self.params)
                # print(
                #     "阅读文章参数查看：",
                #     u,
                #     self.params,
                #     info,
                #     info[1]["Origin"].replace("https://", "").replace("/", ""),
                # )
                r = safe_request(
                    "GET",
                    u,
                    headers=info[1],
                    params=self.params,
                    verify=False,
                    timeout=60,
                    proxies=proxies,
                )
                print("-" * 50)
                # if mykkydReadPureLog == False:
                #     print(
                #    f"账号[{self.name}]第[{refreshTime+1}]次获取阅读文章[{self.sy_value}]目的页：{r.text}"
                # )
                # rawRes = r.text
                # print("获取文章阅读链接：", r.text)
                if r.text == "":
                    print(
                        f"账号[{self.name}]第[{refreshTime+1}]次获取第[{str(self.arctilePostIndex)}]篇阅读文章[{self.sy_value}]目的页失败，请检查网络或稍后再试"
                    )
                    return False
                if r.text and r.json()["errcode"] == 0:
                    res = r.json()
                    print(
                        f"账号[{self.name}]第[{refreshTime+1}]次获取第[{str(self.arctilePostIndex)}]篇阅读文章[{self.sy_value}]跳转链接成功：" + res.get(
                            "data", {}).get("link")
                    )
                else:
                    decoded_str = json.loads(r.text)
                    if decoded_str["msg"]:
                        print(
                            f"账号[{self.name}]第[{refreshTime+1}]次获取第[{str(self.arctilePostIndex)}]篇阅读文章[{self.sy_value}]跳转链接失败：{decoded_str['msg']}"
                        )
                        if self.prevPostLink and "阅读暂时无效" in decoded_str["msg"]:
                            # self.report_check_post(self.prevPostLink)
                            print(f'节省电费和带宽，已停用在线接口服务，请私信或者在群里反馈被限制的文章链接！')
                        return False
                    else:
                        print(
                            f"账号[{self.name}]第[{refreshTime+1}]次获取第[{str(self.arctilePostIndex)}]篇阅读文章[{self.sy_value}]跳转链接失败：{r.text}"
                        )
                        if self.prevPostLink and "阅读暂时无效" in r.text:
                            # self.report_check_post(self.prevPostLink)
                            print(f'节省电费和带宽，已停用在线接口服务，请私信或者在群里反馈被限制的文章链接！')
                time.sleep(1.5)
                refreshTime = refreshTime + 1
                if refreshTime >= 5:
                    print(
                        f"⚠️ 账号[{self.name}]多次获取阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}]超时……"
                    )
                    return
            wechatPostLink = ""
            # print("获取文章数据：", res)
            if res.get("errcode") == 0:
                returnLink = ""
                try:
                    returnLink = res.get("data").get("link")
                except Exception as e:
                    errorMsg = res.get("data")
                    # print("1报错：", e)
                    # print("1返回：", rawRes)
                    if "404 Not Found" in errorMsg:
                        errorMsg = "台子接口不行，崩了~"
                        self.retryReading = True
                        print(
                            f"⚠️ 账号[{self.name}]获取阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}]链接失败，疑似台子接口太垃圾，崩了，返回数据为：",
                            errorMsg,
                        )
                        break
                    print(
                        f"⚠️ 账号[{self.name}]获取阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}]链接失败，疑似台子接口太垃圾，崩了，返回数据为：",
                        errorMsg,
                    )
                    continue
                if "mp.weixin.qq.com" in returnLink:
                    if mykkydReadPureLog == False:
                        print(
                            f"账号[{self.name}] 阅读第[{str(self.arctilePostIndex)}]篇微信文章：{returnLink}"
                        )
                    wechatPostLink = returnLink
                else:
                    # print(f"账号[{self.name}] 阅读第[{arctileTime}]篇文章准备跳转：{link}")
                    wechatPostLink = self.jump(returnLink)
                    if mykkydReadPureLog == False:
                        print(
                            f"账号[{self.name}] 阅读第[{str(self.arctilePostIndex)}]篇微信文章"
                        )
                if mykkydReadPureLog == False:
                    print(
                        f"账号[{self.name}] 阅读第[{str(self.arctilePostIndex)}]篇文章：{wechatPostLink}"
                    )
                # postInfo = getinfo(wechatPostLink)
                # if postInfo == False:
                #     print(
                #         f"⚠️ 账号[{self.name}]因 获取公众号文章信息不成功，导致阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}] 失败……"
                #     )
                #     return False
                if "__biz=" in wechatPostLink:
                    self.prevPostLink = wechatPostLink
                sleepTime = random.randint(7, 10)
                # 如果是检测特征到的文章 或者 后一篇文章与前一篇相似
                if (
                    self.confirm_check_post(wechatPostLink)
                    or int(self.arctilePostIndex) in checkPostIds
                ):
                    sleepTime = readPostDelay or random.randint(15, 20)
                    print(
                        f"⚠️ 账号[{self.name}]阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}] 检测到疑似检测文章，正在推送，等待过检测，等待时间：{sleepTime}秒。。。"
                    )
                    global link_cache
                    # fetch_wx_time_and_record(wechatPostLink, link_cache)
                    if thirdPartnerApiUrl:
                        push_to_third_party(wechatPostLink)
                    if self.wechatBussinessKey:
                        pushWechatBussiness(
                            self.wechatBussinessKey, wechatPostLink)
                    elif self.appToken:
                        push(
                            self.appToken,
                            self.topicIds,
                            "猫猫看看阅读过检测",
                            wechatPostLink,
                            f"账号[{self.name}]阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}] 正在等待过检测，等待时间：{sleepTime}秒\n幻生提示：快点，别耽搁时间了！",
                            "mykkyd",
                        )
                    else:
                        if not thirdPartnerApiUrl:
                            print(
                                f"⚠️ 账号[{self.name}]阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}] 需要过检测，但是未配置推送token，为了避免黑号，停止阅读。。。"
                            )
                            return False
                else:
                    print(
                        f"✅ 账号[{self.name}]阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}] 非检测文章，模拟读{sleepTime}秒"
                    )
                time.sleep(sleepTime)
                addGoldPath = ''
                if 'http' in self.addGoldPath:
                    addGoldPath = self.addGoldPath
                else:
                    addGoldPath = f"http://{info[1]['Host']}/{self.addGoldPath}"
                u1 = f"{addGoldPath}?time={sleepTime}&psign={random.randint(1, 1000)}&{self.sy_keyname}={self.sy_value}"
                r1 = safe_request(
                    "GET", u1, headers=info[1], verify=False, proxies=proxies
                )
                try:
                    # print("增加金币：", u1, info[1], r1.text)
                    if r1.text and r1.json():
                        try:
                            print(
                                f"✅ 账号[{self.name}] 阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}]所得金币：{r1.json()['data']['gold']}个，账户当前金币：{r1.json()['data']['last_gold']}个，今日已读：{r1.json()['data']['day_read']}次，今日未读 {r1.json()['data']['remain_read']}篇文章"
                            )
                            if (
                                onlyDoInviteRewardJob
                                and int(r1.json()["data"]["last_gold"]) > 3000
                            ):
                                print("✅ 账号[{self.name}]金币超过3000，停止阅读")
                                break
                        except Exception as e:
                            print(
                                f"❌ 账号[{self.name}] 阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}]异常：{r1.json().get('msg')}"
                            )
                            if "本次阅读无效" in r1.json().get("msg"):
                                continue
                            else:
                                break
                    else:
                        print(
                            f"❌ 账号[{self.name}] 阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}]失败：{r1.text}"
                        )
                        break
                except Exception as e:
                    # print("2报错：", e)
                    # print("2返回：", r1.text)
                    errorMsg = r1.text
                    if "404 Not Found" in errorMsg:
                        errorMsg = "台子接口不行，崩了~"
                        self.retryReading = True
                        print(
                            f"⚠️ 账号[{self.name}] 阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}]异常，返回数据为：",
                            errorMsg,
                        )
                        break
                    print(
                        f"⚠️ 账号[{self.name}] 阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}]异常，返回数据为：",
                        errorMsg,
                    )
                    continue
            elif res.get("errcode") == 405:
                print(
                    f"⚠️ 账号[{self.name}] 阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}]阅读重复"
                )
                time.sleep(1.5)
            elif res.get("errcode") == 407:
                print(
                    f"⚠️ 账号[{self.name}] 阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}]阅读结束"
                )
                return True
            else:
                print(
                    f"⚠️ 账号[{self.name}] 阅读第[{str(self.arctilePostIndex)}]篇文章[{self.sy_value}]未知情况"
                )
                time.sleep(1.5)
            self.arctilePostIndex = self.arctilePostIndex + 1

    def report_check_post(self, link):
        global machine_code
        global hs_api_origin, hs_api_aes_key, hs_api_aes_iv
        u = f"{hs_api_origin}/api/hs-public/report-check-post"
        p = {
            "encData": aes_encrypt(
                json.dumps({"url": link, "type": "mykkyd"}),
                hs_api_aes_key,
                hs_api_aes_iv,
            )
        }
        r = safe_request(
            "POST",
            u,
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Type": "application/json;charset=UTF-8",
                "req-machine-fp": machine_code,
                "card-secret": hs_api_card,
            },
            json=p,
            verify=False,
            proxies=proxies,
        )
        print(f"✅ 账号[{self.name}] 上传检测文章成功，下次就能识别它为检测文章啦！")

    def get_wx_offical_by_url(self, link):
        try:
            r = safe_request("GET", link, verify=False)
            # print(link, r.text)
            html = re.sub("\s", "", r.text)
            biz = re.findall('varbiz="(.*?)"\|\|', html)
            if biz != []:
                biz = biz[0]
            if biz == "" or biz == []:
                if "__biz" in link:
                    biz = re.findall("__biz=(.*?)&", link)
                    if biz != []:
                        biz = biz[0]
            nickname = re.findall('varnickname=htmlDecode\("(.*?)"\);', html)
            if nickname != []:
                nickname = nickname[0]
            user_name = re.findall('varuser_name="(.*?)";', html)
            if user_name != []:
                user_name = user_name[0]
            msg_title = re.findall("varmsg_title='(.*?)'\.html\(", html)
            if msg_title != []:
                msg_title = msg_title[0]
            text = ""
            text = f"公众号唯一标识：{biz}|文章:{msg_title}|作者:{nickname}|账号:{user_name}"
            print(text)
            return biz
        except Exception as e:
            # print(e)
            print("❌ 提取文章信息失败")
            return False

    def extract_biz_value(self, url):
        try:
            # 解析URL
            parsed_url = urllib.parse.urlparse(url)
            # 提取查询参数
            query_params = urllib.parse.parse_qs(parsed_url.query)
            # 获取__biz的值
            biz_value = query_params.get("__biz", [None])[0]
            return biz_value
        except Exception as e:
            print(f"Error: {e}")
            return None

    def confirm_check_post(self, link):
        check_from_api = False
        if not check_from_api:
            find_biz = self.extract_biz_value(link)
            if "mp.weixin.qq.com" in link:
                if not find_biz:
                    find_biz = self.get_wx_offical_by_url(link)
            return find_biz in check_bizs
        global machine_code
        global hs_api_origin, hs_api_aes_key, hs_api_aes_iv
        u = f"{hs_api_origin}/api/hs-public/confirm-check-post"
        p = {
            "encData": aes_encrypt(
                json.dumps({"url": link, "type": "mykkyd"}),
                hs_api_aes_key,
                hs_api_aes_iv,
            )
        }
        r = safe_request(
            "POST",
            u,
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Type": "application/json;charset=UTF-8",
                "req-machine-fp": machine_code,
                "card-secret": hs_api_card,
            },
            json=p,
            verify=False,
            proxies=proxies,
        )
        # print(r.json())
        if 'Invalid or expired card secret' in r.json().get('message', ''):
            print("⚠️ 999999次的免费卡密失效，疑似被人刷接口，卡密次数清空了，请群里反馈，重新获取接口卡密")
            exit(0)
        # print(f"✅ 账号[{self.name}] 当前文章为检测文章！")
        return r.json().get("status")

    # checkDict.get(postInfo[4]) != None
    #                 # or ("&idx=1" not in wechatPostLink)
    #                 or ("&idx=7" in wechatPostLink)
    #                 or ("&idx=5" in wechatPostLink)
    #                 or (res.get("data").get("a") == 2)
    #                 or ("&chksm=" in wechatPostLink)
    #                 or int(self.arctilePostIndex) in checkPostIds

    def jump(self, link):
        print(f"账号[{self.name}]开始本次阅读……")
        hn = urlparse(link).netloc
        h = {
            "Host": hn,
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.userAgent
            or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh",
            "Cookie": self.Cookie,
            "Client-Ip": self.fakeIp,
            "X-Forwarded-For": self.fakeIp,
            "Remote_Addr": self.fakeIp,
        }
        r = safe_request(
            "GET", link, headers=h, allow_redirects=False, verify=False, proxies=proxies
        )
        # print(r.status_code)
        Location = r.headers.get("Location")
        print(f"账号[{self.name}]开始阅读文章 - {Location}")
        return Location

    def withdrawPost(self):
        u = f"http://{self.domnainHost}/haobaobao/getwithdraw"
        p = f"signid={self.request_id}&ua=0&ptype=0&paccount=&pname="
        if self.aliAccount and self.aliName:
            p = f"signid={self.request_id}&ua=2&ptype=1&paccount={quote(self.aliAccount)}&pname={quote(self.aliName)}"
        r = safe_request(
            "POST",
            u,
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Cookie": self.Cookie,
                "Host": f"{self.domnainHost}",
                "Origin": f"http://{self.domnainHost}",
                "Proxy-Connection": "keep-alive",
                "Referer": f"http://{self.domnainHost}/haobaobao/withdraw",
                "X-Requested-With": "XMLHttpRequest",
                "Client-Ip": self.fakeIp,
                "X-Forwarded-For": self.fakeIp,
                "Remote_Addr": self.fakeIp,
            },
            data=p,
            verify=False,
            proxies=proxies,
        )
        print(f"✅ 账号[{self.name}] 提现结果：", r.json()["msg"])

    def withdraw(self):
        gold = int(int(self.remain_gold) / 1000) * 1000
        print(f"账号[{self.name}] 本次提现金额 ", self.remain, "元 ", gold, "金币")
        withdrawBalance = round((int(self.txbz) / 10000), 3)
        if gold or (self.remain >= withdrawBalance):
            if gold and ((float(self.remain) + gold / 10000) <= 30):
                # 开始提现
                # 以下逻辑没用，不管你gold为多少，它都是全部兑换
                # maxCanExchangeGold = (29.9 - self.remain) * 10000
                # if maxCanExchangeGold > 0:
                #     gold = min(maxCanExchangeGold, gold)
                #     print(f"账号[{self.name}] 为避免超过三十块，本次兑换金币数为 ", gold, "金币")
                u1 = f"http://{self.domnainHost}/haobaobao/getgold"
                p1 = f"request_id={self.request_id}&gold={gold}"
                r = safe_request(
                    "POST",
                    u1,
                    data=p1,
                    headers={
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "Cookie": self.Cookie,
                        "Host": f"{self.domnainHost}",
                        "Origin": f"http://{self.domnainHost}",
                        "Proxy-Connection": "keep-alive",
                        "Referer": f"http://{self.domnainHost}/haobaobao/withdraw",
                        "User-Agent": self.userAgent
                        or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                        "X-Requested-With": "XMLHttpRequest",
                        "Client-Ip": self.fakeIp,
                        "X-Forwarded-For": self.fakeIp,
                        "Remote_Addr": self.fakeIp,
                    },
                    verify=False,
                    proxies=proxies,
                )
                try:
                    res = r.json()
                    if res.get("errcode") == 0:
                        withdrawBalanceNum = self.remain + \
                            float(res["data"]["money"])
                        print(
                            f"✅ 账号[{self.name}] 金币兑换为现金成功，开始提现，预计到账 {withdrawBalanceNum} 元 >>> "
                        )

                        if withdrawBalanceNum < withdrawBalance:
                            print(
                                f"账号[{self.name}]没有达到提现标准 {withdrawBalance} 元"
                            )
                            return False
                        self.withdrawPost()
                        return
                    else:
                        print(
                            f"账号[{self.name}] 金币兑换为现金失败：",
                            r.text,
                            " 提现地址：",
                            u1,
                            " 提现参数：",
                            p1,
                        )
                except Exception as e:
                    # raise e
                    # 处理异常
                    print(f"账号[{self.name}] 提现失败：", e)
            self.withdrawPost()

    def init(self):
        try:
            r = safe_request(
                "GET",
                getNewInviteUrl(),
                headers={
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": self.userAgent
                    or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": self.Cookie,
                    "Client-Ip": self.fakeIp,
                    "X-Forwarded-For": self.fakeIp,
                    "Remote_Addr": self.fakeIp,
                },
                verify=False,
                # 禁止重定向
                allow_redirects=False,
                proxies=proxies,
            )
            self.domnainHost = r.headers.get("Location").split("/")[2]
            # print(r.text)
            if mykkydReadPureLog == False:
                print(f"账号[{self.name}]提取到的域名：{self.domnainHost}")
            # self.headers = {
            #     "Connection": "keep-alive",
            #     "Accept": "application/json, text/javascript, */*; q=0.01",
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090621) XWEB/8351 Flue",
            #     "X-Requested-With": "XMLHttpRequest",
            #     "Referer": f"http://{self.domnainHost}/",
            #     "Origin": f"http://{self.domnainHost}",
            #     # "Host": f"{self.domnainHost}",
            #     "Accept-Encoding": "gzip, deflate",
            #     "Accept-Language": "zh-CN,zh",
            #     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            #     "Cookie": self.Cookie,
            # }
            # # 获取requestId
            self.readJumpPath = ""
            if mykkydDetectingSealStatus:
                r = safe_request(
                    "GET",
                    f"http://{self.domnainHost}/haobaobao/home",
                    headers={
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": self.userAgent
                        or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cookie": self.Cookie,
                        "Client-Ip": self.fakeIp,
                        "X-Forwarded-For": self.fakeIp,
                        "Remote_Addr": self.fakeIp,
                    },
                    verify=False,
                    proxies=proxies,
                )
                htmltext = r.text
                read_jump_read_text = extract_middle_text(
                    htmltext, "function read_jump_read(){", "success: function"
                )
                if read_jump_read_text:
                    readJumpPath = extract_middle_text(
                        read_jump_read_text, "url: domain+'", "',"
                    )
                    if readJumpPath:
                        self.readJumpPath = readJumpPath
                    else:
                        if "直接提" not in self.name:
                            print(
                                f"账号[{self.name}] 初始化失败，请手动访问下确认页面没崩溃 或者 稍后再试吧，一直不行，请前往TG群反馈~ "
                            )
                            return False
                else:
                    hiddenTipText = extract_middle_text(
                        htmltext, '<!-- <p style="color:red">', "<br>"
                    )
                    # 移除掉注释的公告部分
                    htmltext = htmltext.replace(
                        '<!-- <p style="color:red">' + hiddenTipText + "<br>", ""
                    )
                    tipText = extract_middle_text(
                        htmltext, '<p style="color:red">', "<br>"
                    )
                    if "直接提" not in self.name:
                        if "存在违规操作" in htmltext:
                            print(
                                f"账号[{self.name}] 被检测到了，已经被封，终止任务，快去提醒大家吧~ "
                            )
                            return False
                        elif "系统维护中" in tipText:
                            # <p style="color:red">系统维护中，预计周一恢复，与码无关！<br>
                            print(
                                f"账号[{self.name}] 检测到系统维护中，公告内容为 [{tipText}] ，终止任务"
                            )
                            sys.exit(0)
                        else:
                            print(
                                f"账号[{self.name}] 初始化失败，请手动访问下确认页面没崩溃 或者 稍后再试吧，一直不行，请前往TG群反馈~ "
                            )
                            return False
            else:
                self.readJumpPath = "/haobaobao/wtmpdomain2"
            # # 获取提现页面地址
            r = safe_request(
                "GET",
                f"http://{self.domnainHost}/haobaobao/withdraw",
                headers={
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": self.userAgent
                    or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Cookie": self.Cookie,
                    "Client-Ip": self.fakeIp,
                    "X-Forwarded-For": self.fakeIp,
                    "Remote_Addr": self.fakeIp,
                },
                verify=False,
                proxies=proxies,
            )
            htmltext = r.text
            signidl = re.search('request_id = "(.*?)"', htmltext)
            if signidl == []:
                if mykkydReadPureLog == False:
                    print(
                        f"账号[{self.name}]初始化 提现参数 失败，尝试另一种初始化 >>> "
                    )
                r = safe_request(
                    "GET",
                    f"https://code.sywjmlou.com.cn/baobaocode.php",
                    verify=False,
                    proxies=proxies,
                )
                domnainHost = r.json()["data"]["luodi"].split("/")[2]
                r = safe_request(
                    "GET",
                    f"http://{domnainHost}/haobaobao/withdraw",
                    headers={
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": self.userAgent
                        or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309071d) XWEB/8461 Flue",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cookie": self.Cookie,
                        "Client-Ip": self.fakeIp,
                        "X-Forwarded-For": self.fakeIp,
                        "Remote_Addr": self.fakeIp,
                    },
                    verify=False,
                    proxies=proxies,
                )
                htmltext = r.text
                signidl = re.search('request_id = "(.*?)"', htmltext)
                if signidl == []:
                    print(
                        f"账号[{self.name}] 多次初始化 提现参数 失败, 账号异常，请检查Cookie！"
                    )
                    r = safe_request(
                        "GET",
                        f"https://code.sywjmlou.com.cn/baobaocode.php",
                        verify=False,
                        proxies=proxies,
                    )
                    self.domnainHost = r.json()["data"]["luodi"].split("/")[2]
                    return False
                else:
                    self.request_id = signidl[1]
            else:
                self.request_id = signidl[1]
            return True
        except Exception as e:
            # raise e
            print(f"账号[{self.name}]初始化失败,请检查你的ck")
            return False

    def run(self):
        if self.init():
            self.user_info()
            if self.gold() == False:
                return
            if "直接提" not in self.name:
                self.read()
                # 如果接口崩了，就尝试三次重启阅读
                if self.retryReading == True:
                    if mykkydReadPureLog == False:
                        print(f"账号[{self.name}] 检测到阅读接口异常，尝试重试~")
                    for i in range(3):
                        self.read()
                        # 随机延迟
                        time.sleep(random.random() * 3 + 1)
                        if self.retryReading == False:
                            break
                time.sleep(3)
                if self.gold() == False:
                    return
            if onlyDoInviteRewardJob == False:
                time.sleep(3)
                self.withdraw()


def getNewInviteUrl():
    r = safe_request(
        "GET", "https://code.sywjmlou.com.cn/baobaocode.php", verify=False
    ).json()
    if r.get("code") == 0:
        newEntryUrl = r.get("data").get("luodi")
        parsed_url = urlparse(newEntryUrl)
        host = parsed_url.hostname
        return f"http://t51.17365231287fs.xrm6qy8i.cyou/kstief/2093a8936e8ab34e3a10c5b783b6a407?tsd=654".replace(
            "t51.17365231287fs.xrm6qy8i.cyou", host or "t51.17365231287fs.xrm6qy8i.cyou"
        )
    else:
        return "http://t51.17365231287fs.xrm6qy8i.cyou/kstief/2093a8936e8ab34e3a10c5b783b6a407?tsd=654"


def is_user_agent(s):
    pattern = r"^Mozilla\/5\.0 \(.*\) Gecko\/[0-9]{8} Firefox\/[0-9.]+$"
    return bool(re.match(pattern, s))


def main(account, forceAlipayName="", forceAlipayAccount=""):
    global thirdPartnerApiUrl
    # print("\n")
    # print("-" * 50)
    # print(f"账号[{account.split('#')[0]}]开始执行任务 >>>")
    # print("\n")
    # 按@符号分割当前账号的不同参数
    values = account.split("#")
    # print(values)
    cg = {}
    try:
        if len(values) == 2:
            cg = {
                "name": values[0],
                "Cookie": values[1],
                "txbz": 3000,
                "aliAccount": forceAlipayAccount or "",
                "aliName": forceAlipayName or "",
                "userAgent": "",
            }
        else:
            cg = {
                "name": values[0],
                "Cookie": values[1],
                "txbz": values[2] or 3000,
                "aliAccount": forceAlipayAccount or "",
                "aliName": forceAlipayName or "",
                "userAgent": "",
            }
    except Exception as e:
        # 处理异常
        print("幻生逼逼叨:", "配置的啥玩意，缺参数了憨批，看清脚本说明！")
    cg["appToken"] = wxpusherAppToken or ""
    cg["topicIds"] = wxpusherTopicId or ""
    # print("手动：", len(values), values[4])
    if len(values) >= 4:
        if values[3]:
            cg["appToken"] = values[3]
    if len(values) >= 5:
        if values[4]:
            cg["topicIds"] = values[4]
    if len(values) >= 6:
        if values[5] and is_user_agent(values[5]):
            cg["userAgent"] = values[5]
        else:
            cg["aliName"] = values[5]
    if len(values) >= 7:
        if values[6]:
            cg["aliAccount"] = values[6]
    if len(values) >= 8:
        if values[6]:
            cg["userAgent"] = values[7]
    try:
        if wechatBussinessKey == "" and thirdPartnerApiUrl == "":
            if cg["appToken"].startswith("AT_") == False:
                print(
                    f"幻生提示，账号[{account.split('#')[0]}] wxpush 配置错误，快仔细看头部说明！"
                )
            if (cg["appToken"].startswith("AT_") == False) or (
                cg["topicIds"].isdigit() == False
            ):
                print(
                    f"幻生提示，账号[{account.split('#')[0]}] wxpush 配置错误，快仔细看头部说明！"
                )
        api = MMKKYD(cg)
        if cg["aliName"] and cg["aliAccount"]:
            print(
                f"幻生提示，账号[{account.split('#')[0]}] 采用了 支付宝提现，姓名：{cg['aliName']}，账户：{cg['aliAccount']}"
            )
        else:
            print(f"幻生提示，账号[{account.split('#')[0]}] 采用了 微信提现")
        try:
            api.run()
        except Exception as e:
            raise e
            print(f"幻生提示，账号[{account.split('#')[0]}] 执行出错：", e)
    except Exception as e:
        raise e
        print(
            f"幻生提示，账号[{account.split('#')[0]}] 出错啦，也许是平台接口问题，可以过一会尝试重新运行，如果还是不行，请将下面报错截图发到tg交流群:"
        )
        # raise e
    # print("\n")
    # print("-" * 50)
    # print(f"账号[{account.split('#')[0]}]执行任务完毕！")
    # print("\n")


if __name__ == "__main__":
    # 获取当前文件的名称
    filename = Path(__file__).name
    print(f'======== ▷ 开始启动脚本 ◁ ========\n当前脚本：{filename} 🤪')
    # appToken：这个是填wxpusher的appToken
    # topicIds：这个是wxpusher的topicIds改成你自己的
    accounts = os.getenv("mykkyd")
    inviteUrl = getNewInviteUrl()
    if accounts is None:
        print(f"你没有填入mykkyd，咋运行？\n走下邀请呗：{inviteUrl}")
    else:
        # 获取环境变量的值，并按指定字符串分割成多个账号的参数组合
        accounts_list = os.environ.get("mykkyd").split("&")

        # 输出有几个账号
        num_of_accounts = len(accounts_list)
        moreTip = ""
        if readPostDelay > 0:
            moreTip = f"已设置的推送文章等待点击时间为 {readPostDelay}秒 "
        get_announce()
        get_lastest_version(filename)
        announce_content = f'''活动入口[微信打开]：{inviteUrl}\n\n=============================================================\n'''
        print(
            f"幻生提示：获取到 {num_of_accounts} 个账号 {moreTip}"
        )
        if thirdPartnerApiUrl:
            print(f"配置了第三方检测回调地址：{thirdPartnerApiUrl}")
        USE_THREADS = 1
        if os.environ.get("mykkydConcurrency"):
            USE_THREADS = int(os.environ.get("mykkydConcurrency")) or 1
            print(f"已开启多线程模式，线程数为：{USE_THREADS}")
        print(announce_content)
        # 遍历所有账号
        if USE_THREADS <= 1:
            for i, account in enumerate(accounts_list, start=1):
                main(account)
        else:
            with ThreadPoolExecutor(max_workers=USE_THREADS) as executor:
                for i, account in enumerate(accounts_list):
                    # 为每个账号创建一个线程，注意传递参数的方式需要是元组，即使只有一个参数
                    executor.submit(main, account)
