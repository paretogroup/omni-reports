from marshmallow import Schema, post_load, validate
from marshmallow import fields as ma_fields

from omni_reports.client import models


class ReportDefinitionPredicateSchema(Schema):
    field = ma_fields.Str(required=True)
    operator = ma_fields.Str(required=True)
    values = ma_fields.List(ma_fields.Str(), validate=validate.Length(min=1))

    @post_load
    def create(self, data, **kwargs):
        return models.ReportDefinitionPredicate(**data)


class ReportDefinitionDateRangeSchema(Schema):
    start = ma_fields.Date(format="%Y-%m-%d", required=True)
    end = ma_fields.Date(format="%Y-%m-%d", required=True)
    time_increment = ma_fields.Integer(required=False)

    @post_load
    def create(self, data, **kwargs):
        return models.ReportDefinitionDateRange(**data)


class ReportDefinitionSelectorSchema(Schema):
    fields = ma_fields.List(ma_fields.Str(), required=True, validate=validate.Length(min=1))
    predicates = ma_fields.List(ma_fields.Nested(ReportDefinitionPredicateSchema()), required=False)
    date_range = ma_fields.Nested(ReportDefinitionDateRangeSchema(), required=True)

    @post_load
    def create(self, data, **kwargs):
        return models.ReportDefinitionSelector(**data)


class ReportDefinitionSchema(Schema):
    report_type = ma_fields.Str(required=True)
    report_name = ma_fields.Str(required=True)
    selector = ma_fields.Nested(ReportDefinitionSelectorSchema(), required=True)

    @post_load
    def create(self, data, **kwargs):
        return models.ReportDefinition(**data)


class ReportSchema(Schema):
    report_definition = ma_fields.Nested(ReportDefinitionSchema(), required=True)
    records = ma_fields.List(ma_fields.Dict(), required=True)

    @post_load
    def create(self, data, **kwargs):
        return models.Report(**data)
