# 의료급여 지원업무 조회 및 집계

`web/index.html`은 정적 웹페이지입니다. 접속하면 `web/data.js`에 포함된 조회용 업무 기록 800건과 기관 현황 550건을 바로 표시합니다. 원본 CSV 전체 열은 게시하지 않았습니다.

`solution.py`는 Python 표준 라이브러리만 사용합니다. 원본 CSV 두 개를 `upload/` 폴더에 넣고 `python solution.py`를 실행하거나 `--work`, `--org`, `--output`으로 경로를 지정합니다.

Netlify에서는 이 GitHub 저장소를 연결하세요. 저장소 루트의 `netlify.toml`이 게시 디렉터리를 `web`으로 설정합니다.
