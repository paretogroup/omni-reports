import json
from typing import Dict, List

from aiohttp import ClientSession

from omni_reports.client import ReportClient
from omni_reports.client.errors import ReportResponseError
from omni_reports.client.models import ReportPredicate, ReportDefinitionDateRange
from omni_reports.client.types import ReportType
from omni_reports.facebook_reports.fields import FacebookReportField, FACEBOOK_OPERATORS_MAP
from omni_reports.facebook_reports.settings import (
    FACEBOOK_BASE_API, FACEBOOK_VERSION_API,
    REPORT_ENDPOINT_PATTERN
)


def get_base_url():
    return f"{FACEBOOK_BASE_API}/{FACEBOOK_VERSION_API}"


class FacebookAdsReportType(ReportType):
    REPORT_TYPE = None
    FIELD_BEGIN_SEPARATOR = "{"
    FIELD_END_SEPARATOR = "}"

    async def resolve(self, fields, predicates, report_definition, context, client: ReportClient):
        if not self.REPORT_TYPE:
            raise AttributeError('The attribute "facebook_report_type" is required')

        if client.session is None:
            raise AttributeError('Client session cannot be null.')

        session = client.session
        date_range: ReportDefinitionDateRange = report_definition.selector.date_range

        self._validate_predicates(predicates, fields, date_range)

        formatted_fields = self._get_fields(fields)
        predicates = self._get_predicates(predicates)

        url = self._build_request_url(context, formatted_fields, predicates, date_range)
        records = await request(session, url)

        return self._resolve_fields_on_records(records, fields)

    def _build_request_url(self, context, fields, predicates, date_range):

        token = context.get("FACEBOOK_TOKEN")
        network_id = context.get("FACEBOOK_NETWORK_ID")

        endpoint_pattern = REPORT_ENDPOINT_PATTERN[self.REPORT_TYPE] or ""
        endpoint = self._compose_endpoint_with_predicates(endpoint_pattern, {
            "network_id": network_id
        })
        date_range = self._compose_date_range(date_range)
        predicates = self._compose_predicates(predicates)

        return f"{get_base_url()}/{endpoint}?fields={fields}" \
               f"&access_token={token}&{date_range}" \
               f"&filtering={predicates}"

    @staticmethod
    def _validate_predicates(
            predicates: Dict[str, ReportPredicate],
            fields: dict,
            date_range: ReportDefinitionDateRange
    ):
        for predicate in predicates.values():
            if predicate.field.target_group_name:
                raise AttributeError(f"Fields with target group is not accepted yet. "
                                     f"Invalid field: {predicate.field.target_group_name}"

                                     f" - {predicate.field.target_name}")

        if date_range:
            has_date_field = bool([
                field_name
                for field_name, _ in fields.items()
                if field_name == 'date'
            ])
            if date_range.time_increment != 1 and has_date_field:
                raise AttributeError(
                    "You can only date field with time_increment equals to 1. For"
                    "other time_increment values use date_start and date_end fields."
                )

    @staticmethod
    def _get_predicates(predicates: Dict[str, ReportPredicate]) -> List[dict]:
        formatted_predicates = []
        for predicate in predicates.values():
            operator = FACEBOOK_OPERATORS_MAP[predicate.operator]

            formatted_predicates.append({
                "field": predicate.field.target_name,
                "operator": operator,
                "value": predicate.values[0] if operator == "EQUAL" else predicate.values
            })

        return formatted_predicates

    @staticmethod
    def _resolve_fields_on_records(records, fields) -> List[dict]:
        if not isinstance(records, dict):
            raise ValueError(f'Invalid records response for {records}')
        if 'error' in records:
            raise ReportResponseError(
                f"\n\nFacebook Api response error:\n{records.get('error')}"
            )

        only_records = records.get("data") or []
        only_records = only_records if isinstance(only_records, list) else list(only_records)

        updated_records = []

        for record in only_records:
            new_record = {}
            for field_name, field in fields.items():
                try:
                    new_record[field_name] = record[field.target_name]
                except KeyError as error:
                    raise KeyError(f"{error}\nField '{field_name}' not mapped on record {record}.")

                updated_records.append(new_record)

        return updated_records

    @staticmethod
    def _compose_predicates(predicates: dict) -> str:
        return json.dumps(predicates) if predicates else ""

    @staticmethod
    def _compose_date_range(date_range: ReportDefinitionDateRange) -> str:
        if not date_range:
            return ""

        start_range = "{start_object}'since':'{since}'".format(
            start_object="{",
            since=date_range.start,
        )
        end_range = "'until': '{until}'{end_object}".format(
            until=date_range.end,
            end_object="}"
        )

        time_range = f"time_range={start_range},{end_range}"
        time_increment = f"time_increment={date_range.time_increment}"

        return f"{time_range}&{time_increment}"

    def _get_fields(self, fields: Dict[str, FacebookReportField]):
        group_fields = {
            field.target_group_name
            for _, field in fields.items()
            if field.target_group_name
        }

        grouped_fields = {}
        for group_field in group_fields:
            filtered_fields = (
                field.target_name
                for _, field in fields.items()
                if group_field == field.target_group_name
            )
            grouped_fields[group_field] = \
                group_field \
                + self.FIELD_BEGIN_SEPARATOR \
                + ",".join(filtered_fields) \
                + self.FIELD_END_SEPARATOR

        non_object_fields = [
            field.target_name
            for _, field in fields.items()
            if not field.target_group_name
        ]
        all_fields = ",".join([*non_object_fields, *grouped_fields.values()])

        return all_fields

    @staticmethod
    def _compose_endpoint_with_predicates(pattern: str, predicates: dict):
        return pattern.format(**predicates)

    @staticmethod
    def _get_predicates_not_used_on_endpoint_pattern(pattern: str, predicates: dict):
        return {
            predicate_field: predicates[predicate_field]
            for predicate_field in predicates.keys()
            if predicate_field not in pattern
        }


async def request(session: ClientSession, url: str):
    async with session.get(url) as response:
        return await response.json()
