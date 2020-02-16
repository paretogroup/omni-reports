class ReportFieldABC:
    pass


class ReportField(ReportFieldABC):
    def __init__(self, name=None, behavior=None, target_name=None, **extra):
        self.name = name
        self.behavior = behavior
        self.target_name = target_name
        self.extra = extra


class AttributeReportField(ReportField):
    def __init__(self, name=None, target_name=None, **extra):
        super(AttributeReportField, self).__init__(
            behavior="attribute",
            name=name,
            target_name=target_name,
            **extra
        )


class SegmentReportField(ReportField):
    def __init__(self, name=None, target_name=None, **extra):
        super(SegmentReportField, self).__init__(
            behavior="segment",
            name=name,
            target_name=target_name,
            **extra
        )


class MetricReportField(ReportField):
    def __init__(self, name=None, target_name=None, **extra):
        super(MetricReportField, self).__init__(
            behavior="metric",
            name=name,
            target_name=target_name,
            **extra
        )
