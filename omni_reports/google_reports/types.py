from omni_reports.client.fields import AttributeReportField, MetricReportField, SegmentReportField
from omni_reports.google_reports.base import GoogleAdsReportType

BOOLEAN_VALUES = {
    'true': True,
    'false': False
}


def to_bool(val):
    return BOOLEAN_VALUES.get(val)


class GoogleAdsAccountPerformanceReportType(GoogleAdsReportType):
    REPORT_TYPE = "ACCOUNT_PERFORMANCE_REPORT"

    account_id = AttributeReportField(target_name="ExternalCustomerId", display_name="Customer ID")
    day = SegmentReportField(target_name="Date", display_name="Day")
    cost = MetricReportField(target_name="Cost", display_name="Cost", map=lambda val: float(val) / 1e6)
    currency = AttributeReportField(target_name="AccountCurrencyCode", display_name="Currency")
    conversions = MetricReportField(target_name="Conversions", display_name="Conversions", type=float)
    cost_per_conversion = MetricReportField(target_name="CostPerConversion", display_name="Cost / conv.",
                                            map=lambda val: float(val) / 1e6)


class GoogleAdsKeywordsPerformanceReportType(GoogleAdsReportType):
    REPORT_TYPE = "KEYWORDS_PERFORMANCE_REPORT"

    id = AttributeReportField(target_name="Id", display_name="Keyword ID")
    criteria = AttributeReportField(target_name="Criteria", display_name="Keyword")
    ad_group_id = AttributeReportField(target_name="AdGroupId", display_name="Ad group ID")
    ad_group_name = AttributeReportField(target_name="AdGroupName", display_name="Ad group")
    ad_group_status = AttributeReportField(target_name="AdGroupStatus", display_name="Ad group state")
    campaign_id = AttributeReportField(target_name="CampaignId", display_name="Campaign ID")
    campaign_name = AttributeReportField(target_name="CampaignName", display_name="Campaign")
    campaign_status = AttributeReportField(target_name="CampaignStatus", display_name="Campaign state")
    is_negative = AttributeReportField(target_name="IsNegative", display_name="Is negative", map=to_bool)
    has_quality_score = AttributeReportField(target_name="HasQualityScore",
                                             display_name="Has Quality Score",
                                             map=to_bool)
    quality_score = AttributeReportField(target_name="QualityScore", display_name="Quality score")

    cost = MetricReportField(target_name="Cost", display_name="Cost")
