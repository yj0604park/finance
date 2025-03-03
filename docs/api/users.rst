사용자 API
=========

사용자 관리를 위한 API 엔드포인트들을 설명합니다.

인증
----

모든 API 요청은 JWT 토큰을 통한 인증이 필요합니다.

.. code-block:: bash

    Authorization: Bearer <your-token>

엔드포인트
---------

사용자 등록
~~~~~~~~~~

.. http:post:: /api/v1/users/

    새로운 사용자를 등록합니다.

    **예제 요청**:

    .. sourcecode:: http

        POST /api/v1/users/ HTTP/1.1
        Content-Type: application/json

        {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123"
        }

    **예제 응답**:

    .. sourcecode:: http

        HTTP/1.1 201 Created
        Content-Type: application/json

        {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com"
        }

    :reqheader Content-Type: application/json
    :statuscode 201: 사용자가 성공적으로 생성됨
    :statuscode 400: 잘못된 요청 (유효하지 않은 데이터)

사용자 정보 조회
~~~~~~~~~~~~~

.. http:get:: /api/v1/users/(int:user_id)/

    특정 사용자의 정보를 조회합니다.

    **예제 응답**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "name": "Test User",
            "date_joined": "2024-03-03T12:00:00Z"
        }

    :reqheader Authorization: Bearer <token>
    :statuscode 200: 성공
    :statuscode 404: 사용자를 찾을 수 없음

오류 응답
--------

.. http:any:: /api/*

    **인증 오류**:

    .. sourcecode:: http

        HTTP/1.1 401 Unauthorized
        Content-Type: application/json

        {
            "detail": "인증 자격 증명이 제공되지 않았습니다."
        }

    **권한 오류**:

    .. sourcecode:: http

        HTTP/1.1 403 Forbidden
        Content-Type: application/json

        {
            "detail": "이 작업을 수행할 권한이 없습니다."
        } 