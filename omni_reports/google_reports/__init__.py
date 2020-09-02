from omni_reports.client import ReportTypeResolverBuilder

from omni_reports.google_reports.types import (
    GoogleAdsAccountPerformanceReportType,
    GoogleAdsKeywordsPerformanceReportType
)

GoogleAdsReportTypeResolver = ReportTypeResolverBuilder() \
    .add_type('GOOGLE_ADS_ACCOUNT_PERFORMANCE_REPORT', GoogleAdsAccountPerformanceReportType()) \
    .add_type('GOOGLE_ADS_KEYWORDS_PERFORMANCE_REPORT', GoogleAdsKeywordsPerformanceReportType()) \
    .build()
