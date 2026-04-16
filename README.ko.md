# SiliconFlow MCP 서버

[[English](README.md) | [한국어](README.ko.md)]

SiliconFlow의 이미지 생성 서비스를 위한 MCP(Model Context Protocol) 서버입니다. 이 서버를 통해 Claude와 같은 AI 모델이 SiliconFlow에서 제공하는 다양한 모델을 사용하여 고품질 이미지를 직접 생성할 수 있습니다.

## 주요 기능

- **`generate_image` 도구**: 텍스트 프롬프트를 기반으로 이미지를 생성합니다.
  - 다양한 모델 지원 (FLUX.1-schnell, FLUX.1-dev, FLUX.2-pro 등)
  - **`aspect_ratio` 지원**: 1:1, 16:9, 9:16 등의 화면비 선택 가능.
  - 지원 모델에 대해 `negative_prompt` 사용 가능.
  - 재현 가능한 생성을 위한 시드(Seed) 지원.
- **`generate_video` 도구**: 텍스트 프롬프트를 통해 동영상을 생성합니다 (완료될 때까지 자동 확인).
  - Wan-AI 모델 지원 및 다양한 화면비 선택 가능.
- **`submit_video_generation` & `get_video_status`**: 비동기 동영상 생성을 위한 수동 제어 도구.
- **`list_models` 도구**: SiliconFlow에서 사용 가능한 이미지 및 동영상 모델 목록을 실시간으로 가져옵니다.
- **`get_user_info` 도구**: 잔액(총액, 유료, 무료) 및 프로필 정보를 포함한 SiliconFlow 계정 상세 정보를 확인합니다.
- **로컬 저장 기능**: 생성된 `.png`, `.jpg`, `.mp4` 파일을 지정된 폴더에 자동으로 저장합니다.

## 설정 방법

### 1. 사전 요구 사항
- [uv](https://github.com/astral-sh/uv) 설치 권장 또는 Python 3.10 이상.
- SiliconFlow API 키. [SiliconFlow 대시보드](https://cloud.siliconflow.com/account/ak)에서 발급받으세요.

### 2. 환경 설정
서버 실행을 위해 API 키가 필요합니다. 환경 변수 또는 `.env` 파일을 통해 제공할 수 있습니다.

```bash
SILICONFLOW_API_KEY=your_api_key_here
# 선택 사항: 생성된 이미지/동영상을 저장할 로컬 경로
SILICONFLOW_IMAGE_DIR=C:/path/to/save/assets
```

## 사용 방법

### uvx 사용 (권장)
별도의 설치 없이 `uvx`를 통해 즉시 실행할 수 있습니다:

```bash
uvx siliconflow-mcp
```

### PyPI를 통한 설치
패키지를 전역 도구로 설치하여 사용할 수도 있습니다:

```bash
uv tool install siliconflow-mcp
# 또는 pip 사용
pip install siliconflow-mcp
```

### MCP 클라이언트 연동

#### Claude Desktop
Claude Desktop 설정 파일(`Windows: %APPDATA%\Claude\claude_desktop_config.json` 또는 `macOS: ~/Library/Application Support/Claude/claude_desktop_config.json`)에 다음 내용을 추가하세요:

```json
{
  "mcpServers": {
    "siliconflow": {
      "command": "uvx",
      "args": ["siliconflow-mcp"],
      "env": {
        "SILICONFLOW_API_KEY": "your_api_key_here",
        "SILICONFLOW_IMAGE_DIR": "C:/path/to/save/assets"
      }
    }
  }
}
```

#### Claude Code
다음 명령어를 실행하여 서버를 추가합니다:
```bash
claude mcp add siliconflow -- uvx siliconflow-mcp
```

#### Gemini CLI
`.gemini/settings.json` 파일에 다음 설정을 추가하세요:
```json
{
  "mcpServers": {
    "siliconflow": {
      "command": "uvx",
      "args": ["siliconflow-mcp"],
      "env": {
        "SILICONFLOW_API_KEY": "your_api_key_here",
        "SILICONFLOW_IMAGE_DIR": "C:/path/to/save/assets"
      }
    }
  }
}
```

## 개발자 가이드
직접 기여하거나 소스 코드에서 실행하려는 경우:

```bash
# 의존성 설치
uv sync

# 서버 로컬 실행
uv run siliconflow-mcp
```

## 지원 모델
- `black-forest-labs/FLUX.1-schnell` (빠르고 효율적)
- `black-forest-labs/FLUX.1-dev` (고품질)
- `black-forest-labs/FLUX.2-pro` (전문가급 품질)
- ...기타 SiliconFlow에서 호스팅하는 이미지 모델들.

## 라이선스
MIT
