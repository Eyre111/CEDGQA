import requests
import json
import re
import pandas as pd
import time
import codecs

#urls = []
titles = []
answers = []
have_answers = []
ID = []
num =0

def fetchHotel(url):
    # 发起网络请求，获取数据
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    }

    # 发起网络请求
    r = requests.get(url, headers=headers)
    time.sleep(10)
    r.encoding = 'utf-8'
    #print(r.text)
    return r.text


def parseJson(text):

    # 解析json数据
    json_data = json.loads(text)
    lst = json_data['data']
    #print(lst)
    nextUrl = json_data['paging']['next']
    #print(nextUrl)

    if not lst:
        return;

    for item in lst:
        type = item['target']['type']
        id = ''
        title = ''
        #url = ''
        answer = ''

        if type == 'answer' or  type == 'quesion':
            # 回答
            question = item['target']['question']
            id = question['id']
            title = question['title']
            #url = 'https://www.zhihu.com/question/' + str(id)
            content = item['target']['content']
            answer = parseAnwser(content)
            #print("问题：", url, title)
            '''
        elif type == 'article':
            # 专栏
            zhuanlan = item['target']
            # id = zhuanlan['id']
            title = zhuanlan['title']
            url = zhuanlan['url']
            # vote = zhuanlan['voteup_count']
            # cmts = zhuanlan['comment_count']
            # auth = zhuanlan['author']['name']
            content = zhuanlan['content']
            answer = parseAnwser(content)
            print("专栏：", url, title)
            '''

        # print(answer)
        #urls.append(url)
        ID.append(id)
        titles.append(title)
        answers.append(answer)
        if (answer == ''):
            have_answers.append("false")
        else:
            have_answers.append("true")

    #print()
    return nextUrl

#将html字符串转化为纯文本
def parseAnwser(content):
    left_iter = re.finditer('<',content)
    right_iter = re.finditer('>',content)
    left_list = []
    right_list = []
    for i in left_iter:
        left_list.append(i.span()[0])
    for i in right_iter:
        right_list.append(i.span()[0])

    length = len(left_list)

    left_list.append(len(content))
    right_list.insert(0,0)
    # print()

    answer = ""
    for i in range(length):
        left = left_list[i]
        right = right_list[i]
        # print(content[right+1:left])
        answer += content[right+1:left]
        # print(answer)
    # print(answer)
    return answer



if __name__ == '__main__':
    # 主要修改topicID
    topicID =[]
    with open('话题ID.txt','r+',encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            topicID.append(line.split('：',1))
    #topicID = '20689557'  # 地理话题的id
    # essence 对应精华
    # top_activity 对应讨论
    #https://www.zhihu.com/api/v4/topics/19553622/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&after_id=0
    for i in topicID:
        url = 'https://www.zhihu.com/api/v4/topics/' + i[1] + '/feeds/top_activity?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&after_id=0'              
        while url:
            text = fetchHotel(url)
            url = parseJson(text)
        print(i[0])
    
    df = pd.DataFrame(
        {
            'ID':ID,
            'question':titles,
            'answer':answers,
            'hasAnswer':have_answers
        }
    )
    print(len(df))
    df.drop_duplicates(subset='question',keep='first',inplace=True)
    data = df.to_json(orient = 'records',force_ascii=False)
    data = json.loads(data)
    file=codecs.open('question.txt','a+',encoding='utf-8')
    with open("zhihu.json","a+", encoding='utf-8') as f:
        for item in data:
            #print(type(item))
            if item['ID'] != '':
                line = json.dumps(item,ensure_ascii=False)
                f.write(line+'\n')
                file.writelines(item['question'])
                file.write('\n')

