# ARTEL 플러그인

Codex와 Claude Code에서 `artel-skills`와 `artel-macro-mcp`를 함께 설치합니다.
MCP는 `https://stage-mcp.artel.kr/mcp`에 연결하며 ARTEL 스테이징 계정으로 로그인합니다.

## Codex 설치

```sh
codex plugin marketplace add project-artel/artel-plugins
```

데스크톱 앱을 다시 열고 **Plugins**에서 **ARTEL** marketplace의 **ARTEL** 플러그인을 설치합니다.
MCP 연결 화면에서 ARTEL 계정으로 로그인합니다. 터미널에서는 `codex mcp list`에 표시되는 서버 이름을 `codex mcp login <server-name>`에 넘겨 로그인할 수 있습니다.

## Claude Code 설치

```sh
claude plugin marketplace add project-artel/artel-plugins
claude plugin install artel@artel-plugins
```

Claude Code를 열고 `/mcp`에서 `plugin:artel:artel-macro`를 선택해 로그인합니다.
`/artel:artel-test-cases`로 테스트 케이스 작성 스킬을 호출할 수 있습니다.

## MCP 연결 확인

에이전트에 ARTEL MCP의 `list_projects`를 호출해 달라고 요청합니다. 로그인한 계정의 스테이징 프로젝트가 표시되면 연결을 확인할 수 있습니다.
테스트 케이스를 작성할 때는 대상 프로젝트와 빌드를 지정하고 `artel-test-cases` 스킬을 사용합니다.
번들에 포함된 `artel-mcp` 스킬은 로컬 프로토타입 설정을 다루며, 플러그인이 연결하는 원격 서버는 `artel-macro`입니다.

## 스킬 원본과 업데이트

`plugins/artel/skills/`에는 [`project-artel/artel-skills`의 `1d410fd`](https://github.com/project-artel/artel-skills/tree/1d410fdebf313d73ea816aa992feefdf3a290e18) 스킬 7개와 참조 파일을 함께 담았습니다.
스킬을 수정할 때는 원본 저장소에서 먼저 반영하고, 배포할 revision의 `skills/`와 `LICENSE`를 이 저장소에 동기화합니다. 이 문서의 revision과 두 manifest의 버전도 함께 갱신합니다.
