from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel


def _write_report(filename: str, html: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)


class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str


write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="Write a report to a file. Use this tool whenever asked for a report.",
    func=_write_report,
    args_schema=WriteReportArgsSchema,
)
