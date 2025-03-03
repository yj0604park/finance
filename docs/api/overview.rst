API 개요
=======

Finance Manager API에 대한 전반적인 설명입니다.

인증
----

모든 API 요청은 다음 중 하나의 인증 방식을 사용해야 합니다:

1. JWT 토큰
   
   .. code-block:: http

      GET /api/v1/accounts HTTP/1.1
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

2. 세션 인증
   
   웹 브라우저를 통한 요청은 세션 기반 인증을 사용합니다.

3. API 키
   
   서버 간 통신을 위한 API 키 인증:

   .. code-block:: http

      GET /api/v1/accounts HTTP/1.1
      X-API-Key: your-api-key

에러 처리
--------

1. 일반적인 에러 코드

   - 400: 잘못된 요청
   - 401: 인증 실패
   - 403: 권한 없음
   - 404: 리소스 없음
   - 500: 서버 에러

2. 에러 응답 형식

   .. code-block:: json

      {
          "error": {
              "code": "ERROR_CODE",
              "message": "사용자가 읽을 수 있는 에러 메시지",
              "details": {
                  "field": ["구체적인 에러 내용"]
              }
          }
      }

API 버전 관리
-----------

1. URL 기반 버전 관리
   
   - /api/v1/: 현재 안정 버전
   - /api/v2/: 베타 버전 (있는 경우)

2. 버전 지원 정책
   
   - 각 버전은 최소 12개월 지원
   - 버전 폐기 전 3개월 전 공지

요청 제한
--------

1. 속도 제한
   
   - 인증된 사용자: 분당 100 요청
   - 비인증 사용자: 분당 10 요청

2. 헤더 정보

   .. code-block:: http

      X-RateLimit-Limit: 100
      X-RateLimit-Remaining: 95
      X-RateLimit-Reset: 1640995200

데이터 형식
---------

1. 요청 데이터
   
   - Content-Type: application/json
   - UTF-8 인코딩 필수

2. 응답 데이터
   
   - JSON 형식
   - 날짜/시간: ISO 8601 형식
   - 금액: 문자열 형식 (정확도 유지)

페이지네이션
----------

1. 기본 구조

   .. code-block:: json

      {
          "count": 100,
          "next": "https://api.example.com/items?page=3",
          "previous": "https://api.example.com/items?page=1",
          "results": []
      }

2. 커서 기반 페이지네이션

   특정 API에서 사용 (예: 거래 내역):

   .. code-block:: http

      GET /api/v1/transactions?cursor=dXNlcjE=

필터링과 정렬
-----------

1. 필터링
   
   .. code-block:: http

      GET /api/v1/transactions?category=food&date_from=2024-01-01

2. 정렬
   
   .. code-block:: http

      GET /api/v1/transactions?sort=-date,amount

캐싱
----

1. ETag 지원
   
   .. code-block:: http

      ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
      If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"

2. 캐시 정책
   
   - GET 요청: 5분
   - LIST 요청: 1분
   - 사용자별 데이터: 캐시하지 않음

CORS
----

1. 허용된 오리진
   
   - localhost 개발 서버
   - 등록된 프로덕션 도메인

2. 허용된 메서드
   
   - GET
   - POST
   - PUT
   - DELETE
   - OPTIONS (프리플라이트) 