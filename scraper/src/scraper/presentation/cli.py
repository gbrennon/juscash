import asyncio
import datetime as dt

import typer

from scraper.domain.ports.court_case_extractor import CourtCaseExtractorFilters
from scraper.infrastructure.container import (
    get_db_session,
    get_extract_and_persist_course_case_service,
)

app = typer.Typer()


@app.callback()
def main():
    """Framework-agnostic, open-source court case scraper CLI."""


@app.command("scrape-for-day")
def scrape_for_day(date: str = typer.Argument(..., help="Date in YYYY-MM-DD")):
    """Scrape cases for a single day."""
    # Validate and convert string to date
    try:
        date_obj = dt.datetime.strptime(date, "%Y-%m-%d").date()
        typer.echo(f"Date provided: {date_obj}")
    except ValueError:
        typer.secho("Invalid date format. Use YYYY-MM-DD.", err=True, fg=typer.colors.RED)
        raise typer.Exit(1)

    async def inner():
        async with get_db_session() as session:
            service = get_extract_and_persist_course_case_service(session)
            filters = CourtCaseExtractorFilters(
                start_date=date_obj,  # <-- pass as date object!
                end_date=date_obj,
                section_id=None,
                search_terms='"RPV"+e+"pagamento+pelo+INSS"',
            )
            await service.execute(filters)
            typer.echo(f"Extracted and persisted cases for {date_obj}.")

    asyncio.run(inner())


if __name__ == "__main__":
    app()
