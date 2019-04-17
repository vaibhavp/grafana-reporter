import requests
import json
import datetime

BASE_URL = "http://localhost:3000"

GET_DASHBOARD_URL = BASE_URL + "/api/search?folderIds=0&query=&starred=false"
GET_SNAPSHOT_URL = BASE_URL+"/api/dashboard/snapshots"
POST_SNAPSHOT_URL = BASE_URL + "/api/snapshots"

dashboard_dict = {}


headers = {
    'content-type': "application/json",
    'authorization': "Basic YWRtaW46cHJvbS1vcGVyYXRvcg==",
}

res = requests.get(url=GET_DASHBOARD_URL, headers=headers, )
data = res.json()
i = 0
for item in data:
    dashboard_dict[i] = {"udi": item["uid"], "id": item["id"], "name": item["title"]}
    i = i+1

start_date = datetime.datetime.now() - datetime.timedelta(minutes=15)
end_date = datetime.datetime.now()

for ID,subdict in dashboard_dict.items():
    GET_DASHBOARD_VERSION_URL = BASE_URL + "/api/dashboards/id/" + str(subdict["id"]) + "/versions/1"
    version_request = requests.get(url=GET_DASHBOARD_VERSION_URL, headers=headers)
    version_response = version_request.json()
    with open("snapshot.json",'r+') as dashboard_json:
        data = json.load(dashboard_json)
        if "rows" in version_response["data"]:
            data["dashboard"]["rows"] = version_response["data"]["rows"]
        elif "panels" in version_response["data"]:
            data["dashboard"]["panels"] = version_response["data"]["panels"]
        else:
            continue
        data["dashboard"]["templating"] = version_response["data"]["templating"]
        data["dashboard"]["title"] = subdict["name"]
        data["name"] = subdict["name"]
        data["dashboard"]["time"]["from"] = start_date.strftime("%Y-%m-%d %H:%M:%S")
        data["dashboard"]["time"]["to"] = end_date.strftime("%Y-%m-%d %H:%M:%S")

    create_snapshot = requests.post(url=POST_SNAPSHOT_URL, headers=headers, data=json.dumps(data))
    snapshot_response = create_snapshot.json()
    print(subdict["name"] + ":-" + snapshot_response['url'])

