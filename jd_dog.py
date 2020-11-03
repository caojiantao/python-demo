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
sec = 5


def get_result(function_id, body=None):
    params["functionId"] = function_id
    if body:
        params["body"] = json.dumps(body)
    response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False)
    response.encoding = "utf-8"
    content = json.loads(response.content)
    print(content)
    return content["result"] if "result" in content.keys() else None


def collect_energy():
    print("准备收集能量")
    pet_town = get_result("initPetTown")
    place_info_list = pet_town["petPlaceInfoList"]
    if not place_info_list:
        return None
    for place_info in place_info_list:
        if place_info["energy"] == 0:
            continue
        print("收集能量:", place_info["energy"])
        get_result("energyCollect", {"place": place_info["place"]})


if __name__ == '__main__':
    print("准备初始化JD宠物家园...")
    petTown = get_result("initPetTown")
    if not petTown:
        print("token 已失效")
        sys.exit()

    print("准备让狗狗运动领奖励...")
    while True:
        petSportResult = get_result("petSport")
        if not petSportResult:
            print("已达宠物运动次数上限")
            break
        print("休眠", sec, "秒，准备领取运动奖励...")
        time.sleep(sec)
        get_result("getSportReward", {"version": 1})
        if petSportResult["petSportStatus"] == 2:
            print("领取运动奖励：", petSportResult["foodReward"])
        else:
            break

    print("准备获取任务列表...")
    taskList = get_result("taskInit", {"version": 2, "channel": "hd"})
    print(taskList)

    # 去签到
    print("准备领取签到奖励...")
    signInit = taskList["signInit"]
    if not signInit["finished"]:
        getSignRewardResult = get_result("getSignReward")
        print("领取签到奖励：", getSignRewardResult["reward"])

    # 去浏览
    browseList = []
    for item in taskList["taskList"]:
        if item.startswith("browseSingleShopInit"):
            browseList.append(item)
    if len(browseList) > 0:
        for item in browseList:
            browse = taskList[item]
            if not browse["finished"]:
                print("浏览广告：", browse["title"])
                get_result("getSingleShopReward", {"index": browse["index"], "version": 1, "type": 1})
                getSingleShopRewardResult = get_result("getSingleShopReward",
                                                       {"index": browse["index"], "version": 1, "type": 2})
                print("领取奖励：", getSingleShopRewardResult["reward"])

    # 三餐领福袋
    threeMealInit = taskList["threeMealInit"]
    if not threeMealInit["finished"]:
        threeMealInitResult = get_result("getThreeMealReward")
        if threeMealInitResult:
            print("领取三餐福袋奖励：", threeMealInitResult["threeMealReward"])

    # 首次投喂
    firstFeedInit = taskList["firstFeedInit"]
    if not firstFeedInit["finished"]:
        get_result("feedPets")
        collect_energy()
        getFirstFeedRewardResult = get_result("getFirstFeedReward")
        print("领取首次投喂奖励：", getFirstFeedRewardResult["reward"])

    # 每日投喂达10次
    feedReachInit = taskList["feedReachInit"]
    if not feedReachInit["finished"]:
        print("准备循环投喂，领取累计投喂奖励")
        index = 1
        while True:
            feedPetsResult = get_result("feedPets")
            if feedPetsResult:
                collect_energy()
                print("第", index, "投喂成功，休眠", sec, "秒，等待下次投喂...")
                time.sleep(sec)
                index = index + 1
            else:
                break
        # 重新请求
        taskList = get_result("taskInit", {"version": 2, "channel": "hd"})
        feedReachInit = taskList["feedReachInit"]
        hadFeedAmount = feedReachInit["hadFeedAmount"]
        feedReachAmount = feedReachInit["feedReachAmount"]
        print("今日已经投喂", hadFeedAmount, "，目标是", feedReachAmount)
        if hadFeedAmount >= feedReachAmount:
            getFeedReachRewardResult = get_result("getFeedReachReward")
            print("领取投喂累计奖励：", getFeedReachRewardResult["reward"])

    # 准备收集能量
    collect_energy()
