import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
def api_login_view(request):
    """JSON 로그인: {username, password} → session cookie 발급"""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "올바른 JSON 형식이 아닙니다."}, status=400)

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return JsonResponse({"error": "아이디와 비밀번호를 입력하세요."}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"username": user.username, "authenticated": True})

    return JsonResponse(
        {"error": "아이디 또는 비밀번호가 올바르지 않습니다."}, status=401
    )


@require_http_methods(["POST", "GET"])
def api_logout_view(request):
    """로그아웃: session 파기"""
    logout(request)
    return JsonResponse({"authenticated": False})


@require_http_methods(["GET"])
def api_me_view(request):
    """현재 인증 상태 및 사용자 정보 반환"""
    if request.user.is_authenticated:
        return JsonResponse({"username": request.user.username, "authenticated": True})
    return JsonResponse({"authenticated": False}, status=401)
