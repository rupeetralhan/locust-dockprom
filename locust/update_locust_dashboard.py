import json
import os
from argparse import ArgumentParser

import sys


def update_locust_dashboard(exported_dashboard_path=None, locust_dashboard_curl_json=None):
    my_location = os.path.abspath(os.path.dirname(__file__))
    if locust_dashboard_curl_json is None:
        locust_dashboard_curl_json = os.path.abspath(os.path.join(my_location, '../grafana/dashboards/locust.json'))
    if exported_dashboard_path is None:
        exported_dashboard_path = os.path.abspath(
            os.path.join(my_location,'../../locust_exporter/locust_dashboard.json'))
    if exported_dashboard_path and os.path.exists(exported_dashboard_path):
        with open(exported_dashboard_path, 'r') as exported_dashboard_f:
            exported_dashboard_json = json.load(exported_dashboard_f)
    else:
        print('Did not find exported dashboard json {}'.format(exported_dashboard_path))
        return 1
    if locust_dashboard_curl_json and exported_dashboard_json:
        out_json={'dashboard': exported_dashboard_json,
                  "inputs": [
                  ],
                  "folderId": 0,
                  "overwrite": True
                  }
        out_json['dashboard']['id']=None
        with open(locust_dashboard_curl_json, 'w') as locust_dashboard_curl_f:
            json.dump(out_json, locust_dashboard_curl_f, indent=2)
    else:
        print("Can not save output json file {} with {}".format(locust_dashboard_curl_json, exported_dashboard_json))
        return 2



if __name__ == "__main__":
    parser = ArgumentParser(
        description="Update locust dashboard input file - at fields required for curl")
    parser.add_argument("--exported-dashboard-path", help="""json file exported from grafana dashboard.
    If argument is not provided tool assume that locust exporter is in the same dir as locust_dockprom""")
    parser.add_argument("--locust-dashboard-curl-json", help="json file prepared for curl tool")
    args = parser.parse_args()
    print(args)
    sys.exit(update_locust_dashboard(args.exported_dashboard_path, args.locust_dashboard_curl_json))