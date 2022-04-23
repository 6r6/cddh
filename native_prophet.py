# coding: utf-8
# quote from kmaiya/HQAutomator
# 谷歌搜索部分原版搬运，未做修改

import time
import json
import requests
import webbrowser

questions = []


def get_answer():
    resp = requests.get('http://htpmsg.jiecaojingxuan.com/msg/current',timeout=4).text
    resp_dict = json.loads(resp)
    if resp_dict['msg'] == 'no data':
        return 'Waiting for question...'
    else:
        resp_dict = eval(str(resp))
        question = resp_dict['data']['event']['desc']
        question = question[question.find('.') + 1:question.find('?')]
        if question not in questions:
            questions.append(question)
            webbrowser.open("https://www.baidu.com/s?ie=UTF-8&wd=" + question)
        else:
            return 'Waiting for new question...'


def main():
    while True:
        print(time.strftime('%H:%M:%S',time.localtime(time.time())))
        print(get_answer())
        time.sleep(1)


if __name__ == '__main__':
    main()
