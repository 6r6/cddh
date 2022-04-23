# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

app.secret_key = '5sad^%$0asdas5nv%^55'


@app.route("/", methods=['POST', 'GET'])
@app.route("/index", methods=['POST', 'GET'])
def main_page():
    resp = requests.get('http://htpmsg.jiecaojingxuan.com/msg/current', timeout=3).text
    if 'no data' in resp:
        return render_template('main.html', question='等待出题...')
    elif 'questionId' in resp:
        resp_dict = eval(str(resp))
        question = resp_dict['data']['event']['desc']
        questionId = resp_dict['data']['event']['questionId']
        answers = eval(resp_dict['data']['event']['options'])
        return render_template('main.html', question=question, answer1=answers[0], answer2=answers[1], answer3=answers[2])
    else:
        return render_template('main.html', question='接口错误！')


if __name__ == '__main__':
    app.run('0.0.0.0')
