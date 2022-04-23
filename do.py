# coding: utf-8
# quote from kmaiya/HQAutomator
# 谷歌搜索部分原版搬运，未做修改

import time
import json
import requests
from googleapiclient.discovery import build

g_cse_id = ''
g_cse_api_key = ''

questions = []


def google_search(query, start):
    service = build("customsearch", "v1", developerKey=g_cse_api_key)
    res = service.cse().list(q=query, cx=g_cse_id, start=start).execute()
    return res

# Google Question and count number of each result
def metric1Func(question, answers):
    met1 = [0, 0, 0]
    res = google_search(question, None)
    items = str(res['items']).lower()
    met1[0] = items.count(answers[0].lower())
    met1[1] = items.count(answers[1].lower())
    met1[2] = items.count(answers[2].lower()) 
    return met1


# Google Question and each specific Answer and count total results
def metric2Func(question, answers):
    met2 = [0, 0, 0]
    res0 = google_search(question + ' "' + answers[0] + '"', None)
    res1 = google_search(question + ' "' + answers[1] + '"', None)
    res2 = google_search(question + ' "' + answers[2] + '"', None)
    return [int(res0['searchInformation']['totalResults']), int(res1['searchInformation']['totalResults']), int(res2['searchInformation']['totalResults'])]


def predict(metric1, metric2, answers):
    max1 = metric1[0]
    max2 = metric2[0]
    for x in range(1, 3):
        if metric1[x] > max1:
            max1 = metric1[x]
        if metric2[x] > max2:
            max2 = metric2[x]
    if metric1.count(0) == 3:
        return answers[metric2.index(max2)]
    elif metric1.count(max1) == 1:
        if metric1.index(max1) == metric2.index(max2):
            return answers[metric1.index(max1)]
        else:
            percent1 = max1 / sum(metric1)
            percent2 = max2 / sum(metric2)
            if percent1 >= percent2:
                return answers[metric1.index(max1)]
            else:
                return answers[metric2.index(max2)]
    elif metric1.count(max1) == 3:
        return answers[metric2.index(max2)]
    else:
        return answers[metric2.index(max2)]


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
            answers = eval(resp_dict['data']['event']['options'])
            met1 = metric1Func(question, answers)
            met2 = metric2Func(question, answers)
            return predict(met1, met2, answers)
        else:
            return 'Waiting for new question...'


def main():
    while True:
        print(time.strftime('%H:%M:%S',time.localtime(time.time())))
        print(get_answer())
        time.sleep(1)


if __name__ == '__main__':
    main()
