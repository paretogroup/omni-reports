from omni_reports.facebook_reports.base import FacebookAdsReportType

from omni_reports.facebook_reports.fields import (
    FacebookAttributeReportField, FacebookMetricReportField
)

BOOLEAN_VALUES = {
    'true': True,
    'false': False
}


def to_bool(val):
    return BOOLEAN_VALUES.get(val)


class FacebookAdsAccountPerformanceReportType(FacebookAdsReportType):
    REPORT_TYPE = "FACEBOOK_ACCOUNT_REPORT"

    customer_id = FacebookAttributeReportField(target_name="account_id")
    date = FacebookAttributeReportField(target_name="date_start")
    date_start = FacebookAttributeReportField(target_name="date_start")
    date_end = FacebookAttributeReportField(target_name="date_end")
    currency = FacebookMetricReportField(target_name="account_currency")
    cost = FacebookMetricReportField(target_name="spend")
    ad_set_id = FacebookMetricReportField(target_name="id", target_group_name="adsets")
