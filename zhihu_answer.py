
import json
import sqlite3
import time
from datetime import datetime
#下载自己点赞的动态https://zhuanlan.zhihu.com/p/360834359
import requests

headers = {
    "x-api-version": "3.0.40",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "x-requested-with": "fetch",
    "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    "accept": "*/*",
    "referer": "https://www.zhihu.com/people/kongyifei",
    "accept-language": "en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7",
    "cookie": '这里需要自己的 Cookie',
}


ended = False
url = "https://www.zhihu.com/api/v3/moments/kongyifei/activities?limit=7&desktop=true"
db = sqlite3.connect("zhihu.db")
c = db.cursor()
c.execute(
    """create table if not exists upvoted_answers (
    id integer primary key,
    time_upvoted datetime,
    author text,
    author_url text,
    comment_count integer,
    voteup_count integer,
    question text,
    answer text,
    url text,
    topic_ids text,
    time_created datetime,
    time_updated datetime
    );
    """
)

c.execute(
    """create table if not exists upvoted_articles (
    id integer primary key,
    time_upvoted datetime,
    author text,
    author_url text,
    comment_count integer,
    voteup_count integer,
    title text,
    content text,
    url text,
    image_url text,
    time_created datetime,
    time_updated datetime
    );
    """
)


while not ended:
    print(url)
    try:
        response = requests.get(url, headers=headers,)
        data = response.json()
    except Exception:
        print("connection blocked, wait for a few seconds...")
        time.sleep(5)
        continue
    ended = data["paging"]["is_end"]
    url = data["paging"].get("next", "")
    time.sleep(1)
    for item in data["data"]:
        if item["action_text"] not in ["赞同了回答", "赞同了文章"]:
            continue
        if item["action_text"] == "赞同了回答":
            upvote = dict(
                time_upvoted=item["created_time"],
                author=item["target"]["author"].get("name"),
                author_url="https://zhihu.com/people/" + item["target"]["author"].get("id", ""),
                comment_count=item["target"]["comment_count"],
                voteup_count=item["target"]["voteup_count"],
                question=item["target"]["question"]["title"],
                answer=item["target"]["content"],
                url="https://zhihu.com/question/%s/answer/%s"
                % (item["target"]["question"]["id"], item["target"]["id"]),
                topic_ids=json.dumps(item["target"]["question"]["bound_topic_ids"]),
                time_created=item["target"]["created_time"],
                time_updated=item["target"]["updated_time"]
            )

            c.execute(
                "insert into upvoted_answers"
                "(time_upvoted, author, author_url, comment_count, question, "
                "answer, url, voteup_count, topic_ids, time_created, time_updated)"
                "values"
                "(:time_upvoted, :author, :author_url, :comment_count, :question, "
                ":answer, :url, :voteup_count, :topic_ids, :time_created, :time_updated)",
                upvote,
            )
            print(
                datetime.fromtimestamp(upvote["time_upvoted"]).strftime("%Y-%m-%d"),
                upvote["question"],
            )
        elif item["action_text"] == "赞同了文章":
            upvote = dict(
                time_upvoted=item["created_time"],
                author=item["target"]["author"].get("name"),
                author_url="https://zhihu.com/people/" + item["target"]["author"].get("id", ""),
                comment_count=item["target"]["comment_count"],
                voteup_count=item["target"]["voteup_count"],
                title=item["target"]["title"],
                content=item["target"]["content"],
                url=item["target"]["url"],
                image_url=item["target"]["image_url"],
                time_created=item["target"]["created"],
                time_updated=item["target"]["updated"]
            )

            c.execute(
                "insert into upvoted_articles"
                "(time_upvoted, author, author_url, comment_count, title, content, "
                "url, voteup_count, image_url, time_created, time_updated)"
                "values"
                "(:time_upvoted, :author, :author_url, :comment_count, :title, :content, "
                ":url, :voteup_count, :image_url, :time_created, :time_updated)",
                upvote,
            )
            print(
                datetime.fromtimestamp(upvote["time_upvoted"]).strftime("%Y-%m-%d"),
                upvote["title"],
            )
        db.commit()

print("All set!")