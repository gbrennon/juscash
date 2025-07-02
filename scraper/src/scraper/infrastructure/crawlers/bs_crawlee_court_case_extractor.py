import asyncio
import io
import re
from datetime import datetime
from decimal import Decimal
from urllib.parse import parse_qs, urlencode, urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from scraper.domain.court_case import CourtCase, CourtCaseAmount, CourtCaseStatus
from scraper.domain.ports.court_case_extractor import (
    CourtCaseExtractor,
    CourtCaseExtractorFilters,
)

try:
    from pdfminer.high_level import extract_text as pdfminer_extract_text
except ImportError:
    pdfminer_extract_text = None

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

BASE_URL = "https://dje.tjsp.jus.br/cdje/consultaAvancada.do"
BASE_URL_ROOT = "https://dje.tjsp.jus.br"


class BsCrawleeCourtCaseExtractor(CourtCaseExtractor):
    def __init__(self, url: str = BASE_URL, base_url_root: str = BASE_URL_ROOT) -> None:
        self.url = url
        self.base_url_root = base_url_root

    async def extract(
        self, filters: CourtCaseExtractorFilters
    ) -> list[CourtCase]:
        max_exported: int = 1000
        print(f"Extracting court cases with filters: {filters}")
        extracted_cases: list[CourtCase] = []
        published_at_fallback = filters.start_date if filters.start_date else datetime.now()
        page_num = 1
        seen_pages: set[int] = set()
        user_agent = "Mozilla/5.0 (compatible; CourtCaseExtractor/1.0)"

        with httpx.Client(headers={"User-Agent": user_agent}) as s:
            stop_due_to_problem = False

            while not stop_due_to_problem:
                print("**" * 5, f"Exported count so far: {len(extracted_cases)}", "**" * 5)
                if len(extracted_cases) >= max_exported:
                    print(f"Reached max exported count: {max_exported}. Stopping extraction.")
                    break
                print(f"Fetching page {page_num}")
                search_html = self._submit_request_with_session(s, filters, page_num)
                soup = BeautifulSoup(search_html, "html.parser")
                seen_pages.add(page_num)

                popup_urls = []
                for row in soup.select("tr"):
                    link = row.select_one('a.layout[title="Visualizar"]')
                    if not link:
                        continue
                    onclick_attr = link.get("onclick", "")
                    popup_url = self._extract_popup_url_from_onclick(onclick_attr)
                    if not popup_url:
                        continue
                    popup_urls.append(urljoin(self.base_url_root, popup_url))

                if not popup_urls:
                    print("No popups found on this page.")
                    break

                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(user_agent=user_agent)
                    await context.add_cookies(self._get_cookies_for_playwright(s.cookies.jar))

                    def log_request(request):
                        print(f"[Network] {request.method} {request.url}")

                    context.on("request", log_request)

                    for detail_url in popup_urls:
                        if len(extracted_cases) >= max_exported:
                            print(
                                f"Reached max exported count: {max_exported}. Stopping extraction."
                            )
                            break
                        print(f"Fetching detail page: {detail_url}")
                        detail_page = await context.new_page()
                        response = await detail_page.goto(detail_url)
                        await detail_page.wait_for_load_state("domcontentloaded")

                        main_html = await detail_page.content()
                        with open("debug_main_page.html", "w", encoding="utf-8") as f:
                            f.write(main_html)

                        for fr in detail_page.frames:
                            try:
                                fr_html = await fr.content()
                                with open(
                                    f"debug_{fr.name}_frame.html", "w", encoding="utf-8"
                                ) as f2:
                                    f2.write(fr_html)
                            except Exception:
                                pass

                        frame_html = ""
                        frame = None
                        for _ in range(10):
                            frame = detail_page.frame(name="bottomFrame")
                            if frame:
                                break
                            await asyncio.sleep(0.2)

                        problem_detected = False
                        problem_reason = None
                        pdf_text = None

                        def fetch_pdf_fallback(detail_url):
                            parsed = urlparse(detail_url)
                            params = parse_qs(parsed.query)
                            base_get_pagina = (
                                f"{parsed.scheme}://{parsed.netloc}/cdje/getPaginaDoDiario.do"
                            )
                            get_params = {
                                "cdVolume": params.get("cdVolume", [""])[0],
                                "nuDiario": params.get("nuDiario", [""])[0],
                                "cdCaderno": params.get("cdCaderno", [""])[0],
                                "nuSeqpagina": params.get("nuSeqpagina", [""])[0],
                                "uuidCaptcha": "",
                            }
                            get_url = base_get_pagina + "?" + urlencode(get_params)
                            print(f"[Toolkit] Fallback GET: {get_url}")
                            try:
                                resp = httpx.get(get_url)
                                content_type = resp.headers.get("content-type", "")
                                if (
                                    resp.content[:5] == b"%PDF-"
                                    or "application/pdf" in content_type
                                ):
                                    pdf_path = "debug_fallback_getPaginaDoDiario.pdf"
                                    with open(pdf_path, "wb") as f:
                                        f.write(resp.content)
                                    print(f"[Toolkit] Fallback returned a PDF. Saved as {pdf_path}")
                                    extracted_pdf_text = ""
                                    if pdfminer_extract_text:
                                        try:
                                            extracted_pdf_text = pdfminer_extract_text(
                                                io.BytesIO(resp.content)
                                            )
                                            print(
                                                "[Toolkit] PDFMiner text extract (first 2000 chars):"
                                            )
                                            print(extracted_pdf_text[:2000])
                                        except Exception as e:
                                            print("[Toolkit] PDFMiner extraction failed:", e)
                                    if not extracted_pdf_text and PdfReader:
                                        try:
                                            reader = PdfReader(io.BytesIO(resp.content))
                                            pages = [p.extract_text() for p in reader.pages]
                                            extracted_pdf_text = "\n".join([p or "" for p in pages])
                                            print(
                                                "[Toolkit] PyPDF2 text extract (first 2000 chars):"
                                            )
                                            print(extracted_pdf_text[:2000])
                                        except Exception as e:
                                            print("[Toolkit] PyPDF2 extraction failed:", e)
                                    return None, "Fallback returned a PDF file", extracted_pdf_text
                                else:
                                    print("[Toolkit] Fallback fetch result (first 3000 chars):")
                                    print(resp.text[:3000])
                                    with open(
                                        "debug_fallback_getPaginaDoDiario.html",
                                        "w",
                                        encoding="utf-8",
                                    ) as f:
                                        f.write(resp.text)
                                    if (
                                        "<title>Insert title here" in resp.text
                                        or "processando" in resp.text
                                        or "BENV_exibeProcessando" in resp.text
                                        or len(resp.text.strip()) <= 50
                                    ):
                                        return (
                                            None,
                                            "Fallback returned only placeholder/empty content",
                                            None,
                                        )
                                    return resp.text, None, None
                            except Exception as ex:
                                print(f"[Toolkit] Fallback request failed: {ex}")
                                return None, "Fallback fetch failed", None

                        if not frame:
                            frame_html = ""
                            frame_html, fallback_err, pdf_text = fetch_pdf_fallback(detail_url)
                            if not frame_html and not pdf_text:
                                problem_detected = True
                                problem_reason = (
                                    f"bottomFrame not found and fallback failed: {fallback_err}"
                                )
                        else:
                            for _ in range(50):
                                if (
                                    frame.url
                                    and "processando.do" not in frame.url
                                    and "about:blank" not in frame.url
                                ):
                                    break
                                await asyncio.sleep(0.2)
                            if "processando.do" in frame.url or "about:blank" in frame.url:
                                frame_html_temp = await frame.content()
                                meta_refresh = re.search(
                                    r'<meta\s+http-equiv=["\']refresh["\']\s+content=["\'][^;]+;\s*url=([^"\'>]+)',
                                    frame_html_temp,
                                    re.IGNORECASE,
                                )
                                if meta_refresh:
                                    next_url = meta_refresh.group(1)
                                    abs_next_url = urljoin(frame.url, next_url)
                                    await frame.goto(abs_next_url)
                                    await asyncio.sleep(1)
                                    frame_html = await frame.content()
                                else:
                                    js_redirect = re.search(
                                        r'window\.location\.href\s*=\s*[\'"]([^\'"]+)[\'"]',
                                        frame_html_temp,
                                    )
                                    if js_redirect:
                                        next_url = js_redirect.group(1)
                                        abs_next_url = urljoin(frame.url, next_url)
                                        await frame.goto(abs_next_url)
                                        await asyncio.sleep(1)
                                        frame_html = await frame.content()
                                    else:
                                        frame_html = frame_html_temp
                                        if (
                                            "<title>Insert title here" in frame_html
                                            or "processando" in frame_html
                                            or "BENV_exibeProcessando" in frame_html
                                        ):
                                            frame_html, fallback_err, pdf_text = fetch_pdf_fallback(
                                                detail_url
                                            )
                                            if not frame_html and not pdf_text:
                                                problem_detected = True
                                                problem_reason = f"Frame stuck on processando/do and fallback not usable: {fallback_err}"
                            else:
                                frame_html = await frame.content()
                                if (
                                    "<title>Insert title here" in frame_html
                                    or "processando" in frame_html
                                    or "BENV_exibeProcessando" in frame_html
                                ):
                                    frame_html, fallback_err, pdf_text = fetch_pdf_fallback(
                                        detail_url
                                    )
                                    if not frame_html and not pdf_text:
                                        problem_detected = True
                                        problem_reason = f"Frame loaded but only placeholder/processando content and fallback not usable: {fallback_err}"

                        await detail_page.close()
                        if problem_detected:
                            print(
                                f"[ERROR] Problem detected: {problem_reason}. Will stop processing."
                            )
                            stop_due_to_problem = True
                            break

                        # Add new logic to stop after max_exported cases!
                        if frame_html:
                            cases = self._parse_detail_html(frame_html, published_at_fallback)
                        elif pdf_text:
                            cases = self._parse_detail_pdf_text(pdf_text, published_at_fallback)
                        else:
                            cases = []

                        for case in cases:
                            if len(extracted_cases) >= max_exported:
                                print(
                                    f"Reached max exported count: {max_exported}. Stopping extraction."
                                )
                                stop_due_to_problem = True
                                break
                            extracted_cases.append(case)

                        if stop_due_to_problem:
                            break

                    await browser.close()

                if stop_due_to_problem:
                    print("[Debug] Breaking page loop due to threshold or error.")
                    break

                next_page = self._find_next_page(soup, seen_pages)
                if next_page:
                    page_num = next_page
                else:
                    break

        print(f"ExportedCount: {len(extracted_cases)} cases")
        return extracted_cases

    def _submit_request_with_session(
        self, s: httpx.Client, filters: CourtCaseExtractorFilters, page_num: int = 1
    ) -> str:
        url = self.url
        data_inicial = self._convert_date_to_ddmmyyyy(filters.start_date)
        data_final = self._convert_date_to_ddmmyyyy(filters.end_date)
        data = {
            "dadosConsulta.dtInicio": data_inicial,
            "dadosConsulta.dtFim": data_final,
            "dadosConsulta.cdCaderno": getattr(filters, "section_id", None) or "12",
            "dadosConsulta.pesquisaLivre": getattr(filters, "search_terms", None) or "",
            "pagina": str(page_num),
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (compatible; CourtCaseExtractor/1.0)",
        }
        response = s.post(url, data=data, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")
        return response.text

    def _convert_date_to_ddmmyyyy(self, date_obj: datetime | None) -> str:
        if not date_obj:
            return ""
        try:
            return date_obj.strftime("%d/%m/%Y")
        except ValueError as e:
            print(f"Error converting date: {e}")
            return ""

    def _extract_popup_url_from_onclick(self, onclick: str) -> str | None:
        match = re.search(r"popup\('([^']+)'\)", onclick)
        if match:
            return match.group(1)
        return None

    def _find_next_page(self, soup: BeautifulSoup, seen_pages: set[int]) -> int | None:
        nav_span = soup.find("span", class_="style5")
        if not nav_span:
            return None
        for a in nav_span.find_all("a"):
            onclick = a.get("onclick", "")
            match = re.search(r"trocaDePg\((\d+)\)", onclick)
            if match:
                page_num = int(match.group(1))
                if page_num not in seen_pages:
                    return page_num
        return None

    def _get_cookies_for_playwright(self, httpx_jar) -> list[dict]:
        cookies = []
        for cookie in httpx_jar:
            cookies.append(
                {
                    "name": cookie.name,
                    "value": cookie.value,
                    "domain": cookie.domain,
                    "path": cookie.path,
                    "expires": int(cookie.expires) if cookie.expires else -1,
                    "httpOnly": getattr(cookie, "httponly", False),
                    "secure": cookie.secure,
                    "sameSite": "Lax",
                }
            )
        return cookies

    def _parse_detail_html(self, html: str, published_at_fallback: datetime) -> list[CourtCase]:
        soup = BeautifulSoup(html, "html.parser")
        plain_text = soup.get_text(separator="\n", strip=True)
        cases = []
        published_at = published_at_fallback
        published_at_match = re.search(r"Disponibiliza[çc][aã]o: ([^\n]+)", plain_text)
        if published_at_match:
            date_str = published_at_match.group(1).split("Diário")[0].strip()
            try:
                published_at = datetime.strptime(date_str, "%A, %d de %B de %Y")
            except Exception as e:
                print(f"Could not parse published_at: {e}")

        process_blocks = re.split(r"(?=PROCESSO\s*:)", plain_text)
        for block in process_blocks:
            process_match = re.search(r"PROCESSO\s*:\s*([0-9\-.]+)", block)
            lawyer_match = re.search(r"ADVOGADO\s*:\s*(.+)", block)
            if process_match:
                case_id = process_match.group(1).strip()
                lawyer = lawyer_match.group(1).strip() if lawyer_match else ""
                court_case_amount = CourtCaseAmount(
                    Decimal("1000.00"), Decimal("1000.00"), Decimal("1000.00")
                )
                case = CourtCase(
                    id=case_id,
                    name=f"Case for {case_id}",
                    lawyers=[lawyer] if lawyer else [],
                    status=CourtCaseStatus.NEW,
                    amount=court_case_amount,
                    published_at=published_at,
                    content=block.strip(),
                )
                cases.append(case)
        return cases

    def _parse_detail_pdf_text(
        self, pdf_text: str, published_at_fallback: datetime
    ) -> list[CourtCase]:
        """
        Parses extracted PDF text to return a list of CourtCase objects.
        You can improve this regex logic as needed for your court's document format.
        """
        # Example: Match lines like 'Processo 0004319-12.2018.8.26.0509 - Execução da Pena - Aberto - ...'
        cases = []
        published_at = published_at_fallback
        # Try to extract a publish date from the top of the PDF
        published_at_match = re.search(r"Disponibiliza[çc][aã]o: ([^\n]+)", pdf_text)
        if published_at_match:
            date_str = published_at_match.group(1).split("Diário")[0].strip()
            try:
                published_at = datetime.strptime(date_str, "%A, %d de %B de %Y")
            except Exception as e:
                print(f"Could not parse published_at from PDF: {e}")

        # Find all process blocks
        process_pattern = re.compile(
            r"(Processo\s*(?P<id>\d{7,}-\d{2}\.\d{4}\.\d{1,2}\.\d{2}\.\d{4}).*?)(?=Processo\s*\d{7,}-\d{2}\.\d{4}\.\d{1,2}\.\d{2}\.\d{4}|$)",
            re.DOTALL,
        )
        matches = process_pattern.finditer(pdf_text)
        for match in matches:
            block = match.group(0)
            case_id = match.group("id")
            lawyer_match = re.search(r"ADV:\s*([A-ZÁ-Úa-zá-ú\s]+)\s*\(OAB\s*[\d\w/]+\)", block)
            lawyer = lawyer_match.group(1).strip() if lawyer_match else ""
            court_case_amount = CourtCaseAmount(
                Decimal("1000.00"), Decimal("1000.00"), Decimal("1000.00")
            )
            case = CourtCase(
                id=case_id,
                name=f"Case for {case_id}",
                lawyers=[lawyer] if lawyer else [],
                status=CourtCaseStatus.NEW,
                amount=court_case_amount,
                published_at=published_at,
                content=block.strip(),
            )
            cases.append(case)
        print(f"Extracted {len(cases)} cases from PDF text")
        return cases
