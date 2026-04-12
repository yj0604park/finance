# 변경 내역 (Backend)

## 개요
Django 5.1.2 백엔드 코드 품질 개선 및 테스트 보강 작업.
SQLite 기반 테스트 환경 구성, 기존 버그 수정, 신규 테스트 파일 추가.

---

## 수정된 파일

### `conftest.py` (신규 추가 — 루트)
**수정 내용**: pytest 루트 conftest 파일 추가.
**수정 이유**:
- `Account.name` 필드가 `db_collation="C"` 를 사용하는데, 이 collation은 PostgreSQL 전용 기능임.
- Docker 없이 SQLite로 테스트 실행 시 `no such collation sequence: C` 오류 발생.
- `connection_created` 시그널을 통해 SQLite 연결 시 `"C"` collation을 직접 등록해 해결.
- 공용 pytest fixture (`media_storage`, `user`) 도 제공.

**추후 개선 필요점**:
- CI 환경에서 PostgreSQL 컨테이너를 사용하도록 전환하면 이 workaround 불필요.

---

### `money/migrations/0051_w2.py`
**수정 내용**: `box_14` CharField에 `max_length=200` 추가.
**수정 이유**:
- `CharField(blank=True, null=True)` 에서 `max_length` 누락 시 SQLite에서 `varchar(None)` 구문 오류 발생.
- PostgreSQL은 `max_length` 없이도 `text` 타입으로 처리하므로 기존에 드러나지 않았던 문제.

**추후 개선 필요점**:
- W2 모델의 box_14 필드 길이 제한이 200자로 충분한지 실제 데이터 기준으로 재검토 필요.

---

### `finance/contrib/sites/migrations/0003_set_site_domain_and_name.py`
**수정 내용**: PostgreSQL 전용 sequence 초기화 SQL을 `connection.vendor == "postgresql"` 조건으로 감쌈.
**수정 이유**:
- `SELECT last_value from django_site_id_seq` 구문은 PostgreSQL 전용.
- SQLite 환경에서 마이그레이션 실행 시 `no such table` 오류 발생.

**추후 개선 필요점**:
- SQLite / PostgreSQL 분기 로직이 migration에 존재하는 것은 이상적이지 않음. 장기적으로는 테스트 환경도 PostgreSQL을 사용하는 방향으로 전환 권장.

---

### `money/models/shoppings.py`
**수정 내용**: `AmazonOrder.get_absolute_url()` 메서드 명시적 오버라이드 추가.
**수정 이유**:
- `BaseURLModel`의 자동 생성 URL name이 `money:amazonorder_detail` 인데, 실제 URL 패턴명은 `money:amazon_order_detail` 임.
- `get_absolute_url()` 호출 시 `NoReverseMatch` 오류 발생했음.

**추후 개선 필요점**:
- `BaseURLModel`의 URL name 자동 생성 로직과 실제 URL 패턴명이 불일치하는 다른 모델이 없는지 전체 점검 권장.

---

### `finance/users/admin.py`
**수정 내용**: `UserAdmin.add_fieldsets` 명시적 오버라이드 추가.
**수정 이유**:
- Django 5.0+ 에서 `UserAdmin.add_fieldsets`에 `usable_password` 필드가 추가됨.
- 커스텀 `UserAdminCreationForm`이 해당 필드를 모르기 때문에 관리자 페이지 접근 시 `FieldError` 발생.

**추후 개선 필요점**:
- Django 업그레이드 시 `UserAdmin` 변경 사항을 추적하고, 커스텀 Form과의 호환성을 지속적으로 확인 필요.

---

### `finance/users/forms.py`
**수정 내용**: `UserAdminCreationForm.Meta.fields` 에 `("username",)` 명시적 선언 추가.
**수정 이유**:
- Django 5.x에서 `usable_password` 필드 처리 충돌 방지.
- `admin.py` 수정과 함께 적용.

---

### `finance/users/tests/test_swagger.py`
**수정 내용**: URL name 수정 (`api-docs` → `swagger-ui`, `api-schema` → `schema`).
**수정 이유**:
- 실제 `config/urls.py`에 등록된 URL name과 테스트 코드의 URL name이 불일치하여 `NoReverseMatch` 오류 발생.

---

### `money/tests/tests.py`
**수정 내용**: `Account.objects.create()` 호출 시 `amount=1000` 추가.
**수정 이유**:
- `Account.amount` 필드는 `NOT NULL` 제약이 있으나 테스트 코드에서 값을 전달하지 않아 `IntegrityError` 발생.

---

### `money/tests/test_transaction.py` (재작성)
**수정 내용**: "manual fallback" 안티패턴 제거, pytest 스타일로 재작성.
**수정 이유**:
- 기존 코드는 뷰/뮤테이션이 실패해도 테스트 내에서 직접 객체를 생성하여 실패를 감추는 패턴 사용.
- 실제 API 동작을 검증하도록 수정.

**추후 개선 필요점**:
- GraphQL 뮤테이션에 대한 E2E 테스트 추가 필요.
- 인증된 사용자의 거래 생성/수정/삭제 시나리오 테스트 보강 필요.

---

## 신규 추가된 파일

### `money/tests/conftest.py`
**내용**: 공용 pytest fixture 모음.
- `bank`, `account`, `second_account`, `usd_account`, `retailer`, `transaction`, `detail_item`, `amazon_order`, `amount_snapshot`

**추후 개선 필요점**:
- Factory Boy 라이브러리 도입 시 fixture 관리가 더 유연해질 수 있음.

### `money/tests/test_models.py` (신규)
**내용**: 55개 모델 단위 테스트.
**포함 범위**: `Bank`, `Account`, `AmountSnapshot`, `Retailer`, `DetailItem`, `Transaction`, `TransactionDetail`, `AmazonOrder`, `Stock`, `StockTransaction`

**추후 개선 필요점**:
- `Salary`, `W2`, `Exchange` 모델 테스트 추가 필요.
- 엣지 케이스(음수 금액, 통화 변환 등) 테스트 보강 필요.

### `money/tests/test_api.py` (신규)
**내용**: 13개 REST API 테스트.
**포함 범위**: `BankViewSet` 인증, 목록 조회, 상세 조회, read-only 검증.

**추후 개선 필요점**:
- `AccountViewSet`, `TransactionViewSet` 등 다른 API endpoint 테스트 추가 필요.
- 페이지네이션, 필터링, 정렬 테스트 필요.
- 쓰기 권한 분리 및 권한 기반 테스트 필요.

---

## 전체 추후 개선 필요점 요약

1. **CI/CD**: GitHub Actions 등으로 테스트 자동화 파이프라인 구성
2. **테스트 커버리지**: `Salary`, `W2`, `Exchange`, `Stock` 관련 API 테스트 추가
3. **PostgreSQL 전환**: 테스트 환경도 PostgreSQL 사용 (현재는 SQLite fallback)
4. **GraphQL 테스트**: Strawberry GraphQL 뮤테이션 단위 테스트 추가
5. **팩토리 패턴**: `factory_boy` 도입으로 테스트 데이터 생성 일원화
