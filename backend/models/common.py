from typing import Any
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any):
        from pydantic_core import core_schema

        def validate_from_str(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)

        # Schema for incoming data (validation)
        python_schema = core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(validate_from_str),
                    ]
                ),
            ]
        )

        # Schema for outgoing data (serialization) and for JSON Schema generation
        serialization_and_json_schema = core_schema.str_schema(
            pattern=r"^[0-9a-fA-F]{24}$"
        )

        return core_schema.json_or_python_schema(
            python_schema=python_schema,
            json_schema=serialization_and_json_schema,
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )