## Pareto Reports

Pareto Reports is a client to request, normalize and consolidate reports
from several platforms using a simple, declarative and concise request structure.
Behind the scenes, the _Pareto Reports Client_ will convert the report definition into platform-specific
report requests.

The _Pareto Report Definition_ is a json-like data structure based on _Google Ads Report Definition_,
accepting several elements to query and segment a report.

#### Installation

To install _Pareto Reports_, use `pip`:

```shell script
pip install -U pareto-reports
```

#### Usage

Create a `ReportTypeResolver` to resolve report types of each platform (like Google Ads).
Then, create a `ReportClient` and execute your report definition. 

```python
from pareto_reports.client import ReportClient, ReportTypeResolverBuilder

resolver = ReportTypeResolverBuilder() \
    .extend(PlatformAReportResolver) \
    .extend(PlatformBReportResolver) \
    .build()

client = ReportClient(resolver)
result = client.execute_report({
    'report_type': 'PLATFORM_A_ACCOUNT_PERFORMANCE_REPORT',
    'report_name': 'my_report',
    'selector': {
        'fields': ['account_id', 'cost', 'conversions', 'cost_per_conversion'],
        'predicates': [
            {
                'field': 'cost',
                'operator': 'greater_than',
                'values': ['0']
            }
        ]
    }
})

print(result)
```

Additionally, you can pass a context to `ReportClient` so that a `ReportTypeResolver` can be configured.

```python
from pareto_reports.client import ReportClient

client = ReportClient(resolver, {
    'PLATFORM_A_CLIENT_ID': 'MY_CLIENT_ID',
    'PLATFORM_A_CLIENT_SECRET': 'MY_CLIENT_SECRET',
})

# or via `execute_report`
report_definition = {...}
client.execute_report(report_definition, {
    'PLATFORM_A_CUSTOMER_ID': 'MY_CUSTOMER_ID',
})
```

#### Creating a ReportType

Create a `ReportType` in _Pareto Reports_ is simple. Just create a new class extending `ReportType`, declare 
the fields of your report type and implement the resolve method. The `ReportClient` will validate all definitions of 
your report type and call the resolver.

To create your report type, you must declare all fields of report with its behaviors and metadata. There is three types
of behaviors: attribute, metric and segment.

- Attribute: The attribute fields must always reflect the current state of your data, ignoring the timespan of the report;
- Metric: The metric fields reflect the data over the timespan of the report;
- Segment: The segment field contains dimension data that is used to group metrics. Including a metric field into your
report definition may split a single row into multiple rows. The value of metric fields reflect the data over the timespan
of the report. 

After the identification of the behavior for each report type field, you can start declaring the report type class:
 
```python
from pareto_reports.client import ReportClient, ReportTypeResolverBuilder
from pareto_reports.client.types import ReportType
from pareto_reports.client.fields import AttributeReportField, MetricReportField, SegmentReportField


class MyAdReportType(ReportType):
    """
    Example of ReportType to query perfomance of all accounts in platform
    """

    account_id = SegmentReportField()
    campaign_id = SegmentReportField()
    ad_group_id = SegmentReportField()
    ad_id = SegmentReportField()
    
    cost = MetricReportField()
    conversions = MetricReportField()
    cost_per_conversion = MetricReportField()

    campaign_status = AttributeReportField()
    ad_group_status = AttributeReportField()
    ad_status = AttributeReportField()

    def resolve(self, fields, predicates, report_definition, context, client):
        # logic to apply predicates and filter fields
        return []

resolver = ReportTypeResolverBuilder() \
    .add_type("MY_AD_REPORT", MyAdReportType()) \
    .build()

client = ReportClient(resolver)
client.execute_report({
    'report_type': 'MY_AD_REPORT',
    'report_name': 'report_name_here',
    'selector': {
        'fields': ['ad_group_id', 'cost', 'conversions', 'cost_per_conversion'],
        'predicates': [
            {
                'field': 'campaign_id',
                'operator': 'equals',
                'values': ['1234']
            }
        ]
    }
})
```

#### Contributing

To contribute, see the [CONTRIBUTING](CONTRIBUTING.md) guides.

#### License

[MIT](https://choosealicense.com/licenses/mit/)
