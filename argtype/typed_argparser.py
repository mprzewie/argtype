from argparse import ArgumentParser, Namespace
from typing import TypeVar, Generic, NamedTuple, Optional, Sequence, Dict, Any

from argtype.doc.google import OMIT_LINES

_DESCRIPTION_KEY = "description"
NamedTupleType = TypeVar("NamedTupleType", bound=NamedTuple, covariant=True)


class TypedArgumentParser(ArgumentParser, Generic[NamedTupleType]):
    def __init__(self, named_tuple_type: NamedTupleType, **kwargs):
        self.named_tuple_type = named_tuple_type
        kwargs[_DESCRIPTION_KEY] = kwargs.get(_DESCRIPTION_KEY, self._description)
        super().__init__(**kwargs)
        for field_name in self._fields:
            self.add_argument(
                f"--{field_name}",
                type=self._type(field_name),
                default=self._default(field_name),
                help=self._help(field_name),
                required=self._required(field_name),
            )

    def parse_args(
        self, args: Optional[Sequence] = None, namespace: Optional[Namespace] = None
    ) -> NamedTupleType:
        return self.named_tuple_type(**super().parse_args(args, namespace).__dict__)

    @property
    def _fields(self) -> Sequence[str]:
        return self.named_tuple_type._fields

    def _type(self, field_name: str) -> type:
        return self.named_tuple_type._field_types.get(field_name, None)

    def _default(self, field_name: str) -> Any:
        return self.named_tuple_type._field_defaults.get(field_name, None)

    def _help(self, field_name: str) -> str:
        return self._docstrings_for_fields.get(field_name, None)

    def _required(self, field_name: str) -> bool:
        return field_name not in self.named_tuple_type._field_defaults.keys()

    @property
    def _description(self):
        return self._doc_dict.get(None, "")

    @property
    def _docstrings_for_fields(self) -> Dict[str, str]:
        doc_dict = self._doc_dict
        return {
            field: doc_dict[field] for field in doc_dict.keys() if field in self._fields
        }

    @property
    def _doc_dict(self, omit_lines: Sequence[str] = OMIT_LINES) -> Dict[str, str]:
        docstring = self.named_tuple_type.__doc__
        lines = [
            l.lstrip()
            for l in docstring.split("\n")
            if l.lstrip().rstrip() not in omit_lines
        ]
        doc_dict = {}
        current_field = None
        for doc_line in lines:
            l_split = doc_line.split(":")
            if l_split[0].replace(" ", "") in self._fields:
                current_field = l_split[0]
                doc_line = l_split[1]
            doc_dict[current_field] = (
                doc_dict.get(current_field, "") + doc_line.rstrip() + " "
            )
        return doc_dict
