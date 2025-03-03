API 엔드포인트
=============

Finance Manager API의 상세 엔드포인트 문서입니다.

사용자 관리
---------

회원가입
~~~~~~~

.. http:post:: /api/v1/auth/register/

   새로운 사용자를 등록합니다.

   **예제 요청**:

   .. sourcecode:: http

      POST /api/v1/auth/register/ HTTP/1.1
      Content-Type: application/json

      {
          "username": "testuser",
          "email": "test@example.com",
          "password": "securepassword123",
          "password_confirm": "securepassword123"
      }

   **예제 응답**:

   .. sourcecode:: http

      HTTP/1.1 201 Created
      Content-Type: application/json

      {
          "id": 1,
          "username": "testuser",
          "email": "test@example.com",
          "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
      }

   :reqheader Content-Type: application/json
   :statuscode 201: 사용자가 성공적으로 생성됨
   :statuscode 400: 잘못된 요청 (유효하지 않은 데이터)

로그인
~~~~~

.. http:post:: /api/v1/auth/login/

   사용자 로그인을 처리합니다.

   **예제 요청**:

   .. sourcecode:: http

      POST /api/v1/auth/login/ HTTP/1.1
      Content-Type: application/json

      {
          "username": "testuser",
          "password": "securepassword123"
      }

   **예제 응답**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
          "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
          "user": {
              "id": 1,
              "username": "testuser",
              "email": "test@example.com"
          }
      }

   :reqheader Content-Type: application/json
   :statuscode 200: 로그인 성공
   :statuscode 401: 인증 실패

거래 관리
--------

거래 목록 조회
~~~~~~~~~~~

.. http:get:: /api/v1/transactions/

   사용자의 거래 내역을 조회합니다.

   **예제 요청**:

   .. sourcecode:: http

      GET /api/v1/transactions/?category=food&date_from=2024-01-01 HTTP/1.1
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

   **예제 응답**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
          "count": 2,
          "next": null,
          "previous": null,
          "results": [
              {
                  "id": 1,
                  "date": "2024-03-03",
                  "amount": "50000.00",
                  "type": "income",
                  "category": "salary",
                  "description": "월급"
              },
              {
                  "id": 2,
                  "date": "2024-03-03",
                  "amount": "-30000.00",
                  "type": "expense",
                  "category": "food",
                  "description": "식비"
              }
          ]
      }

   :query category: 거래 카테고리
   :query date_from: 시작 날짜 (YYYY-MM-DD)
   :query date_to: 종료 날짜 (YYYY-MM-DD)
   :query type: 거래 유형 (income/expense)
   :reqheader Authorization: Bearer <token>
   :statuscode 200: 성공
   :statuscode 401: 인증 실패

새 거래 등록
~~~~~~~~~~

.. http:post:: /api/v1/transactions/

   새로운 거래를 등록합니다.

   **예제 요청**:

   .. sourcecode:: http

      POST /api/v1/transactions/ HTTP/1.1
      Content-Type: application/json
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

      {
          "date": "2024-03-03",
          "amount": "50000.00",
          "type": "income",
          "category": "salary",
          "description": "월급"
      }

   **예제 응답**:

   .. sourcecode:: http

      HTTP/1.1 201 Created
      Content-Type: application/json

      {
          "id": 1,
          "date": "2024-03-03",
          "amount": "50000.00",
          "type": "income",
          "category": "salary",
          "description": "월급"
      }

   :reqheader Authorization: Bearer <token>
   :reqheader Content-Type: application/json
   :statuscode 201: 거래가 성공적으로 생성됨
   :statuscode 400: 잘못된 요청 (유효하지 않은 데이터)

자산 관리
--------

자산 현황 조회
~~~~~~~~~~~

.. http:get:: /api/v1/assets/summary/

   사용자의 전체 자산 현황을 조회합니다.

   **예제 응답**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
          "total_assets": "1000000.00",
          "total_liabilities": "300000.00",
          "net_worth": "700000.00",
          "assets_by_category": {
              "cash": "200000.00",
              "savings": "500000.00",
              "investments": "300000.00"
          }
      }

   :reqheader Authorization: Bearer <token>
   :statuscode 200: 성공
   :statuscode 401: 인증 실패

계좌 관리
--------

계좌 목록 조회
~~~~~~~~~~~

.. http:get:: /api/v1/accounts/

   사용자의 계좌 목록을 조회합니다.

   **예제 응답**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
          "count": 2,
          "results": [
              {
                  "id": 1,
                  "name": "주거래 계좌",
                  "type": "bank",
                  "balance": "500000.00",
                  "currency": "KRW"
              },
              {
                  "id": 2,
                  "name": "투자 계좌",
                  "type": "investment",
                  "balance": "1000000.00",
                  "currency": "KRW"
              }
          ]
      }

   :reqheader Authorization: Bearer <token>
   :statuscode 200: 성공
   :statuscode 401: 인증 실패

새 계좌 등록
~~~~~~~~~~

.. http:post:: /api/v1/accounts/

   새로운 계좌를 등록합니다.

   **예제 요청**:

   .. sourcecode:: http

      POST /api/v1/accounts/ HTTP/1.1
      Content-Type: application/json
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

      {
          "name": "새 계좌",
          "type": "bank",
          "balance": "0.00",
          "currency": "KRW"
      }

   **예제 응답**:

   .. sourcecode:: http

      HTTP/1.1 201 Created
      Content-Type: application/json

      {
          "id": 3,
          "name": "새 계좌",
          "type": "bank",
          "balance": "0.00",
          "currency": "KRW"
      }

   :reqheader Authorization: Bearer <token>
   :reqheader Content-Type: application/json
   :statuscode 201: 계좌가 성공적으로 생성됨
   :statuscode 400: 잘못된 요청 (유효하지 않은 데이터)

예산 관리
--------

예산 설정
~~~~~~~

.. http:post:: /api/v1/budgets/

   새로운 예산을 설정합니다.

   **예제 요청**:

   .. sourcecode:: http

      POST /api/v1/budgets/ HTTP/1.1
      Content-Type: application/json
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

      {
          "category": "food",
          "amount": "300000.00",
          "period": "monthly",
          "start_date": "2024-03-01"
      }

   **예제 응답**:

   .. sourcecode:: http

      HTTP/1.1 201 Created
      Content-Type: application/json

      {
          "id": 1,
          "category": "food",
          "amount": "300000.00",
          "period": "monthly",
          "start_date": "2024-03-01",
          "end_date": "2024-03-31"
      }

   :reqheader Authorization: Bearer <token>
   :reqheader Content-Type: application/json
   :statuscode 201: 예산이 성공적으로 생성됨
   :statuscode 400: 잘못된 요청 (유효하지 않은 데이터) 