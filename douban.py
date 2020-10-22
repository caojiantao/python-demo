import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla"
    }
    response = requests.get("https://movie.douban.com/top250", headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.content, "html.parser")
    elementList = soup.select("ol[class='grid_view'] li")
    movieList = []
    for item in elementList:
        # 图片
        img = item.select(".pic img")[0]["src"]
        # 标题
        title = item.select(".title")[0].string
        # 描述
        quote = item.select(".inq")[0].string
        print(title, img, quote)