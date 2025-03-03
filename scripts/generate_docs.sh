#!/bin/bash

# API 스키마 생성
echo "Generating API schema..."
python manage.py spectacular --file docs/api/schema.yml

# Python 모듈 문서 생성
echo "Generating Python module documentation..."
cd docs
sphinx-apidoc -f -o api ../finance
sphinx-apidoc -f -o api ../money

# HTML 문서 생성
echo "Building HTML documentation..."
make html

echo "Documentation generation complete. Check docs/_build/html/index.html"
