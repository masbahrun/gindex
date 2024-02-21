from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json
import argparse
import pandas as pd

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"


def indexURL(urls, http):
    for u in urls:
        content = {}
        content['url'] = u.strip()
        content['type'] = "URL_UPDATED"
        json_ctn = json.dumps(content)    
        response, content = http.request(ENDPOINT, method="POST", body=json_ctn)
        result = json.loads(content.decode())

        # For debug purpose only
        if("error" in result):
            print("Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"], result["error"]["message"]))
        else:
            print("urlNotificationMetadata.url: {}".format(result["urlNotificationMetadata"]["url"]))
            print("urlNotificationMetadata.latestUpdate.url: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["url"]))
            print("urlNotificationMetadata.latestUpdate.type: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["type"]))
            print("urlNotificationMetadata.latestUpdate.notifyTime: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonkeyFile")
    args = parser.parse_args()
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(args.jsonkeyFile, scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())
    
    with open('urls.txt') as my_file:
        sitemap = my_file.readlines()
    indexURL(sitemap, http)
    
if __name__ == "__main__":
    main()