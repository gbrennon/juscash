from datetime import datetime
from scraper.infrastructure.crawlers.request_builders import (
    CaseSearchRequestBuilder,
    CourtCaseExtractorFilters
)

class TestCaseSearchRequestBuilder:
    def test_build_when_start_date_is_set_then_str_start_date_is_included(self):
        builder = CaseSearchRequestBuilder()
        filters = CourtCaseExtractorFilters(
            start_date=datetime(2023, 1, 1)
        )

        request = builder.build(filters)

        assert request["data"]["dadosConsulta.dtInicio"] == "01/01/2023"

    def test_build_when_end_date_is_set_then_str_end_date_is_included(self):
        builder = CaseSearchRequestBuilder()
        filters = CourtCaseExtractorFilters(
            end_date=datetime(2023, 2, 5)
        )

        request = builder.build(filters)

        assert request["data"]["dadosConsulta.dtFim"] == "05/02/2023"

    def test_build_when_section_id_is_set_then_int_is_casted(self):
        builder = CaseSearchRequestBuilder()
        filters = CourtCaseExtractorFilters(
            section_id=123  # use integer, as expected by the dataclass
        )

        request = builder.build(filters)

        assert request["data"]["dadosConsulta.cdCaderno"] == "123"  # should be string

    def test_build_when_search_terms_is_set_then_str_is_included(self):
        builder = CaseSearchRequestBuilder()
        filters = CourtCaseExtractorFilters(
            search_terms="test search"
        )

        request = builder.build(filters)

        assert request["data"]["dadosConsulta.pesquisaLivre"] == "test search"

    def test_build_when_no_filters_then_only_pagina_set_and_as_empty_string(self):
        builder = CaseSearchRequestBuilder()
        filters = CourtCaseExtractorFilters()

        request = builder.build(filters)

        assert request["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
        assert request["url"] == "https://dje.tjsp.jus.br/cdje/consultaAvancada.do"
        assert request["method"] == "POST"
        assert request["data"]["pagina"] == ""
        assert len(request["data"]) == 1  # only 'pagina' present

    def test_build_when_all_filters_then_all_included(self):
        builder = CaseSearchRequestBuilder()
        filters = CourtCaseExtractorFilters(
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 2, 5),
            section_id=123,
            search_terms="test search"
        )

        request = builder.build(filters)

        assert request["data"]["dadosConsulta.dtInicio"] == "01/01/2023"
        assert request["data"]["dadosConsulta.dtFim"] == "05/02/2023"
        assert request["data"]["dadosConsulta.cdCaderno"] == "123"
        assert request["data"]["dadosConsulta.pesquisaLivre"] == "test search"
        assert request["data"]["pagina"] == ""
