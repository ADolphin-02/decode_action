
import sys
if 10 != int(sys.version.split(" ", 1)[0].split('.')[1]):
    print(f'当前pyhton版本是{sys.version.split(" ", 1)[0]},请下载相应版本的脚本')
    exit(0)
import zlib
import gzip
import bz2
import lzma
import base64
import marshal
import datetime
import json
import os
import random
import threading
import time
import traceback
import requests
