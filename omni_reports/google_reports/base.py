import csv
from io import TextIOWrapper

from googleads import oauth2, adwords, common

from omni_reports.client import ReportClient
from omni_reports.client.types import ReportType
from omni_reports.client.utils import async_wrap

GOOGLE_OPERATORS_MAP = {
    'equals': 'EQUALS',
    'not_equals': 'NOT_EQUALS',
    'in': 'IN',
    'not_in': 'NOT_IN',
}


class GoogleAdsReportType(ReportType):
    REPORT_TYPE = None

    async def resolve(self, fields, predicates, report_definition, context, client: ReportClient):
        google_report_type = self.REPORT_TYPE
        if not google_report_type:
            raise AttributeError('The attribute "google_report_type" is required')

        gads_report_definition = self.__convert_to_google_ads_report_definition(
            fields,
            predicates,
            report_definition,
            google_report_type
        )

        gads_client = self.__create_client(context)
        async_func = async_wrap(self.retrieve_report)

        return await async_func(
            fields,
            gads_client,
            gads_report_definition,
        )

    def retrieve_report(self, fields, gads_client, gads_report_definition):
        gads_report_stream = self.__download_report_as_stream(gads_client, gads_report_definition)
        gads_report_stream_wrapper = TextIOWrapper(gads_report_stream, encoding='utf-8')
        gads_report_reader = csv.DictReader(gads_report_stream_wrapper)

        return self.__convert_from_google_ads_records(gads_report_reader, fields)

    @staticmethod
    def __convert_to_google_ads_report_definition(fields, predicates, report_definition, google_report_type):
        gads_predicates = []
        for predicate_name, predicate in predicates.items():
            gads_predicates.append({
                'field': predicate.field.target_name,
                'operator': GOOGLE_OPERATORS_MAP[predicate.operator],
                'values': predicate.values
            })
        return {
            'reportType': google_report_type,
            'reportName': report_definition.report_name,
            'dateRangeType': 'CUSTOM_DATE',
            'downloadFormat': 'CSV',
            'selector': {
                'fields': [field.target_name or field_name for field_name, field in fields.items()],
                'predicates': gads_predicates,
                'dateRange': {
                    'min': str(report_definition.selector.date_range.start),
                    'max': str(report_definition.selector.date_range.end)
                }
            }
        }

    @staticmethod
    def __convert_from_google_ads_records(records, fields):
        converted_records = []
        for record in records:
            converted_record = dict()
            for column, value in record.items():
                field = next(
                    (name for name, field in fields.items() if field.extra.get('display_name') == column), None)
                if not field:
                    raise AttributeError(f'Field with name "{column}" not found')

                field_definition = fields[field]
                if 'map' in field_definition.extra:
                    value_map = field_definition.extra.get('map')
                    value = value_map(value)
                if 'type' in field_definition.extra:
                    value_type = field_definition.extra.get('type')
                    value = value_type(value)

                converted_record[field] = value
            converted_records.append(converted_record)
        return converted_records

    @staticmethod
    def __create_client(context):
        client_id = context.get('GOOGLE_ADS_CLIENT_ID')
        client_secret = context.get('GOOGLE_ADS_CLIENT_SECRET')
        refresh_token = context.get('GOOGLE_ADS_REFRESH_TOKEN')
        developer_token = context.get('GOOGLE_ADS_DEVELOPER_TOKEN')
        user_agent = context.get('GOOGLE_ADS_USER_AGENT')
        customer_id = context.get('GOOGLE_ADS_CUSTOMER_ID')

        oauth2_client = oauth2.GoogleRefreshTokenClient(
            client_id,
            client_secret,
            refresh_token)

        ads_client = adwords.AdWordsClient(
            developer_token,
            oauth2_client,
            user_agent,
            client_customer_id=customer_id)
        ads_client.cache = common.ZeepServiceProxy.NO_CACHE

        return ads_client

    @staticmethod
    def __download_report_as_stream(client, report):
        report_downloader = client.GetReportDownloader(version='v201809')

        return report_downloader.DownloadReportAsStream(
            report, skip_report_header=True, skip_column_header=False,
            skip_report_summary=True, include_zero_impressions=False)
