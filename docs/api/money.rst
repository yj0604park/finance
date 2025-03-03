money package
=============

Subpackages
-----------

.. toctree::
   :maxdepth: 4

   money.migrations
   money.view

Submodules
----------

money.admin module
------------------

.. automodule:: money.admin
   :members:
   :undoc-members:
   :show-inheritance:

money.apps module
-----------------

.. automodule:: money.apps
   :members:
   :undoc-members:
   :show-inheritance:

money.choices module
--------------------

.. automodule:: money.choices
   :members:
   :undoc-members:
   :show-inheritance:

money.forms module
------------------

.. automodule:: money.forms
   :members:
   :undoc-members:
   :show-inheritance:

money.helper module
-------------------

.. automodule:: money.helper
   :members:
   :undoc-members:
   :show-inheritance:

money.models module
-------------------

.. automodule:: money.models
   :members:
   :undoc-members:
   :show-inheritance:

money.tests module
------------------

.. automodule:: money.tests
   :members:
   :undoc-members:
   :show-inheritance:

money.urls module
-----------------

.. automodule:: money.urls
   :members:
   :undoc-members:
   :show-inheritance:

money.views module
------------------

.. automodule:: money.views
   :members:
   :undoc-members:
   :show-inheritance:

Module contents
---------------

.. automodule:: money
   :members:
   :undoc-members:
   :show-inheritance:

금융 API
========

금융 거래 및 자산 관리를 위한 API 엔드포인트들을 설명합니다.

거래 관리
--------

거래 목록 조회
~~~~~~~~~~~

.. http:get:: /api/v1/transactions/

    사용자의 거래 내역을 조회합니다.

    **예제 요청**:

    .. sourcecode:: http

        GET /api/v1/transactions/ HTTP/1.1
        Authorization: Bearer <your-token>

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
                    "amount": 50000,
                    "type": "income",
                    "category": "salary",
                    "description": "월급"
                },
                {
                    "id": 2,
                    "date": "2024-03-03",
                    "amount": -30000,
                    "type": "expense",
                    "category": "food",
                    "description": "식비"
                }
            ]
        }

    :query date_from: 시작 날짜 (YYYY-MM-DD)
    :query date_to: 종료 날짜 (YYYY-MM-DD)
    :query type: 거래 유형 (income/expense)
    :reqheader Authorization: Bearer <token>
    :statuscode 200: 성공
    :statuscode 401: 인증 실패

새 거래 등록
~~~~~~~~~

.. http:post:: /api/v1/transactions/

    새로운 거래를 등록합니다.

    **예제 요청**:

    .. sourcecode:: http

        POST /api/v1/transactions/ HTTP/1.1
        Content-Type: application/json
        Authorization: Bearer <your-token>

        {
            "date": "2024-03-03",
            "amount": 50000,
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
            "amount": 50000,
            "type": "income",
            "category": "salary",
            "description": "월급"
        }

    :reqheader Authorization: Bearer <token>
    :reqheader Content-Type: application/json
    :statuscode 201: 거래가 성공적으로 생성됨
    :statuscode 400: 잘못된 요청 (유효하지 않은 데이터)

자산 현황
-------

.. http:get:: /api/v1/assets/summary/

    사용자의 전체 자산 현황을 조회합니다.

    **예제 응답**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "total_assets": 1000000,
            "total_liabilities": 300000,
            "net_worth": 700000,
            "assets_by_category": {
                "cash": 200000,
                "savings": 500000,
                "investments": 300000
            }
        }

    :reqheader Authorization: Bearer <token>
    :statuscode 200: 성공
    :statuscode 401: 인증 실패
