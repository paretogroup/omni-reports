from pareto_reports.client import ReportTypeResolverBuilder
from pareto_reports.facebook_reports.types import FacebookAdsAccountPerformanceReportType

FacebookAdsReportTypeResolver = ReportTypeResolverBuilder() \
    .add_type('FACEBOOK_ADS_ACCOUNT_PERFORMANCE_REPORT', FacebookAdsAccountPerformanceReportType()) \
    .build()
