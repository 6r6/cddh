# coding: utf-8
import os
from PIL import Image
import pytesseract
import webbrowser

box = (100,400,1400,700) #剪裁图片位置，数据基于1440*2560分辨率的三星S6(G920F直面屏)


def pull_screenshot():
    os.system('adb shell screencap -p /sdcard/2.png')
    os.system('adb pull /sdcard/2.png .')


def main():
    while input("任意键开始识别(0 退出) : ") != '0':
        pull_screenshot()
        img2 = Image.open("./2.png")
		#剪裁图片，加快识别速度
        img = img2.crop(box)
        #如果不知道如何设置剪裁参数，请将下面这一行的img改成img2
        text=pytesseract.image_to_string(img,lang='chi_sim')
        text=text.replace(' ','').replace('\n','')
        text=text[text.find('.') + 1:text.find('?')]
        webbrowser.open("https://www.baidu.com/s?ie=UTF-8&wd=" + text)
		#webbrowser.open("https://cn.bing.com/search?q=" + text)

if __name__ == '__main__':
    main()