from omni_reports.client.errors import ReportTypeNotFoundError


class ReportTypeResolverABC:
    async def process(self, report_definition, context, client):
        raise NotImplementedError()


class ReportTypeResolver(ReportTypeResolverABC):
    def __init__(self, types=None):
        self.types = types or {}

    async def process(self, report_definition, context, client):
        type_config = self.types.get(report_definition.report_type)
        if not type_config:
            raise ReportTypeNotFoundError(report_definition)
        return await type_config.execute(report_definition, context, client)


class ReportTypeResolverBuilder:
    __types = {}

    def extend(self, resolver: ReportTypeResolver):
        self.__types.update(resolver.types)
        return self

    def add_type(self, report_type, report_type_config):
        self.__types[report_type] = report_type_config
        return self

    def build(self) -> ReportTypeResolverABC:
        return ReportTypeResolver(
            types=self.__types,
        )
