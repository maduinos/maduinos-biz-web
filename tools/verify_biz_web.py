#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import sys
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTACT_EMAIL = "whjeong@maduinos.com"
CUSTOM_DOMAIN = "biz.maduinos.com"
PROFILE_IMAGE_SHA256 = {
    "assets/profile-icon.png": "b5cc4bdd49dc62f09faed8c446b81801a36ee6b703d29734c2bc14d7639f07c0",
    "assets/profile-github.png": "b5cc4bdd49dc62f09faed8c446b81801a36ee6b703d29734c2bc14d7639f07c0",
    "assets/profile-youtube.png": "c596e8cf9e7eaa86fd10c465c99b77cbed13132433935823a748edfe54e2156f",
}


REQUIRED_FILES = [
    "README.md",
    "CNAME",
    "favicon.ico",
    "index.html",
    ".github/workflows/deploy-pages.yml",
    "assets/maduinos-biz.css",
    "assets/apple-touch-icon.png",
    "assets/favicon-32.png",
    "assets/hero-edge-ai-fpga.png",
    "assets/zm4-module-render.png",
    "assets/zm4-fpga-som-module.png",
    "assets/edge-ai-carrier-lab.png",
    "assets/tdc-cis-lab-system.png",
    "assets/profile-github.png",
    "assets/profile-youtube.png",
    "assets/profile-icon.png",
    "pages/ai-edge-vision.html",
    "pages/fpga-education-consulting.html",
    "pages/fpga-product-poc.html",
    "pages/zm4-module.html",
]

REQUIRED_PUBLIC_TERMS = [
    "FPGA 기반 센서 처리 기술과 ZM4 플랫폼",
    "Camera / TDC / CIS",
    "Camera capture",
    "TDC timing",
    "CIS sensor processing",
    "FPGA/Zynq data path",
    "보편적인 기술 다이어그램",
    "개발 중인 ZM4 플랫폼",
    "ZM4 FPGA SoM",
    "바로 제공 가능",
    "FPGA/Zynq 실무 교육",
    "FPGA / Embedded / Edge AI / Hardware Prototyping",
    "기술 컨설팅",
    "임베디드 제품 PoC",
    "Target Specification",
    "Sensor Input",
    "FPGA Capture",
    "Processing",
    "Host & Validation",
    "register map",
    "timing capture log",
    "CSV log",
    "host CLI",
    "bring-up checklist",
    "validation report",
    "교육/컨설팅 상세 페이지",
    "기술 검토 요청",
    "1주 기술 진단",
    "2~4주 센서 PoC",
    "문의 전 준비 자료",
    "샘플 산출물",
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
]

REQUIRED_SECTIONS = [
    "hero",
    "technologies",
    "platform",
    "available-now",
    "details",
    "contact",
]

FORBIDDEN_PUBLIC_LINKS = [
    "2023/10/live-fpga.html",
    "2023/10/xilinx-fpgazynq.html",
    "2023/10/blog-post.html",
    "2023/10/vod.html",
]

FORBIDDEN_PUBLIC_PHRASES = [
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
]

REQUIRED_WORKFLOW_SNIPPETS = [
    "actions/checkout@v6.0.2",
    "actions/configure-pages@v6.0.0",
    "actions/upload-pages-artifact@v5.0.0",
    "actions/deploy-pages@v5.0.0",
    "python3 tools/verify_biz_web.py",
    "cp -R assets pages index.html favicon.ico CNAME _site/",
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


def ensure_icon_only_profiles() -> None:
    for path, expected_digest in PROFILE_IMAGE_SHA256.items():
        digest = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        if digest != expected_digest:
            fail(f"{path} should be the approved icon-only profile image")


def ensure_large_favicon_face() -> None:
    data = (ROOT / "assets/favicon-32.png").read_bytes()
    # The face-only favicon should occupy enough of the 32px canvas to stay legible.
    # Minimal PNG parsing is intentionally avoided here; the approved asset hash
    # covers composition while png_size covers dimensions.
    digest = hashlib.sha256(data).hexdigest()
    expected = "2bd3772c67846a09072260ee4ce045c0d1a32a844563ea8961acfa3c39383f5e"
    if digest != expected:
        fail("assets/favicon-32.png should be the approved large face-only favicon")


def check_brand_icons(files: list[Path]) -> None:
    expected_sizes = {
        "assets/favicon-32.png": (32, 32),
        "assets/apple-touch-icon.png": (180, 180),
        "assets/profile-github.png": (1024, 1024),
        "assets/profile-youtube.png": (800, 800),
        "assets/profile-icon.png": (1024, 1024),
    }
    for path, expected in expected_sizes.items():
        actual = png_size(path)
        if actual != expected:
            fail(f"{path} should be {expected[0]}x{expected[1]}, got {actual[0]}x{actual[1]}")

    ensure_icon_only_profiles()
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
        "MADUINOS는 Camera, TDC, CIS 센서 입력을 FPGA/Zynq 기반 capture, timing, preprocessing 구조로 연결하는 기술을 개발합니다.",
        "교육/컨설팅과 임베디드 제품 PoC는 지금 바로 제공하고",
        "ZM4 FPGA SoM 기반 센서 처리 플랫폼은 개발 중입니다.",
        "FPGA / Embedded / Edge AI / Hardware Prototyping",
        "보편적인 기술 다이어그램",
        "Camera / TDC / CIS",
        "바로 제공 가능",
        "개발 중인 ZM4 플랫폼",
        "기술 검토 요청",
        "1주 기술 진단",
        "2~4주 센서 PoC",
        "문의 전 준비 자료",
        "샘플 산출물",
        'rel="canonical"',
        'property="og:title"',
        'name="twitter:card"',
        "data-media-src",
        "hero-media-image",
        "hero-disciplines",
        "email-line",
        "assets/tdc-cis-lab-system.png",
        "technology-flow",
        "상세 페이지",
        "page-link-grid",
        "pages/ai-edge-vision.html",
        "pages/zm4-module.html",
        "pages/fpga-product-poc.html",
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
    ]:
        if customer_hidden in preview:
            fail(f"customer-facing page should not expose: {customer_hidden}")

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
        fail("preview should link to the education/consulting detail page")

    if "width: 250px" not in css:
        fail("header logo should be enlarged for stronger brand presence")

    if "var(--" not in css:
        fail("CSS should use design tokens via custom properties")

    if "word-break: keep-all" not in css:
        fail("CSS should prevent awkward Korean character-level wrapping")

    for css_snippet in ["min-height: 760px"]:
        if css_snippet not in css:
            fail(f"CSS missing business overview styling: {css_snippet}")

    files = html_files()
    check_brand_icons(files)
    check_local_refs(files)

    print("ok: maduinos-biz-web artifacts passed structural/content checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
