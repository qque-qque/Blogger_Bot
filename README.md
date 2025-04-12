# **Blogger 자동 포스트 작성기**

이 프로그램은 **Google Blogger API**를 사용하여 **자동으로 블로그 포스트**를 작성하는 Python 스크립트입니다. `input.txt` 파일에서 제목과 내용을 읽어들여, 해당 내용을 Blogger 블로그에 포스트로 작성합니다.

---

## **필요한 라이브러리 및 설정**

### 1. **필요한 라이브러리 설치**

먼저, 필요한 Python 라이브러리들을 설치합니다. `requirements.txt` 파일을 이용하여 한번에 설치할 수 있습니다.

```txt
google-api-python-client==2.23.0
google-auth-httplib2==0.1.0
google-auth-oauthlib==0.4.6
python-dotenv==0.21.0
requests==2.26.0
```

또는 pip를 사용하여 직접 설치할 수 있습니다.

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib python-dotenv requests
```

### 2. **API 설정 및 인증 정보**

#### Google API 콘솔에서 설정:

- Google Developer Console에서 새 프로젝트를 생성합니다.
- Blogger API를 활성화합니다.
- OAuth 2.0 클라이언트 ID를 생성하고, 생성된 `client_secret.json` 파일을 다운로드합니다.
- 다운로드한 `client_secret.json` 파일을 프로젝트 폴더에 저장합니다.

#### 환경 변수 설정:

- `.env` 파일을 프로젝트 루트 디렉토리에 생성합니다.
- `.env` 파일에 `CLIENT_SECRET_FILE`과 `BLOG_ID`를 설정합니다.

```env
CLIENT_SECRET_FILE=client_secret.json
BLOG_ID=your_blog_id_here
```

`CLIENT_SECRET_FILE`은 다운로드한 `client_secret.json`의 파일 이름입니다.
`BLOG_ID`는 Blogger 대시보드에서 블로그의 ID를 확인할 수 있습니다.

### 파일 구조

```plaintext
project-folder/
│
├── client_secret.json  # OAuth 인증을 위한 클라이언트 시크릿 파일
├── input.txt           # 작성할 포스트의 제목과 내용이 담긴 파일
├── requirements.txt     # 필요한 라이브러리 리스트
├── .env                # 환경 변수 파일 (CLIENT_SECRET_FILE, BLOG_ID 설정)
└── token.pickle         # OAuth 인증 후 저장되는 인증 토큰 파일
└── src/
    └── main.py         # 블로그 포스트를 자동으로 작성하는 Python 스크립트
```

---

## **사용법**

### 1. **input.txt 파일 작성**

포스트에 사용할 제목과 내용을 `input.txt` 파일에 작성합니다. 파일의 첫 번째 줄은 포스트 제목, 나머지 줄들은 포스트의 내용이 됩니다.

예시: `input.txt`

```plaintext
오늘의 날씨는 맑고 따뜻해요!
오늘은 맑고 따뜻한 날씨가 계속될 예정입니다. 밖에 나가서 산책하기 좋은 날이네요.
```

### 2. **스크립트 실행**

터미널이나 커맨드 프롬프트를 열고, 프로젝트 폴더로 이동합니다.

아래 명령어를 실행하여 블로그에 포스트를 작성합니다.

```bash
python main.py
```

이 스크립트는 `input.txt` 파일에서 제목과 내용을 읽어 Blogger API를 사용하여 블로그에 새로운 포스트를 작성합니다.

---

## **기능 설명**

### 1. `get_credentials`

이 함수는 OAuth 인증을 관리합니다. 사용자가 처음 인증할 때는 웹 브라우저에서 인증을 거친 후 `token.pickle` 파일에 인증 정보를 저장합니다. 이후에는 이 파일을 사용하여 인증 과정을 자동화합니다.

### 2. `get_blogger_service`

이 함수는 인증을 받은 후, Blogger API의 서비스 객체를 반환합니다. 이 객체를 통해 블로그 포스트를 관리할 수 있습니다.

### 3. `create_blog_post`

이 함수는 제목과 내용을 인자로 받아 새로운 블로그 포스트를 작성합니다.

### 4. `read_input_from_file`

`input.txt` 파일에서 제목과 내용을 읽어옵니다. 첫 번째 줄은 제목, 그 이후의 줄은 내용으로 간주합니다.

### 5. `create_blog_post_from_file`

`read_input_from_file` 함수를 사용하여 제목과 내용을 읽고, `create_blog_post` 함수를 호출하여 블로그에 포스트를 작성합니다.

---

## **참고 사항**

- OAuth 인증은 처음 실행 시, 구글 계정을 통해 인증을 해야 합니다. 인증이 완료되면 `token.pickle` 파일에 인증 정보가 저장되며, 이후 인증 없이 사용할 수 있습니다.
- 이 스크립트는 `input.txt`에서 제목과 내용을 자동으로 읽어와 포스트를 작성합니다. 제목과 내용이 정확히 `input.txt` 파일에 맞게 작성되어야 합니다.

---

## **문제 해결**

### 1. `FileNotFoundError: input.txt` 오류

`input.txt` 파일이 존재하지 않으면 이 오류가 발생합니다. 파일을 작성하고 해당 디렉토리에 저장하세요.

### 2. 인증 오류

OAuth 인증 과정에서 문제가 발생하면, 인증을 다시 시도해 보세요. 인증 후 생성된 `token.pickle` 파일을 삭제하고 다시 실행하면 새로 인증을 받을 수 있습니다.
