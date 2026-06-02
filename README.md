# MADUINOS Biz Web

`maduinos-biz-web`는 MADUINOS 공개 비즈니스 홈페이지를 배포하는 정적 웹 저장소다. GitHub Pages Actions가 검증을 실행한 뒤 `index.html`, `pages`, `assets`, `CNAME`을 `_site` artifact로 묶어 배포한다.

## 현재 포지셔닝

사이트의 중심 메시지는 `FPGA 기반 센서 처리 기술과 ZM4 플랫폼`이다.

- 메인 기술: `Camera / TDC / CIS` 센서 입력을 FPGA/Zynq 기반 `capture`, `timing`, `preprocessing` 구조로 연결한다.
- 기술 표현: 특정 완성 모듈을 과장하지 않고 `보편적인 기술 다이어그램`으로 `Sensor Input`, `FPGA Capture`, `Processing`, `Host & Validation` 흐름을 보여준다.
- 개발 중 플랫폼: `ZM4 FPGA SoM`은 `개발 중인 ZM4 플랫폼`으로 표현한다.
- 바로 제공 가능 범위: `FPGA/Zynq 실무 교육`, `기술 컨설팅`, `임베디드 제품 PoC`.
- 신뢰 근거: `register map`, `timing capture log`, `CSV log`, `host CLI`, `bring-up checklist`, `validation report`.
- 메인 페이지에는 기존 상세 페이지 4개로 연결되는 `상세 페이지` 섹션을 유지한다.

## 파일 구조

- `index.html`: 메인 페이지
- `.github/workflows/deploy-pages.yml`: GitHub Pages Actions 배포 워크플로
- `CNAME`: 커스텀 도메인 `biz.maduinos.com`
- `favicon.ico`: 브라우저 탭용 MADUINOS 아이콘
- `assets/favicon-32.png`: PNG favicon
- `assets/apple-touch-icon.png`: iOS 홈 화면용 아이콘
- `assets/profile-github.png`: GitHub 프로필 업로드용 아이콘 전용 정사각 이미지
- `assets/profile-youtube.png`: YouTube 프로필 업로드용 아이콘 전용 정사각 이미지
- `assets/profile-icon.png`: 작은 원형 표시용 아이콘 전용 프로필 이미지
- `assets/maduinos-biz.css`: 공통 스타일
- `assets/maduinos_wordmark.png`: MADUINOS 워드마크
- `assets/hero-edge-ai-fpga.png`: FPGA 센서 처리 hero 보조 이미지
- `assets/edge-ai-carrier-lab.png`: Camera capture와 carrier 기반 검증 이미지
- `assets/tdc-cis-lab-system.png`: TDC/CIS 센서 취득 개발 시스템 이미지
- `assets/zm4-fpga-som-module.png`: 개발 중인 ZM4 FPGA SoM 방향 이미지
- `assets/zm4-module-render.png`: ZM4 모듈 보조 렌더
- `pages/ai-edge-vision.html`: Camera/TDC/CIS 센서 처리 기술 상세 페이지
- `pages/fpga-education-consulting.html`: FPGA/Zynq 실무 교육 및 기술 컨설팅 상세 페이지
- `pages/fpga-product-poc.html`: 임베디드 제품 PoC 상세 페이지
- `pages/zm4-module.html`: 개발 중인 ZM4 플랫폼 상세 페이지
- `tools/verify_biz_web.py`: 구조, 문구, 링크, 배포 설정 검증 스크립트

## 공개 메시지 원칙

고객-facing HTML은 현재 제공 가능한 범위와 개발 중인 범위를 분리한다.

- `Camera capture`, `TDC timing`, `CIS sensor processing`, `FPGA/Zynq data path`는 보유 기술로 표현한다.
- `ZM4 FPGA SoM`은 개발 중인 기준 플랫폼으로 표현한다.
- 교육/컨설팅과 임베디드 제품 PoC는 바로 제공 가능 범위로 표현한다.
- 모듈이나 키트가 완성 판매 상태인 것처럼 단정하지 않는다.
- 기술 신뢰성은 산출물과 검증 흐름으로 보여준다.

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
