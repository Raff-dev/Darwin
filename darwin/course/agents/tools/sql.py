import sqlite3
from sqlite3 import OperationalError

from langchain.tools import Tool
from pydantic.v1 import BaseModel  # type: ignore

conn = sqlite3.connect("/darwin/course/agents/db.sqlite")


def list_tables() -> str | OperationalError:
    result = _run_sqlite_query("SELECT name FROM sqlite_master WHERE type='table';")
    if isinstance(result, OperationalError):
        return result
    tables = "\n".join([row[0] for row in result if row[0] is not None])
    return tables


def _run_sqlite_query(query: str) -> list[dict] | OperationalError:
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except OperationalError as err:
        return err


def _describe_tables(table_names: list[str]) -> str | OperationalError:
    tables = ", ".join(f"'{table}'" for table in table_names)
    result = _run_sqlite_query(
        f"SELECT sql FROM sqlite_master WHERE type='table' AND name IN ({tables});"
    )
    if isinstance(result, OperationalError):
        return result
    return "\n".join([row[0] for row in result if row[0] is not None])


class RunQueryArgsSchema(BaseModel):
    query: str


class DescribeTableArgsSchema(BaseModel):
    table_names: list[str]


run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a query on the sqlite database",
    func=_run_sqlite_query,
    args_schema=RunQueryArgsSchema,
)

describe_table_tool = Tool.from_function(
    name="describe_table",
    description="Given a list of tables, returns the schema of the tables",
    func=_describe_tables,
    args_schema=DescribeTableArgsSchema,
)
