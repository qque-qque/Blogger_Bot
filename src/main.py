import time
from datetime import datetime
import os
import pickle
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request  # 수정된 부분
from requests import Request as req  # 'requests' 라이브러리의 Request는 별칭으로 사용 가능

# .env 파일에서 환경 변수 로드
load_dotenv()

# OAuth 2.0 인증 스코프
SCOPES = ['https://www.googleapis.com/auth/blogger']

# 환경 변수에서 CLIENT_SECRET_FILE과 BLOG_ID 가져오기
CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')
BLOG_ID = os.getenv('BLOG_ID')

# 인증을 위한 함수
def get_credentials():
    creds = None
    # token.pickle 파일이 있는지 확인
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # 자격 증명이 없거나 유효하지 않으면 로그인
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # 'google.auth.transport.requests.Request' 사용
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)  # 로컬 서버에서 인증 진행

        # 인증 후 토큰을 저장하여 다음번에 재사용
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

# Blogger API 서비스 객체 가져오기
def get_blogger_service():
    creds = get_credentials()  # 인증 받은 자격 증명
    return build('blogger', 'v3', credentials=creds)

# 블로그 포스트 작성
def create_blog_post(blog_id, title, content):
    try:
        service = get_blogger_service()

        # 포스트 작성
        posts = service.posts()
        post = posts.insert(blogId=blog_id, body={
            'title': title,
            'content': content
        }).execute()

        print(f"블로그 글 작성 완료: {post['url']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

# 외부 파일에서 제목과 내용을 읽어오는 함수
def read_input_from_file():
    try:
        with open('input.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            title = lines[0].strip()  # 첫 번째 줄은 제목
            content = ''.join(lines[1:]).strip()  # 나머지 줄은 내용
            return title, content
    except FileNotFoundError:
        print("입력 파일(input.txt)을 찾을 수 없습니다.")
        return None, None

# 파일에서 읽은 제목과 내용을 사용하여 블로그 포스트 작성하기
def create_blog_post_from_file():
    # 외부 파일에서 제목과 내용 읽기
    title, content = read_input_from_file()

    if title and content:
        # 블로그 포스트 작성
        create_blog_post(BLOG_ID, title, content)
        print(f"'{title}' 관련 포스트가 블로그에 작성되었습니다.")
    else:
        print("제목과 내용을 읽어오지 못했습니다.")

def main():
    create_blog_post_from_file()

if __name__ == '__main__':
    main()
