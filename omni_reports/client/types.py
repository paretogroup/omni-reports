import inspect

from omni_reports.client.errors import ReportTypeFieldNotFoundError, InvalidReportRecordError
from omni_reports.client.fields import ReportFieldABC
from omni_reports.client.models import ReportPredicate
from omni_reports.client.utils import is_instance_or_subclass


def _get_fields(attrs, field_class, pop=False):
    fields = [
        (field_name, field_value)
        for field_name, field_value in attrs.items()
        if is_instance_or_subclass(field_value, field_class)
    ]
    if pop:
        for field_name, _ in fields:
            del attrs[field_name]
    return fields


def _get_fields_by_mro(klass, field_class):
    mro = inspect.getmro(klass)
    return sum(
        (
            _get_fields(
                getattr(base, "_declared_fields", base.__dict__),
                field_class,
            )
            for base in mro[:0:-1]
        ),
        [],
    )


class ReportTypeMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls_fields = _get_fields(attrs, ReportFieldABC, True)
        klass = super().__new__(mcs, name, bases, attrs)
        inherited_fields = _get_fields_by_mro(klass, ReportFieldABC)

        meta = klass.Meta
        klass.opts = klass.OPTIONS_CLASS(meta)

        klass._declared_fields = mcs.get_declared_fields(
            klass=klass,
            cls_fields=cls_fields,
            inherited_fields=inherited_fields,
        )

        return klass

    @classmethod
    def get_declared_fields(
            mcs,
            klass,
            cls_fields,
            inherited_fields,
    ):
        return dict(inherited_fields + cls_fields)


class ReportTypeOptions:
    def __init__(self, meta):
        self.meta = meta


class ReportTypeABC:
    def execute(self, report_definition, context, client):
        raise NotImplementedError

    def resolve(self, fields, predicates, report_definition, context, client):
        raise NotImplementedError


class ReportType(ReportTypeABC, metaclass=ReportTypeMeta):
    OPTIONS_CLASS = ReportTypeOptions

    _declared_fields = {}

    opts = None  # type: ReportTypeOptions

    class Meta:
        pass

    async def execute(self, report_definition, context, client):
        fields = self._extract_fields(report_definition)
        predicates = self._extract_predicates(report_definition)

        records = await self.resolve(
            fields,
            predicates,
            report_definition,
            context,
            client,
        )

        return self._filter_fields_in_records(records, fields)

    async def resolve(self, fields, predicates, report_definition, context, client):
        raise NotImplementedError

    def _extract_predicates(self, report_definition):
        predicates = {}

        for rd_predicate in report_definition.selector.predicates:
            field = self._declared_fields.get(rd_predicate.field)
            if not field:
                raise ReportTypeFieldNotFoundError(rd_predicate.field)
            predicates[rd_predicate.field] = ReportPredicate(
                field=field,
                operator=rd_predicate.operator,
                values=rd_predicate.values
            )

        return predicates

    def _extract_fields(self, report_definition):
        fields = {}
        for rd_field in report_definition.selector.fields:
            field = self._declared_fields.get(rd_field)
            if not field:
                raise ReportTypeFieldNotFoundError(rd_field)
            fields[rd_field] = field
        return fields

    @staticmethod
    def _filter_fields_in_records(records, fields):
        new_records = []
        for record in records:
            new_record = {}
            for field_name, field in fields.items():
                if field_name not in record:
                    raise InvalidReportRecordError(record, f"Field with name \"{field_name}\" not found on record")
                new_record[field_name] = record[field_name]
            new_records.append(new_record)
        return new_records
