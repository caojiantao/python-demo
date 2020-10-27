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
