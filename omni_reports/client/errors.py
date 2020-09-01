
class ReportTypeNotFoundError(RuntimeError):
    def __init__(self, type_name):
        super(ReportTypeNotFoundError, self).__init__(
            f"No report type found with name \"{type_name}\"."
        )


class ReportTypeFieldNotFoundError(RuntimeError):
    def __init__(self, field_name):
        super(ReportTypeFieldNotFoundError, self).__init__(
            f"No report type field found with name \"{field_name}\"."
        )


class InvalidReportRecordError(RuntimeError):
    def __init__(self, record, message):
        super(InvalidReportRecordError, self).__init__(message)
        self.record = record


class InvalidReportDefinitionError(RuntimeError):
    def __init__(self, report_definition, message):
        super().__init__(message)


class ReportResponseError(RuntimeError):
    def __init__(self, message):
        super().__init__(message)
