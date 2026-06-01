# MADUINOS Biz Web

`maduinos-biz-web`는 MADUINOS 공개 비즈니스 홈페이지를 배포하는 정적 웹 저장소다. GitHub Pages Actions가 검증을 실행한 뒤 `index.html`, `pages`, `assets`, `CNAME`을 `_site` artifact로 묶어 배포한다.

## 파일 구조

- `index.html`: 메인 페이지
- `.github/workflows/deploy-pages.yml`: GitHub Pages Actions 배포 워크플로
- `CNAME`: 커스텀 도메인 `biz.maduinos.com`
- `favicon.ico`: 브라우저 탭용 MADUINOS 아이콘
- `assets/favicon-32.png`: PNG favicon
- `assets/apple-touch-icon.png`: iOS 홈 화면용 아이콘
- `assets/profile-github.png`: GitHub 프로필 업로드용 정사각 이미지
- `assets/profile-youtube.png`: YouTube 프로필 업로드용 정사각 이미지
- `assets/profile-icon.png`: 작은 원형 표시용 아이콘 중심 프로필 이미지
- `assets/maduinos-biz.css`: 공통 스타일
- `assets/maduinos_wordmark.png`: MADUINOS 워드마크
- `assets/hero-edge-ai-fpga.png`: ZM4 FPGA SoM 기반 Edge AI PoC hero 이미지
- `assets/edge-ai-carrier-lab.png`: 검증된 ZM4 보드와 carrier 기반 Edge AI PoC 이미지
- `assets/tdc-cis-lab-system.png`: TDC/CIS 센서 취득 개발 시스템 이미지
- `assets/zm4-fpga-som-module.png`: AMD Zynq 핵심 칩을 보여주는 ZM4 FPGA SoM 컨셉 렌더
- `assets/zm4-module-render.png`: ZM4 모듈 보조 렌더
- `pages/ai-edge-vision.html`: AI 기반 임베디드 인식 기술 상세 페이지
- `pages/fpga-education-consulting.html`: FPGA/Zynq 실무 교육 및 컨설팅 상세 페이지
- `pages/fpga-product-poc.html`: FPGA 기반 임베디드 제품 PoC 상세 페이지
- `pages/zm4-module.html`: ZM4 FPGA SoM 상세 페이지
- `tools/verify_biz_web.py`: 구조, 문구, 링크, 배포 설정 검증 스크립트

## 공개 포지셔닝

홈페이지는 고객이 맡기고 싶은 문제를 먼저 보여주고, 세부 기술은 상세 페이지로 분리한다.

- AI 기반 임베디드 인식 기술
- AMD FPGA 교육
- FPGA 기반 임베디드 제품 PoC
- FPGA 보드 브링업
- TDC 기술: 라이다, 초음파, 고속 거리측정
- CIS 이미지 센싱 및 인식 기술
- ZM4 FPGA SoM
- 검증된 보드와 MADUINOS 지원
- 양산 적용 검토까지 이어지는 FPGA SoM 모듈
- 임베디드 시스템 설계부터 제품화까지 대응

## ZM4 포지셔닝 원칙

ZM4는 센서 입력과 AMD Zynq 칩 기반 FPGA 처리를 빠르게 검증하기 위한 FPGA SoM 모듈로 표현한다.

- 핵심 메시지: `ZM4 FPGA SoM`, `검증된 보드`, `MADUINOS 지원`, `quick-start`, `양산 적용`
- 고객 가치는 검증된 보드에서 빠르게 시작하고, PoC 결과를 carrier/interface 적용과 제품화 판단으로 연결하는 것이다.
- 지원 항목은 MADUINOS가 검증한 board, carrier, interface, host tool, log package 기준으로 공개한다.

## 문의 원칙

공개 사이트의 문의 동선은 `whjeong@maduinos.com` 메일 주소로 유지한다. 고객-facing HTML에는 배포 방식이나 내부 구현을 노출하지 않는다.

## 배포 방향

1. GitHub 저장소 Settings > Pages에서 Source를 GitHub Actions로 설정한다.
2. `main` 브랜치에 push하거나 Actions에서 `Deploy MADUINOS Biz Web to GitHub Pages`를 수동 실행한다.
3. 워크플로는 `python3 tools/verify_biz_web.py`로 구조와 문구를 검증한 뒤 `_site` 디렉터리를 Pages artifact로 배포한다.
4. 첫 화면은 artifact 최상위의 `index.html`이며, 상세 페이지는 `pages/*.html` 경로로 연결된다.

## 검증

```bash
python3 tools/verify_biz_web.py
```

검증은 필수 파일, 공개 포지셔닝 문구, 내부 기획 문구 노출, 민감한 계획 문구 노출, 로컬 링크, GitHub Pages workflow, 한국어 줄바꿈 규칙을 확인한다.
