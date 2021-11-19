# 3기_도서관대출서비스_이재근

|  이름  |     이메일         |
| :---:  |    :---:           |
| 이재근 | ljkean14@gmail.com |

***

- [3기_도서관대출서비스_이재근](#3기_도서관대출서비스_이재근)
  - [프로젝트 구성](#프로젝트-구성)
    - [프로젝트 일정](#프로젝트-일정)
    - [프로젝트 필요 기능](#프로젝트-필요-기능)
    - [프로젝트 사용 기술](#프로젝트-사용-기술)
    - [파이썬 패키지 버전](#파이썬-패키지-버전)
  - [프로젝트 기능 설명](#프로젝트-기능-설명)
  - [프로젝트 구성도](#프로젝트-구성도)
  - [프로젝트 팀원 역활](#프로젝트-팀원-역활)
  - [프로젝트 버전](#프로젝트-버전)

***

## 프로젝트 구성

### 프로젝트 일정

| 일정 | 11/15(월)| 11/16(화) | 11/17(수) | 11/18(목) | 11/19(금) | 11/20(토) | 11/21(일) |
| :---:|   :---:  |   :---:   |   :---:   |   :---:   |   :---:   |   :---:   |   :---:   |
| 1주차 |    -    |    OT     |   DB설계  |     -     |책 파일 입력|     -     | 로그인 환경 구성|

| 일정 | 11/15(월)| 11/16(화) |  11/17(수) | 11/18(목) | 11/19(금) | 11/20(토) | 11/21(일) |
| :---:|   :---:  |   :---:   |   :---:   |   :---:   |   :---:   |   :---:   |   :---:   |
| 2주차 |메인페이지|대여, 반납, 책정보|나머지 기능|부스트랩 디자인|서버 환경 구성| 배포 에러 확인| 발표 |

### 프로젝트 필요 기능

- 해야할 기능

***

- 로그인
- 회원가입
- 로그아웃
- 메인 페이지
- 대여하기
- 반납하기
- 대여기록
  - 없을경우, 있을경우 다르게 출력
- 책 소개

***

### 프로젝트 사용 기술

- Flask
- Mysql
- Jinja2

***

### 파이썬 패키지 버전

> python.3.8\
> certifi            2021.10.8\
> charset-normalizer 2.0.7\
> click              8.0.3\
> colorama           0.4.4\
> Flask              2.0.2\
> Flask-SQLAlchemy   2.5.1\
> greenlet           1.1.2\
> idna               3.3\
> itsdangerous       2.0.1\
> Jinja2             3.0.3\
> MarkupSafe         2.0.1\
> pip                19.2.3\
> requests           2.26.0\
> setuptools         41.2.0\
> SQLAlchemy         1.4.27\
> urllib3            1.26.7\
> Werkzeug           2.0.2

***

## 프로젝트 기능 설명

- 아직 아무 기능 없음

***

## 프로젝트 구성도

- 프로젝트

![001](image/프로젝트%20구조.png)

- DB

![002](image/DB구조.png)

***

## 프로젝트 팀원 역활

- 팀장 : 이재근
  - DB 관리 : 이재근
  - 로그인 세션 관리 : 이재근
  - 프론트앤드 관리 : 이재근
  - 데이터 관리 : 이재근

***

## 프로젝트 버전

- 0.0.01
  - DB models 구성
    - User, Book, Book_stock, Book_rental, Book_evaluation

***

- 0.0.02
  - local 환경에 DB 설치
![003](image/DB모델.png)
  - mysql key 외부 파일에서 읽어오는 형식으로 노출 제거
  - 메인 페이지, 로그인, 로그아웃 프로토타입 설계

***

- 0.0.03
  - flask app 형식이 아닌 flask factory 형식으로 구조 변경
    - 수많은 from . import  에러 발생
    - blueprint 위치 변경으로 인한 참조 변경
    - html 에서의 url_for 수정해야하는점 파악
  - DB 수정
    - 외부키 전부 개인키로 바꾸기
    - 구조 변화로 인한 error 처리
      - `During handling of the above exception, another exception occurred:`
      - `RuntimeError: No application found. Either work inside a view function or push an application context. See http://flask-sqlalchemy.pocoo.org/contexts/.`
        - flask-sqlalchemy 해결방법을 참고하여 해결
  - 디버그 모드 추가하기
  - 프로젝트 일정 만들기
  - 문자열 NN 속성은 빈 문자열 넣는식으로 default값 넣기.
  - Wiki 탬플릿 만들기
