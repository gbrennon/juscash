from dataclasses import dataclass
from datetime import datetime
from typing import Any

BASE_URL = "https://dje.tjsp.jus.br/cdje/consultaAvancada.do"


@dataclass(frozen=True)
class CourtCaseSearchFilters:
    """Filters for court case extraction."""

    start_date: datetime | None = None
    end_date: datetime | None = None
    section_id: str | None = None
    search_terms: str | None = None


class CaseSearchRequestBuilder:
    """Builds POST requests for court case searches."""

    def build(self, filters: CourtCaseSearchFilters) -> dict[str, Any]:
        """
        Build POST request data for court search.

        :param filters: Search filters
        :return: Request configuration dictionary
        """
        # Build form data
        form_data = {}

        if filters.start_date:
            form_data["dadosConsulta.dtInicio"] = filters.start_date.strftime(
                "%d/%m/%Y"
            )

        if filters.end_date:
            form_data["dadosConsulta.dtFim"] = filters.end_date.strftime("%d/%m/%Y")

        if filters.section_id is not None:
            form_data["dadosConsulta.cdCaderno"] = str(filters.section_id)

        if filters.search_terms:
            form_data["dadosConsulta.pesquisaLivre"] = filters.search_terms

        # Always include pagination parameter
        form_data["pagina"] = ""

        # Build headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        return {
            "url": BASE_URL,
            "method": "POST",
            "headers": headers,
            "data": form_data,
        }
