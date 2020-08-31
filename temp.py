import asyncio
import os
from pprint import pprint

from aiohttp import ClientSession

from pareto_reports.client import ReportClient
from pareto_reports.facebook_reports import FacebookAdsReportTypeResolver

FACEBOOK_BASE_API = "https://graph.facebook.com"
FACEBOOK_VERSION_API = "v7.0"

TEMP_ACCESS_TOKEN = "EAAIuoYA4YdIBAAByxwPQrG97tosgc0ZBP3AadLZCcGZCXp2rBflbuo6cNoWXzwviMZA3O9sPwnzKXJ9k1d1tsxVy5ziMuYBZA3PDQb3X36wZBlHHoJm458hyRAQ0klcmMFYVWR0JVKT2Bskv8f40GK2K4uPbjxEgGVGOWrp9LwpUmOxk7jZAJZANxbqBBDh5pKbkSrkEufd1IH39KWpNwZCfi"

FACEBOOK_USER_INFO_REPORT_ENDPOINT = 'me'
FIELDS = "id,name,accounts{name}"


REPORT_ENDPOINT = {
    'FACEBOOK_USER_INFO_REPORT': FACEBOOK_USER_INFO_REPORT_ENDPOINT
}


def get_base_url():
    return f"{FACEBOOK_BASE_API}/{FACEBOOK_VERSION_API}"


async def request():
    async with ClientSession() as session:
        client = ReportClient(FacebookAdsReportTypeResolver, {
            'FACEBOOK_TOKEN': TEMP_ACCESS_TOKEN,
            'FACEBOOK_NETWORK_ID': "act_2061402793900152",
        })

        result = await client.execute_report_async(session, {
            "report_type": "FACEBOOK_ADS_ACCOUNT_PERFORMANCE_REPORT",
            "report_name": "test",
            "selector": {
                "fields": ["cost", "date", "currency"],
                "date_range": {
                    "start": "2020-02-15",
                    "end": "2020-02-16",
                },
                # "predicates": [
                #     {
                #         "field": "customer_id",
                #         "operator": "equals",
                #         "values": ["2061402793900152"]
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
