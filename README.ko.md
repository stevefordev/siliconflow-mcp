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
- **로컬 저장 기능**: 생성된 `.png`, `.jpg`, `.mp4` 파일을 지정된 폴더에 자동으로 저장합니다.

## 설정 방법

### 1. 사전 요구 사항
- [uv](https://github.com/astral-sh/uv) 설치 권장.
- SiliconFlow API 키. [SiliconFlow 대시보드](https://cloud.siliconflow.com/account/ak)에서 발급받으세요.

### 2. 환경 설정
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 본인의 API 키를 입력합니다 (`.env.example` 파일을 복사하여 사용할 수 있습니다):
```bash
SILICONFLOW_API_KEY=your_api_key_here
# 선택 사항: 생성된 이미지를 저장할 로컬 경로
SILICONFLOW_IMAGE_DIR=C:/path/to/save/images
```

### 3. Claude Desktop 연동
Claude Desktop 설정 파일(`Windows: %APPDATA%\Claude\claude_desktop_config.json`)에 다음 내용을 추가하세요:

```json
{
  "mcpServers": {
    "siliconflow": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/path/to/siliconflow-mcp",
        "run",
        "siliconflow-mcp"
      ]
    }
  }
}
```
*참고: `C:/path/to/siliconflow-mcp`를 실제 이 프로젝트가 설치된 절대 경로로 변경하세요.*

## 개발자 가이드

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
