from datetime import date
from typing import Dict, List

from omni_reports.client.fields import ReportField


class ReportPredicate:
    def __init__(self, field: ReportField = None, operator: str = None, values: List[str] = None):
        self.field = field
        self.operator = operator
        self.values = values

    def __str__(self):
        return f"<ReportPredicate field={self.field} operator={self.operator} values={self.values}>"

    def __repr__(self):
        return self.__str__()


class ReportDefinitionPredicate:
    def __init__(self, field: str = None, operator: str = None, values: List[str] = None):
        self.field = field
        self.operator = operator
        self.values = values

    def __str__(self):
        return f"<ReportDefinitionPredicate field={self.field} operator={self.operator} values={self.values}>"

    def __repr__(self):
        return self.__str__()


class ReportDefinitionDateRange:
    def __init__(self, start: date = None, end: date = None, time_increment: int = 1):
        self.start = start
        self.end = end
        self.time_increment = time_increment or 1

    def __str__(self):
        return f"<ReportDefinitionDateRange start={self.start} end={self.end}>"

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return bool(self.start and self.end and self.time_increment)


class ReportDefinitionSelector:
    def __init__(self,
                 fields: List[str] = None,
                 predicates: List[ReportDefinitionPredicate] = None,
                 date_range: ReportDefinitionDateRange = None):
        self.fields = fields
        self.predicates = predicates or list()
        self.date_range = date_range

    def __str__(self):
        return f"<ReportDefinitionSelector fields={self.fields}>"

    def __repr__(self):
        return self.__str__()


class ReportDefinition:
    def __init__(self, report_type: str = None, report_name: str = None, selector: ReportDefinitionSelector = None):
        self.report_type = report_type
        self.report_name = report_name
        self.selector = selector

    def __str__(self):
        return f"<ReportDefinition report_type={self.report_type} report_name={self.report_name}>"

    def __repr__(self):
        return self.__str__()


class Report:
    def __init__(self, report_definition: ReportDefinition = None, records: List[Dict] = None):
        self.report_definition = report_definition
        self.records = records

    def __str__(self):
        return f"<Report " \
               f"report_type={self.report_definition.report_type} " \
               f"report_name={self.report_definition.report_name}>"

    def __repr__(self):
        return self.__str__()
