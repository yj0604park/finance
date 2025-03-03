개발자 기여 가이드
==============

Finance Manager 프로젝트에 기여하는 방법을 설명합니다.

개발 환경 설정
-----------

1. 필수 요구사항
   
   - Python 3.8+
   - Docker 및 Docker Compose
   - Git
   - PostgreSQL 13+
   - Redis 6+

2. 로컬 개발 환경 설정

   .. code-block:: bash

      # 저장소 클론
      git clone https://github.com/your-username/finance.git
      cd finance

      # 가상환경 생성 및 활성화
      python -m venv venv
      source venv/bin/activate  # Windows: venv\Scripts\activate

      # 의존성 설치
      pip install -r requirements/local.txt

      # 환경 변수 설정
      cp .env.example .env

      # 데이터베이스 마이그레이션
      python manage.py migrate

      # 개발 서버 실행
      python manage.py runserver

코드 작성 가이드
------------

1. 코드 스타일
   
   - Black 코드 포맷터 사용
   - isort로 import 정렬
   - flake8 린터 규칙 준수
   - mypy 타입 체크 통과

2. 문서화
   
   - 모든 함수/클래스에 docstring 작성
   - 복잡한 로직은 인라인 주석 추가
   - README 및 문서 업데이트

3. 테스트
   
   - 단위 테스트 필수
   - 통합 테스트 권장
   - 최소 80% 코드 커버리지 유지

Git 워크플로우
-----------

1. 브랜치 전략
   
   - main: 프로덕션 코드
   - develop: 개발 브랜치
   - feature/*: 새로운 기능
   - bugfix/*: 버그 수정
   - hotfix/*: 긴급 수정

2. 커밋 메시지
   
   .. code-block::

      feat: 새로운 기능 추가
      fix: 버그 수정
      docs: 문서 수정
      style: 코드 포맷팅
      refactor: 코드 리팩토링
      test: 테스트 코드
      chore: 기타 변경사항

3. PR(Pull Request) 가이드
   
   - PR 템플릿 사용
   - 리뷰어 최소 1명 이상
   - CI 테스트 통과 필수
   - 충돌 해결 후 PR 제출

테스트 작성 가이드
-------------

1. 단위 테스트
   
   .. code-block:: python

      def test_transaction_creation():
          """거래 생성 테스트"""
          transaction = Transaction.objects.create(
              amount=1000,
              category="income",
              description="test"
          )
          assert transaction.amount == 1000
          assert transaction.category == "income"

2. 통합 테스트
   
   .. code-block:: python

      class TestTransactionAPI(APITestCase):
          def test_transaction_list_api():
              """거래 목록 API 테스트"""
              url = reverse("api:transaction-list")
              response = self.client.get(url)
              assert response.status_code == 200

3. 성능 테스트
   
   - 로컬에서 기본 성능 테스트
   - 프로덕션 환경 시뮬레이션
   - 부하 테스트 시나리오

보안 가이드
--------

1. 일반 보안
   
   - 비밀번호 해싱 필수
   - HTTPS 사용
   - CSRF 토큰 확인
   - XSS 방지

2. API 보안
   
   - 토큰 기반 인증
   - 요청 제한 설정
   - 입력값 검증
   - CORS 설정

3. 데이터 보안
   
   - 민감 정보 암호화
   - 접근 권한 확인
   - 로깅 및 모니터링

배포 프로세스
----------

1. 배포 전 체크리스트
   
   - 모든 테스트 통과
   - 코드 리뷰 완료
   - 문서 업데이트
   - 마이그레이션 확인

2. 배포 단계
   
   .. code-block:: bash

      # 1. 코드 병합
      git checkout main
      git merge develop

      # 2. 태그 생성
      git tag -a v1.0.0 -m "version 1.0.0"

      # 3. 배포
      docker-compose -f production.yml up -d

      # 4. 마이그레이션
      docker-compose -f production.yml exec web python manage.py migrate

3. 롤백 절차
   
   - 이전 버전 태그로 복구
   - 데이터베이스 롤백
   - 모니터링 강화

문제 해결
-------

1. 일반적인 문제
   
   - 환경 변수 설정 확인
   - 캐시 초기화
   - 로그 확인
   - 데이터베이스 연결 확인

2. 디버깅 가이드
   
   - pdb 사용법
   - 로깅 레벨 설정
   - 성능 프로파일링
   - 메모리 누수 확인 