import asyncio
from pprint import pprint

from aiohttp import ClientSession

from pareto_reports.client import ReportClient
from pareto_reports.facebook_reports import FacebookAdsReportTypeResolver


TEMP_ACCESS_TOKEN = "EAAIuoYA4YdIBAF7GxCpIxqA7MuyTAizZCbloFLMBcGnxngcjwV9RXSSWExST3X0D6ZC9aBviAn1AJZCp7lbJZAktaaxyMxg6j25tZBStKZC9E7kqRprkjpEeZA7F4vDbZBjmH2IZBIsRj3Ee9NjtSwM7ocsHgD4jcCM7h3Fep5Ca1qxnjCJ01tskLou3coEhc78ugaDSiE1I5XoZBqF6Ox1t5i"


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
