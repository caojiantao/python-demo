import json
import sys

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
    "loginWQBiz": "ddnc"
}
sec = 5


def get_result(function_id, body=None):
    params["functionId"] = function_id
    if body:
        params["body"] = json.dumps(body)
    response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False)
    response.encoding = "utf-8"
    result = json.loads(response.content)
    print(result)
    return result


if __name__ == '__main__':
    print("================= start =================")

    print("准备获取JD果园任务列表...")
    taskList = get_result("taskInitForFarm")
    if not taskList:
        print("token 已失效")
        sys.exit()
    print(taskList)

    # 签到
    print("[签到]--- start ---")
    signResult = taskList["signInit"]
    if not signResult["todaySigned"]:
        res = get_result("clockInForFarm", {"type": 1, "version": 8, "channel": 2})
        print("领取签到奖励:", res["amount"])
    print("[签到]---- end ----")

    # 浏览广告
    print("[浏览广告]--- start ---")
    adList = taskList["gotBrowseTaskAdInit"]["userBrowseTaskAds"]
    for ad in adList:
        if ad["hadFinishedTimes"] == 0:
            adId = ad["advertId"]
            get_result("browseAdTaskForFarm", {"advertId": adId, "type": 0})
            res = get_result("browseAdTaskForFarm", {"advertId": adId, "type": 1})
            print("领取浏览广告奖励:", res["amount"])
    print("[浏览广告]---- end ----")

    # 定时领水滴
    print("[定时领水滴]--- start ---")
    meal = taskList["gotThreeMealInit"]
    if meal["pos"] != -1:
        res = get_result("gotThreeMealForFarm")
        print("领取定时水滴奖励:", res["amount"])
    print("[定时领水滴]---- end ----")

    # 首次浇水奖励
    print("[首次浇水]--- start ---")
    firstWater = taskList["firstWaterInit"]
    if not firstWater["firstWaterFinished"]:
        get_result("waterGoodForFarm")
        res = get_result("firstWaterTaskForFarm")
        print("领取首次浇水奖励:", res["amount"])
    print("[首次浇水]---- end ----")

    # 红包雨
    print("[红包雨]--- start ---")
    waterRain = taskList["waterRainInit"]
    duration = 3 * 60 * 60 * 1000
    if (waterRain["winTimes"] < waterRain["config"]["maxLimit"]) \
            and (waterRain["lastTime"] == 0 or (taskList["sysTime"] - waterRain["lastTime"] > duration)):
        res = get_result("waterRainForFarm")
        print("领取红包雨奖励:", res["addEnergy"])
    print("[红包雨]---- end ----")

    # 循环浇水
    print("[循环浇水]--- start ---")
    totalWater = taskList["totalWaterTaskInit"]
    while True:
        res = get_result("waterGoodForFarm")
        if res["code"] != '0':
            break
        print("浇水成功")
    print("[循环浇水]---- end ----")

    # 累计浇水奖励
    print("[累计浇水]--- start ---")
    totalWater = taskList["totalWaterTaskInit"]
    if not totalWater["f"] \
            and totalWater["totalWaterTaskTimes"] >= totalWater["totalWaterTaskLimit"]:
        res = get_result("totalWaterTaskForFarm")
        print("领取累计浇水奖励:", res["amount"])
    print("[累计浇水]---- end ----")

    print("================== end ==================")
