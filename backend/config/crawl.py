import requests
from bs4 import BeautifulSoup
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import json
import base64

# RSA 암호화 함수
def encrypt_with_public_key(public_key_str, data):
    """
    공개키로 데이터를 암호화하고 Base64로 인코딩된 결과를 반환합니다.
    """
    # PEM 형식의 공개키 로드
    
    public_key = serialization.load_pem_public_key(public_key_str.encode())
    # RSA 암호화
    encrypted = public_key.encrypt(
        data.encode('utf-8'),  # 데이터를 UTF-8로 인코딩
        padding.PKCS1v15()  # JSEncrypt와 동일한 PKCS#1 v1.5 패딩 사용
    )
    
    # Base64로 암호화된 값을 인코딩하여 반환 (JSEncrypt와 동일한 방식)
    encrypted_base64 = base64.b64encode(encrypted).decode('utf-8')
    return encrypted_base64

# 로그인 함수
def login_to_school(login_id, login_pwd, store_id_yn='N'):
    # 1. 입력값 확인
    if not login_id:
        print("ID를 입력하세요")
        return
    if not login_pwd:
        print("비밀번호를 입력하세요")
        return

    # 2. Step 1: 서버로부터 공개키 가져오기
    public_key_url = "https://klas.kw.ac.kr/usr/cmn/login/LoginSecurity.do"
    response = requests.post(public_key_url)
    if response.status_code != 200:
        print("공개키를 가져오는 데 실패했습니다.")
        return
    
    public_key = response.json().get("publicKey")
    if not public_key:
        print("공개키가 응답에 포함되지 않았습니다.")
        return
    formatted_public_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"

    # 3. RSA 암호화로 로그인 정보 생성
    login_data = json.dumps({
        "loginId": login_id,
        "loginPwd": login_pwd,
        "storeIdYn": store_id_yn,
    })
    try:
        login_token = encrypt_with_public_key(formatted_public_key, login_data)
    except Exception as e:
        print(f"로그인 토큰 생성 실패: {e}")
        return
    
    # 4. Step 2: 서버로 로그인 요청 보내기
    login_url = "https://klas.kw.ac.kr/usr/cmn/login/LoginConfirm.do"
    payload = {
        "loginToken": login_token,  # RSA 암호화된 데이터를 전송
        "redirectUrl": "",
        "redirectTabUrl": "",
    }
    headers = {
        "Content-Type": "application/json",
        "x-requested-with": "XMLHttpRequest"
    }

    login_response = requests.post(login_url, data=json.dumps(payload), headers=headers)
    if login_response.status_code != 200:
        print(login_response.text)
        print("로그인 요청 실패")
        return

    res = login_response.json()
    
    # 5. 서버 응답 처리
    if res.get("errorCount") == 0:
        response_data = res.get("response")
        if response_data.get("certOpt") == "Y":
            print("임시 비밀번호를 먼저 변경해주세요.")
        elif response_data.get("gradAt") == "Y":
            print("졸업생은 KLAS 종합정보서비스를 이용할 수 없습니다.")
        else:
            print("로그인 성공!")
            print("리다이렉트 URL:", res.get("redirectUrl"))
    else:
        print("로그인 실패:", res.get("errorMessage"))
