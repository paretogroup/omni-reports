from omni_reports.client.fields import (
    ReportField, AttributeReportField,
    SegmentReportField, MetricReportField
)

FACEBOOK_OPERATORS_MAP = {
    'equals': 'EQUAL',
    'not_equals': 'NOT_EQUALS',
    'in': 'IN',
    'not_in': 'NOT_IN',
}


class FacebookReportField(ReportField):
    def __init__(self, *args, target_name, target_group_name=None, **extra):
        self.target_group_name = target_group_name

        super().__init__(*args, target_name=target_name, **extra)


class FacebookAttributeReportField(FacebookReportField, AttributeReportField):
    pass


class FacebookSegmentReportField(FacebookReportField, SegmentReportField):
    pass


class FacebookMetricReportField(FacebookReportField, MetricReportField):
    pass
