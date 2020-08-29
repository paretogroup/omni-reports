import asyncio
import os
from pprint import pprint

from aiohttp import ClientSession

from pareto_reports.client import ReportClient
from pareto_reports.facebook_reports import FacebookAdsReportTypeResolver

FACEBOOK_BASE_API = "https://graph.facebook.com"
FACEBOOK_VERSION_API = "v7.0"

TEMP_ACCESS_TOKEN = "EAAIuoYA4YdIBAFusU2tddI0BtXX5uXltFJc3ZBYX81MkFODo8PDZCAvW09HsAPkbrRMxIojOC5dZBMdstaM2QQwcZA6PdnQruoyZCX9M4sZBAcmce2R8hU3X1bZCouuwnAHZCsC78WxcmZCiOUL9p99Vuemq5ZC9xYiCGqCZBt5dMbdInVjNpVZCAUvXPQDdNL7PhnxZCIkXSg1b1b7DzIXE7dZBcukIoYw6OHZANjje5pzwwqHhMHrbz58xCLvy3VARFihFhIZD"

FACEBOOK_USER_INFO_REPORT_ENDPOINT = 'me'
FIELDS = "id,name,accounts{name}"


REPORT_ENDPOINT = {
    'FACEBOOK_USER_INFO_REPORT': FACEBOOK_USER_INFO_REPORT_ENDPOINT
}


def get_base_url():
    return f"{FACEBOOK_BASE_API}/{FACEBOOK_VERSION_API}"


async def request(
):

    async with ClientSession() as session:
        client = ReportClient(FacebookAdsReportTypeResolver, {
            'FACEBOOK_TOKEN': TEMP_ACCESS_TOKEN,
            'FACEBOOK_NETWORK_ID': "act_2061402793900152",
        })

        result = await client.execute_report_async(session, {
            "report_type": "FACEBOOK_ADS_ACCOUNT_PERFORMANCE_REPORT",
            "report_name": "test",
            "selector": {
                "fields": ["cost", "date_start", "date_end"],
                "date_range": {
                    "start": "2020-02-15",
                    "end": "2020-02-16",
                    "time_increment": 2
                },
                # "predicates": [
                #     {
                #         "field": "customer_id",
                #         "operator": "equals",
                #         "values": ["TRUE"]
                #     }
                # ]
            }
        })

        pprint(result)


async def main():
    await request()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
