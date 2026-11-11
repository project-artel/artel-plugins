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

## 스킬 원본과 업데이트

`plugins/artel/skills/`에는 [`project-artel/artel-skills`의 `e049073`](https://github.com/project-artel/artel-skills/tree/e049073ee6eb3bb878d60a191041a50f88c254c1) 기준 스킬 6개와 참조 파일을 담았습니다.
원본의 `artel-mcp` 스킬은 넣지 않습니다. 로컬 프로토타입(`artel-mcp-poc`)을 설치하는 안내라서, 플러그인이 연결하는 원격 서버 `artel-macro`와 관계가 없습니다. 그대로 넣으면 "MCP 셋팅" 같은 요청에 이 스킬이 먼저 쓰여 로컬 프로토타입을 설치하려 듭니다.
스킬 번들을 갱신할 때 이 문서의 기준 커밋과 두 manifest의 버전을 함께 갱신하고, `artel-mcp`는 계속 뺍니다.
