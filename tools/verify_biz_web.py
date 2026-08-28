#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import sys
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTACT_EMAIL = "whjeong@maduinos.com"
CUSTOM_DOMAIN = "maduinos.com"
BRAND_LINE = "FPGA & EMBEDDED SYSTEMS"
BUSINESS_FOOTER_SNIPPETS = [
    "상호: 매두이노",
    "대표: 정우현",
    "사업자등록번호: 740-29-01506",
    "통신판매업신고번호: 제2024-용인기흥-3949호",
    "업태: 정보통신업 · 종목: 미디어콘텐츠창작업",
    "이메일: whjeong@maduinos.com",
]
REQUIRED_FILES = [
    "README.md",
    "CNAME",
    "favicon.ico",
    "index.html",
    "404.html",
    "robots.txt",
    "sitemap.xml",
    ".github/workflows/deploy-pages.yml",
    "assets/maduinos-biz.css",
    "assets/apple-touch-icon.png",
    "assets/favicon-32.png",
    "assets/maduinos_wordmark_reference_clean.png",
    "assets/zm4-zm4mpsoc-black-som-module.webp",
    "assets/edge-ai-carrier-lab.webp",
    "assets/tdc-cis-lab-system.webp",
    "assets/tdc-timing-applications.webp",
    "assets/cis-application-markets.webp",
    "assets/og-home.jpg",
    "assets/og-tdc.jpg",
    "assets/og-cis.jpg",
    "assets/og-zm4.jpg",
    "assets/og-education.jpg",
    "pages/ai-edge-vision.html",
    "pages/tdc-module.html",
    "pages/cis-module.html",
    "pages/fpga-education-consulting.html",
    "pages/fpga-product-poc.html",
    "pages/zm4-module.html",
]

REQUIRED_PUBLIC_TERMS = [
    BRAND_LINE,
    "FPGA 기반 고속 센서 시스템 개발",
    "교육 및 강의",
    "고객 맞춤형 교육",
    "고객 보드 Bring-Up",
    "FPGA VOD 강의 목차",
    "레벨별 커리큘럼",
    "Verilog HDL",
    "Zynq / Zynq MPSoC",
    "Zynq7000 초급",
    "Zynq7000 중급",
    "Zynq7000 고급",
    "LVDS",
    "FPGA 기반 TDC 모듈",
    "거리 분해능 4mm",
    "기본 16채널",
    "다이나믹 동작 시 수십채널 가능",
    "최대 거리에 따라 가변",
    "거리에 따라 가변 가능",
    "USB2.0",
    "이더넷 100/1000Mbps",
    "UART, CAN",
    "5V/12V/24V",
    "0°C ~ 65°C",
    "CIS 기반 모듈",
    "지폐계수기",
    "투표장치",
    "공장 라인스캔센서",
    "CIS 기반 영상인식이 필요한 모든 고속 장치",
    "R/G/B/IR/UV",
    "16us/line",
    "제품 이미지",
    "기술 다이어그램",
    "상세 스펙",
    "어플리케이션 영역",
    "제품 라인",
    "문의 전 준비 자료",
]

FORBIDDEN_PRIVATE_TERMS = [
    "퇴사",
    "연봉",
    "현금성",
    "이혼",
    "부양가족",
    "생활비",
    "집 주소",
    "전화번호",
    "개인 이메일",
    "생년월일",
    "1983년 10월 25일",
    "문서확인번호",
    "덕영대로2077번길",
    "204동 1904호",
    "청현마을기흥데시앙",
    "영덕동",
]

REQUIRED_SECTIONS = [
    "hero",
    "products",
    "contact",
]

FORBIDDEN_PUBLIC_LINKS = [
    "2023/10/live-fpga.html",
    "2023/10/xilinx-fpgazynq.html",
    "2023/10/blog-post.html",
    "2023/10/vod.html",
]

FORBIDDEN_PUBLIC_PHRASES = [
    "FPGA TRAINING & ENGINEERING",
    "고객이 이해하기 쉬운 6개 기술 사업축",
    "기술을 나열하지 않고",
    "먼저 내세우고",
    "운영하세요",
    "Pages Ready To Paste",
    "제품 PoC를 빠르게",
    "검증된 FPGA SoM 모듈",
    "양산 적용 범위",
    "양산 적용 항목",
    "Proof & Deliverables",
    "Proof &amp; Deliverables",
    "메시지는 데모 장식보다",
    "사이트 메시지는",
    "기존 상세 페이지는 그대로 유지합니다",
    "LiDAR",
    "Lidar",
    "lidar",
    "라이다",
    "한 화면에서 선택",
    "선택합니다",
    "원하는 항목 선택",
    "고객이 원하는",
    "고객은 현재",
    "First Screen Choice",
    "Choice",
    "경쟁 모듈",
    "경쟁",
    "제품 개발에 필요한 언어로 정리합니다",
    "ATM",
    "FPGA 교육과 모듈 제품",
    "교육 및 강의 제품",
    "FPGA 기반 TDC 모듈 제품",
    "CIS 기반 모듈 제품",
    "ZM4 SoM 모듈 제품",
    "채널 수 32",
    "32채널",
    "32 channels",
    "XC7Z010",
    "G32",
    "AC7Z010",
    "AC78Z010",
    "ac7z010",
    "ac78z010",
    "FPGA fabric",
    "Artix",
    "676MHz",
    "수신 기술",
    "SiPM",
    "1000Base-T1",
    "프레임 속도 10 / 20 / 25Hz",
    "10 / 20 / 25Hz",
    "raw echo 3",
    "3 echo raw data",
    "3 echo",
    "12V, 1A",
    "전류",
    "IP67",
    "-40°C",
    "105°C",
    "119 x 95 x 77",
    "730g",
    "기구 기준",
    "Optics",
    "rod lens",
    "20us/line",
    "35 x 42 mm",
]

REQUIRED_WORKFLOW_SNIPPETS = [
    "actions/checkout@v6.0.2",
    "actions/configure-pages@v6.0.0",
    "actions/upload-pages-artifact@v5.0.0",
    "actions/deploy-pages@v5.0.0",
    "python3 tools/verify_biz_web.py",
    "cp -R assets pages index.html 404.html favicon.ico CNAME robots.txt sitemap.xml _site/",
    "path: _site",
    "pages: write",
    "id-token: write",
    "workflow_dispatch:",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def read(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        fail(f"missing required file: {path}")
    return p.read_text(encoding="utf-8")


def html_files() -> list[Path]:
    return [ROOT / "index.html", *sorted((ROOT / "pages").glob("*.html"))]


def all_public_html_files() -> list[Path]:
    return [ROOT / "index.html", ROOT / "404.html", *sorted((ROOT / "pages").glob("*.html"))]


def check_business_footer(files: list[Path]) -> None:
    for html_file in files:
        text = html_file.read_text(encoding="utf-8")
        if 'class="business-info"' not in text:
            fail(f"{html_file.relative_to(ROOT)} missing business info footer")
        if 'class="footer-links"' in text:
            fail(f"{html_file.relative_to(ROOT)} footer should not include product/home shortcut links")
        for snippet in BUSINESS_FOOTER_SNIPPETS:
            if snippet not in text:
                fail(f"{html_file.relative_to(ROOT)} missing business footer snippet: {snippet}")


def check_contact_sections(files: list[Path]) -> None:
    for html_file in files:
        text = html_file.read_text(encoding="utf-8")
        start = 0
        while True:
            start = text.find('class="shell contact-layout"', start)
            if start == -1:
                break
            end = text.find("</section>", start)
            if end == -1:
                fail(f"{html_file.relative_to(ROOT)} has an unterminated contact section")
            section = text[start:end]
            if "<img " in section or "mascot" in section:
                fail(f"{html_file.relative_to(ROOT)} contact section should not include character imagery")
            start = end + len("</section>")


def check_local_refs(files: list[Path]) -> None:
    for html_file in files:
        text = html_file.read_text(encoding="utf-8")
        for value in re.findall(r'(?:src|href)="([^"]+)"', text):
            if value.startswith(("#", "mailto:", "http://", "https://")):
                continue
            clean = value.split("#", 1)[0].split("?", 1)[0]
            target = (html_file.parent / urllib.parse.unquote(clean)).resolve()
            if not target.exists():
                fail(f"broken local reference in {html_file.relative_to(ROOT)}: {value}")


def png_size(path: str) -> tuple[int, int]:
    data = (ROOT / path).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"{path} should be a PNG file")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def ensure_large_favicon_face() -> None:
    data = (ROOT / "assets/favicon-32.png").read_bytes()
    # The favicon should occupy enough of the 32px canvas to stay legible.
    # Minimal PNG parsing is intentionally avoided here; the approved asset hash
    # covers composition while png_size covers dimensions.
    digest = hashlib.sha256(data).hexdigest()
    expected = "2bb5419c7ef0d624070bcec42efddb3e35a7f32a864baea3ba3365a0cba837a3"
    if digest != expected:
        fail("assets/favicon-32.png should be the approved M favicon")


def check_brand_icons(files: list[Path]) -> None:
    expected_sizes = {
        "assets/favicon-32.png": (32, 32),
        "assets/apple-touch-icon.png": (180, 180),
    }
    for path, expected in expected_sizes.items():
        actual = png_size(path)
        if actual != expected:
            fail(f"{path} should be {expected[0]}x{expected[1]}, got {actual[0]}x{actual[1]}")

    ensure_large_favicon_face()

    ico = (ROOT / "favicon.ico").read_bytes()
    if ico[:4] != b"\x00\x00\x01\x00":
        fail("favicon.ico should be a valid ICO file")

    for html_file in files:
        relative_prefix = "../" if html_file.parent.name == "pages" else ""
        text = html_file.read_text(encoding="utf-8")
        required_links = [
            f'href="{relative_prefix}favicon.ico"',
            f'href="{relative_prefix}assets/favicon-32.png"',
            f'href="{relative_prefix}assets/apple-touch-icon.png"',
        ]
        for snippet in required_links:
            if snippet not in text:
                fail(f"{html_file.relative_to(ROOT)} missing favicon link: {snippet}")


def main() -> int:
    for path in REQUIRED_FILES:
        if not (ROOT / path).exists():
            fail(f"missing required file: {path}")

    if ROOT.name != "maduinos-biz-web":
        fail(f"repository directory should be named maduinos-biz-web, got: {ROOT.name}")

    preview = read("index.html")
    css = read("assets/maduinos-biz.css")
    workflow = read(".github/workflows/deploy-pages.yml")
    cname = read("CNAME").strip()

    if cname != CUSTOM_DOMAIN:
        fail(f"CNAME should be exactly {CUSTOM_DOMAIN}")

    for section_id in REQUIRED_SECTIONS:
        pattern = rf'id=["\']{re.escape(section_id)}["\']'
        if not re.search(pattern, preview):
            fail(f"preview is missing section #{section_id}")

    detail_pages = [
        read("pages/ai-edge-vision.html"),
        read("pages/tdc-module.html"),
        read("pages/cis-module.html"),
        read("pages/fpga-education-consulting.html"),
        read("pages/fpga-product-poc.html"),
        read("pages/zm4-module.html"),
    ]
    combined_public = "\n".join([preview, read("README.md"), *detail_pages])
    for term in REQUIRED_PUBLIC_TERMS:
        if term not in combined_public:
            fail(f"missing public positioning term: {term}")

    combined_private = "\n".join([preview, *detail_pages])
    for term in FORBIDDEN_PRIVATE_TERMS:
        if term in combined_private:
            fail(f"private planning term leaked into public site: {term}")

    for link in FORBIDDEN_PUBLIC_LINKS:
        if link in combined_public:
            fail(f"old template/content link should not be used: {link}")

    for phrase in FORBIDDEN_PUBLIC_PHRASES:
        if phrase in combined_public:
            fail(f"internal-facing phrase leaked into public site: {phrase}")

    for snippet in REQUIRED_WORKFLOW_SNIPPETS:
        if snippet not in workflow:
            fail(f"GitHub Pages workflow missing snippet: {snippet}")

    if CONTACT_EMAIL not in combined_public:
        fail(f"public site is missing contact email: {CONTACT_EMAIL}")

    if f"mailto:{CONTACT_EMAIL}" not in preview:
        fail("preview contact section should link directly to the contact email")

    if "<form" in preview:
        fail("static preview should not include a non-functional contact form")

    required_preview_snippets = [
        BRAND_LINE,
        "FPGA 기반 고속 센서와",
        "CIS 라인스캔, 정밀 타이밍 계측, Zynq/MPSoC 시스템의 아키텍처 설계",
        "센서 입력부터 실시간 처리까지 연결합니다.",
        "사양 확인부터 검증까지 단계적으로 진행합니다.",
        "제품 라인",
        "교육 및 강의",
        "FPGA VOD 강의, 고객 맞춤형 교육, 고객 보드 Bring-Up",
        "고객 맞춤형 교육",
        "고객 보드 Bring-Up",
        "Zynq / Zynq MPSoC",
        "FPGA 기반 TDC 모듈",
        "기본 16채널",
        "다이나믹 동작 시 수십채널 가능",
        "USB2.0",
        "이더넷 100/1000Mbps",
        "UART, CAN",
        "CIS 기반 모듈",
        "투표장치",
        "CIS 기반 영상인식이 필요한 모든 고속 장치",
        "pages/tdc-module.html",
        "pages/cis-module.html",
        "pages/fpga-education-consulting.html",
        "tdc-timing-applications.webp",
        "cis-application-markets.webp",
        "문의 전 준비 자료",
        "전체 다이어그램",
        'rel="canonical"',
        'property="og:title"',
        'name="twitter:card"',
        "email-line",
        "solution-nav",
        "maduinos_wordmark_reference_clean.png",
        "brand-logo",
        "product-card-grid",
        "product-line-grid",
        "product-line-card",
    ]
    for snippet in required_preview_snippets:
        if snippet not in preview:
            fail(f"preview missing updated visual/copy snippet: {snippet}")

    if "Claim policy" in preview:
        fail("public pages should not show a Claim policy block")

    for customer_hidden in [
        "GitHub Pages",
        "서버형 문의 폼",
        "1st Data",
        "1st Logic",
        "1st Demo",
        "What You Get",
        "Engagement Model",
        "Trust Boundary",
        "Business at a glance",
        "id=\"capabilities\"",
        "id=\"engagement\"",
        "id=\"business-map\"",
        "id=\"capabilities\"",
        "id='capabilities'",
        "id='engagement'",
        "id='business-map'",
        "CM4",
        "Raspberry Pi",
        "Compute Module",
        "drop-in replacement",
        "공식 Raspberry",
        "한 화면",
        ">선택<",
        "선택하세요",
        "바로 선택",
        "Business Areas",
        "사업 영역",
        "사업영역",
        'id="product-menu"',
        "id='product-menu'",
        'id="education"',
        "id='education'",
        'id="roadmap"',
        "id='roadmap'",
        "학습 로드맵",
        "Education Roadmap",
        "maduinos_wordmark.png",
        "자료:",
    ]:
        if customer_hidden in preview:
            fail(f"customer-facing page should not expose: {customer_hidden}")

    if 'class="business-model-card"' in preview or "business-model-grid" in preview:
        fail("homepage should not have a separate business areas card grid")

    if preview.count('class="product-line-card"') != 3:
        fail("homepage should present exactly three public offering cards")

    if "solution-card featured" in preview or ".solution-card.featured" in css:
        fail("product line should not visually promote one module over the other two")

    for raw_p in re.findall(r"<p(?:\s[^>]*)?>(.*?)</p>", preview, flags=re.S):
        text = re.sub(r"<[^>]+>", "", raw_p)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > 185:
            fail(f"homepage paragraph should stay concise for scanning: {text[:80]}...")

    for customer_hidden in [
        "CM4",
        "Raspberry Pi",
        "Compute Module",
        "drop-in replacement",
        "공식 Raspberry",
    ]:
        if customer_hidden in combined_public:
            fail(f"public artifacts should not expose old ZM4 positioning: {customer_hidden}")

    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT).as_posix()
        if ".git/" in relative or relative.startswith(".git/"):
            continue
        for forbidden_path_term in ["cm4", "raspberry", "compute-module"]:
            if forbidden_path_term in relative.lower():
                fail(f"public repository path should not expose old ZM4 positioning: {relative}")

    if "pages/fpga-education-consulting.html" not in preview:
        fail("preview should link to the education content detail page")
    for link in ["pages/tdc-module.html", "pages/cis-module.html"]:
        if link not in preview:
            fail(f"preview should link directly to product detail page: {link}")

    if ".brand-logo" not in css or "width: 380px" not in css or "max-width: 82vw" not in css:
        fail("header brand should use the larger clean MADUINOS wordmark image")

    if "var(--" not in css:
        fail("CSS should use design tokens via custom properties")

    if "word-break: keep-all" not in css:
        fail("CSS should prevent awkward Korean character-level wrapping")

    for css_snippet in ["min-height: 760px", ".solution-nav", ".product-card-grid", ".product-line-grid"]:
        if css_snippet not in css:
            fail(f"CSS missing business overview styling: {css_snippet}")

    product_detail_paths = [
        "pages/fpga-education-consulting.html",
        "pages/tdc-module.html",
        "pages/cis-module.html",
    ]
    for path in product_detail_paths:
        text = read(path)
        for snippet in ['rel="canonical"', 'property="og:title"', 'property="og:image"', 'name="twitter:card"']:
            if snippet not in text:
                fail(f"{path} missing share/SEO metadata: {snippet}")
        if f'href="https://{CUSTOM_DOMAIN}/{path}"' not in text:
            fail(f"{path} canonical URL should match its public path")

    if 'name="robots" content="noindex, nofollow"' not in read("pages/zm4-module.html"):
        fail("unreleased ZM4 page should be noindex and nofollow")
    if "pages/zm4-module.html" in preview:
        fail("homepage should not link to the unreleased ZM4 page")

    for path in ["pages/ai-edge-vision.html", "pages/fpga-product-poc.html"]:
        if 'name="robots" content="noindex' not in read(path):
            fail(f"{path} legacy compatibility page should be noindex")

    sitemap = read("sitemap.xml")
    for url in [f"https://{CUSTOM_DOMAIN}/", *[f"https://{CUSTOM_DOMAIN}/{p}" for p in product_detail_paths]]:
        if f"<loc>{url}</loc>" not in sitemap:
            fail(f"sitemap.xml missing url: {url}")

    if f"Sitemap: https://{CUSTOM_DOMAIN}/sitemap.xml" not in read("robots.txt"):
        fail("robots.txt should point crawlers at sitemap.xml")

    files = html_files()
    check_business_footer(all_public_html_files())
    check_contact_sections(files)
    check_brand_icons(files)
    check_local_refs(files)

    print("ok: maduinos-biz-web artifacts passed structural/content checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
