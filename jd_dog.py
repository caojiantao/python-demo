import json
import sys
import time

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

token = "CA1C77B096B3E990C416F106A9E272562A16EC6EE7E79C957B4ADF0EC8E7E428"
url = "https://api.m.jd.com/client.action"
headers = {
    "User-Agent": "Mozilla"
}
cookies = {
    "wq_auth_token": token
}
params = {
    "appid": "wh5",
    "loginType": "1",
    "loginWQBiz": "pet-town"
}


def get_result(function_id, body=None):
    params["functionId"] = function_id
    if body:
        params["body"] = json.dumps(body)
    response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False)
    response.encoding = "utf-8"
    content = json.loads(response.content)
    return content["result"] if "result" in content.keys() else None


if __name__ == '__main__':
    petTown = get_result("initPetTown")
    if not petTown:
        print("token 已失效")
        sys.exit()
    petPlaceInfoList = petTown["petPlaceInfoList"]
    if petPlaceInfoList:
        for item in petPlaceInfoList:
            if item["energy"] == 0:
                continue
            print("收集能量:", item["energy"])
            get_result("energyCollect", {"place": item["place"]})

    result = get_result("taskInit", {"version": 2, "channel": "hd"})
    print(result)
    # 去签到
    signInit = result["signInit"]
    if not signInit["finished"]:
        print("去签到")
        get_result("getSignReward")
    # 首次投喂
    firstFeedInit = result["firstFeedInit"]
    if not firstFeedInit["finished"]:
        print("首次投喂")
        get_result("feedPets")
        print("领取首次投喂奖励")
        get_result("getFirstFeedReward")
    # 去浏览
    browseList = []
    for item in result["taskList"]:
        if item.startswith("browseSingleShopInit"):
            browseList.append(item)
    if len(browseList) > 0:
        for item in browseList:
            browse = result[item]
            if not browse["finished"]:
                print("浏览广告：", browse["title"])
                get_result("getSingleShopReward", {"index": browse["index"], "version": 1, "type": 1})
                print("领取奖励：", browse["title"])
                get_result("getSingleShopReward", {"index": browse["index"], "version": 1, "type": 2})
    # 三餐领福袋
    threeMealInit = result["threeMealInit"]
    if not threeMealInit["finished"]:
        print("准备领取三餐福袋")
        threeMealInitResult = get_result("getThreeMealReward")
        print("领取三餐福袋成功：", threeMealInitResult["threeMealReward"])
    # 每日投喂达10次
    feedReachInit = result["feedReachInit"]
    if not feedReachInit["finished"]:
        print("准备循环投喂，领取10次奖励")
        index = 1
        sec = 5
        while True:
            feedPetsResult = get_result("feedPets")
            if feedPetsResult:
                print("第", index, "投喂成功，休眠", sec, "秒，等待下次投喂...")
                time.sleep(sec)
            else:
                break
        # 重新请求
        result = get_result("taskInit", {"version": 2, "channel": "hd"})
        feedReachInit = result["feedReachInit"]
        hadFeedAmount = feedReachInit["hadFeedAmount"]
        feedReachAmount = feedReachInit["feedReachAmount"]
        print("已经投喂", hadFeedAmount, "，目标是", feedReachAmount)
        if hadFeedAmount >= feedReachAmount:
            getFeedReachRewardResult = get_result("getFeedReachReward")
            print("领取投喂累计奖励：", getFeedReachRewardResult["reward"])
