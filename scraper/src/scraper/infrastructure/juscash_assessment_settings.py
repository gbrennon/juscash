from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class JuscashAssessmentSettings:
    """
    Settings for Juscash assessment.
    This class holds the configuration for the Juscash assessment process.
    """

    start_date: str = "13/11/2024"
    end_date: str = "13/11/2024"
    section_id: str = "12"
    search_query: str = '"RPV"+e+"pagamento pelo INSS"'
    timeout: timedelta = timedelta(seconds=30)
    max_requests_per_crawler: int = 10


assessment_settings = JuscashAssessmentSettings()
