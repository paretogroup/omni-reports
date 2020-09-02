from typing import Optional, Dict

from aiohttp import ClientSession

from omni_reports.client.models import Report
from omni_reports.client.resolvers import ReportTypeResolverABC
from omni_reports.client.schemas import ReportDefinitionSchema, ReportSchema


class ReportClient:
    __report_definition_schema = ReportDefinitionSchema()
    __report_schema = ReportSchema()

    session: Optional[ClientSession]

    def __init__(
            self, resolver: ReportTypeResolverABC,
            context: Optional[Dict] = None,
            session: Optional[ClientSession] = None
    ):
        self.resolver = resolver
        self.context = context or dict()

        self.session = session

    async def execute_report(self, report_definition, context=None):
        context = context or dict()
        context = {**self.context, **context}

        report_def = self.__report_definition_schema.load(report_definition)
        report_records = await self.resolver.process(report_def, context, self)
        report = Report(
            report_definition=report_def,
            records=report_records,
        )

        return self.__report_schema.dump(report)
