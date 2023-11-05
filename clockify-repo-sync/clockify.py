from datetime import datetime
import requests
import json
from collections import namedtuple
import csv

# Personal info
ORIGIN_KEY = ""
DEST_KEY = ""
SPACE_NAME = "Innosoft"  # same name for workspace and project
BASE_URL = "https://api.clockify.me/api/v1/workspaces/"
CSV_PATH = "./entries.csv"

ORIGIN_HEAD = {"x-api-key": ORIGIN_KEY, "content-type": "application/json"}
DEST_HEAD = {"x-api-key": DEST_KEY, "content-type": "application/json"}


def retrieve(url, headers):
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return json.loads(response.content.decode("utf-8"))
    else:
        raise ValueError(
            "Error {}: {}".format(str(response.status_code), response.content)
        )


def post(url, headers, data):
    data = json.dumps(data)
    response = requests.post(url=url, headers=headers, data=data)
    if response.status_code == 200 or response.status_code == 201:
        return json.loads(response.content.decode("utf-8"))
    else:
        raise ValueError(
            "Error {}: {}".format(str(response.status_code), response.content)
        )


# Retrieve info from origin workspace
origin_workspaces = retrieve(BASE_URL, ORIGIN_HEAD)
origin = list(filter(lambda w: w["name"] == SPACE_NAME, origin_workspaces))[0]
origin_ws_id = origin["id"]
# ----------------------------
origin_tags = retrieve(BASE_URL + origin_ws_id + "/tags", headers=ORIGIN_HEAD)
origin_tags_name = [tag["name"] for tag in origin_tags]
# ----------------------------
origin_projects = retrieve(BASE_URL + origin_ws_id + "/projects", headers=ORIGIN_HEAD)
origin_projects_name = [project["name"] for project in origin_projects]

# Sync with dest workspace
dest_workspaces = retrieve(BASE_URL, DEST_HEAD)
dest = list(filter(lambda w: w["name"] == SPACE_NAME, dest_workspaces))
dest = dest[0] if len(dest) > 0 else post(BASE_URL, DEST_HEAD, {"name": SPACE_NAME})
dest_ws_id = dest["id"]
# ----------------------------
dest_tags = retrieve(BASE_URL + dest_ws_id + "/tags", headers=DEST_HEAD)
dest_tags_dict = {tag["name"]: tag["id"] for tag in dest_tags}
for tag in origin_tags_name:
    if tag not in dest_tags_dict.keys():
        tag_json = post(BASE_URL + dest_ws_id + "/tags", DEST_HEAD, {"name": tag})
        dest_tags_dict[tag] = tag_json["id"]
# ----------------------------
dest_projects = retrieve(BASE_URL + dest_ws_id + "/projects", headers=DEST_HEAD)
dest_projects_dict = {project["name"]: project["id"] for project in dest_projects}
for project in origin_projects_name:
    if project not in dest_projects_dict.keys():
        project_json = post(
            BASE_URL + dest_ws_id + "/projects", DEST_HEAD, {"name": project}
        )
        dest_projects_dict[project] = project_json["id"]


# Obtain and store time entries from origin by csv
Record = namedtuple(
    "Record",
    [
        "billiable",
        "customAttributes",
        "customFields",
        "description",
        "end",
        "projectId",
        "start",
        "tagIds",
        "taskId",
    ],
)

entries = []
start_time_registered = []
with open(CSV_PATH, "r", encoding="utf-8") as f:
    csv_data = csv.reader(f)
    next(csv_data)
    for row in csv_data:
        if row[9] + " " + row[10] in start_time_registered:
            continue
        else:
            billiable = True if row[8] == "Yes" else False  # billiable
            customAttributes = []
            customFields = []
            description = row[2]

            date_format = "%d/%m/%Y  %H:%M:%S"
            end_time = row[11] + " " + row[12]
            end_time = datetime.strptime(end_time, date_format)
            end_time = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            projectId = dest_projects_dict[row[0].strip()]

            start_time = row[9] + " " + row[10]
            start_time_registered.append(start_time)
            start_time = datetime.strptime(start_time, date_format)
            start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")

            tagIds = [dest_tags_dict[tag.strip()] for tag in row[7].split(",")]
            taskId = ""

            record = Record(
                billiable,
                customAttributes,
                customFields,
                description,
                end_time,
                projectId,
                start_time,
                tagIds,
                taskId,
            )
            entries.append(record)
for entry in entries:
    app_data = {
        "billable": entry.billiable,
        "customAttributes": entry.customAttributes,
        "customFields": entry.customFields,
        "description": entry.description,
        "end": entry.end,
        "projectId": entry.projectId,
        "start": entry.start,
        "tagIds": entry.tagIds,
        "taskId": entry.taskId,
    }
    post(BASE_URL + dest_ws_id + "/time-entries", DEST_HEAD, app_data)
