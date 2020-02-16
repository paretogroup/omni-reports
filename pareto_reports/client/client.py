from pareto_reports.client.models import Report
from pareto_reports.client.schemas import ReportDefinitionSchema, ReportSchema


class ReportClient:
    __report_definition_schema = ReportDefinitionSchema()
    __report_schema = ReportSchema()

    def __init__(self, resolver, context=None):
        self.resolver = resolver
        self.context = context or dict()

    def execute_report(self, report_definition, context=None):
        context = context or dict()
        context = {**self.context, **context}

        report_def = self.__report_definition_schema.load(report_definition)
        report_records = self.resolver.process(report_def, context, self)
        report = Report(
            report_definition=report_def,
            records=report_records,
        )

        return self.__report_schema.dump(report)
