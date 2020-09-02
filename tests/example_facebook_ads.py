import asyncio
import os
from pprint import pprint

from aiohttp import ClientSession
from dotenv import load_dotenv

from omni_reports.client import ReportClient
from omni_reports.facebook_reports import FacebookAdsReportTypeResolver

load_dotenv()


async def request():
    async with ClientSession() as session:
        client = ReportClient(FacebookAdsReportTypeResolver, {
            'FACEBOOK_TOKEN': os.getenv('FACEBOOK_TOKEN'),
            'FACEBOOK_NETWORK_ID': os.getenv('FACEBOOK_NETWORK_ID'),
        }, session=session)

        result = await client.execute_report({
            "report_type": "FACEBOOK_ADS_ACCOUNT_PERFORMANCE_REPORT",
            "report_name": "test",
            "selector": {
                "fields": ["cost", "date", "currency"],
                "date_range": {
                    "start": "2000-02-15",
                    "end": "2000-02-16",
                },
                "predicates": [
                    {
                        "field": "cost",
                        "operator": "equals",
                        "values": ["1396.77"]
                    }
                ]
            }
        })

        pprint(result)


async def main():
    await request()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
