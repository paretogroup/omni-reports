import asyncio
import os
from pprint import pprint

from dotenv import load_dotenv

from omni_reports.client import ReportClient
from omni_reports.google_reports import GoogleAdsReportTypeResolver

load_dotenv()


async def request():
    client = ReportClient(GoogleAdsReportTypeResolver, {
        'GOOGLE_ADS_CLIENT_ID': os.getenv('GOOGLE_ADS_CLIENT_ID'),
        'GOOGLE_ADS_CLIENT_SECRET': os.getenv('GOOGLE_ADS_CLIENT_SECRET'),
        'GOOGLE_ADS_DEVELOPER_TOKEN': os.getenv('GOOGLE_ADS_DEVELOPER_TOKEN'),
        'GOOGLE_ADS_USER_AGENT': os.getenv('GOOGLE_ADS_USER_AGENT'),
        'GOOGLE_ADS_CUSTOMER_ID': os.getenv('GOOGLE_ADS_CUSTOMER_ID'),
        'GOOGLE_ADS_REFRESH_TOKEN': os.getenv('GOOGLE_ADS_REFRESH_TOKEN'),
    })

    result = await client.execute_report({
        "report_type": "GOOGLE_ADS_KEYWORDS_PERFORMANCE_REPORT",
        "report_name": "this_month_google_ads_keywords_performance",
        "selector": {
            "fields": ["id", "criteria", "cost"],
            "date_range": {
                "start": "2020-02-15",
                "end": "2020-02-16"
            },
            "predicates": [
                {
                    "field": "has_quality_score",
                    "operator": "equals",
                    "values": ["TRUE"]
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
