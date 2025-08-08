# Finance Manager

금융 자산 관리를 위한 웹 애플리케이션

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## 🚀 주요 기능

- 사용자 자산 관리
- 금융 거래 추적
- 자산 분석 및 리포트
- 예산 계획 및 관리

## 🛠 기술 스택

- **Backend**: Django, Python
- **Database**: PostgreSQL
- **Task Queue**: Celery
- **Frontend**: Django Templates, JavaScript
- **Testing**: pytest
- **CI/CD**: Azure Pipelines

## 📋 요구사항

- Python 3.8+
- PostgreSQL
- Redis (Celery용)

## 🔧 설치 방법

1. 저장소 클론:
```bash
git clone [repository-url]
cd finance
```

2. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 의존성 설치:
```bash
pip install -r requirements/local.txt
```

4. 환경 변수 설정:
```bash
cp .env.example .env
```

5. 데이터베이스 마이그레이션:
```bash
python manage.py migrate
```

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy finance

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

``` bash
cd finance
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

``` bash
cd finance
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

``` bash
cd finance
celery -A config.celery_app worker -B -l info
```

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

## 📚 API 문서

API 문서는 `/api/docs/` 에서 확인할 수 있습니다.

---

## GraphQL 스키마(SDL) 내보내기

Docker 컨테이너에서 Django 설정과 동일한 환경으로 Strawberry 스키마를 내보내려면 아래 절차를 따릅니다.

1) 컨테이너 내부에서 스키마 출력 파일 생성

```bash
docker compose -f local.yml exec django bash -lc "source /entrypoint && python -c \"import django, os; os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings.base'); django.setup(); from money.schema import schema; print(schema.as_str())\" > schema.graphql"
```

2) 생성된 파일을 호스트로 복사

```bash
docker cp <django_container_id_or_name>:/app/schema.graphql ./schema.graphql
```

- 참고: 컨테이너 ID/이름은 `docker ps`로 확인할 수 있습니다. 예: `docker cp 8faa11e00797:/app/schema.graphql .`
- 결과물 `schema.graphql`은 `backend/` 루트에 위치하게 됩니다.

3) 프론트엔드 코드젠 실행(선택)

```bash
cd ../frontend
npm run codegen
```

- 프론트엔드 `codegen.js`에서 라이브 엔드포인트를 사용하는 설정으로도 코드젠을 수행할 수 있습니다. 인증이 필요한 경우 `GRAPHQL_AUTHORIZATION`/`GRAPHQL_COOKIE`/`GRAPHQL_CSRF_TOKEN` 환경변수를 설정하세요.
