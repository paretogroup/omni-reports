from pareto_reports.client.models import Report
from pareto_reports.client.resolvers import ReportTypeResolverABC
from pareto_reports.client.schemas import ReportDefinitionSchema, ReportSchema


class ReportClient:
    __report_definition_schema = ReportDefinitionSchema()
    __report_schema = ReportSchema()

    def __init__(self, resolver: ReportTypeResolverABC, context=None):
        self.resolver = resolver
        self.context = context or dict()

    async def execute_report_async(self, session, report_definition, context=None):
        context = context or dict()
        context = {**self.context, **context}

        report_def = self.__report_definition_schema.load(report_definition)
        report_records = await self.resolver.process_async(session, report_def, context, self)
        report = Report(
            report_definition=report_def,
            records=report_records,
        )

        return self.__report_schema.dump(report)

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
