from rest_framework import generics, viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import RegisterSerializer, BusinessSerializer
from .models import Business, BusinessMember
from authentication.permissions import IsBusinessAdmin
from django.views.generic import TemplateView

class RegisterTemplateView(TemplateView):
    template_name = 'authentication/register.html'
class LoginTemplateView(TemplateView):
    template_name = 'authentication/login.html'

# JWT를 쿠키에 넣는 커스텀 로그인 뷰
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # 기본 JWT 발급 로직 실행
        response = super().post(request, *args, **kwargs)
        data = response.data
        access_token = data.pop('access', None)  # JWT 토큰을 응답 본문에서 제거
        refresh_token = data.pop('refresh', None)

    # JWT가 존재하는 경우(로그인 성공)
        response = Response({'message': 'Login successful'}, status=response.status_code)
        if access_token:
            response.set_cookie(
                'access_token',
                access_token,
                httponly=True,   # JavaScript에서 접근 불가 (보안 강화)
                secure=True,     # HTTPS에서만 전송 (개발 환경에서는 False 가능)
                samesite='Lax'   # CSRF 방지
            )
        if refresh_token:
            response.set_cookie(
                'refresh_token',
                refresh_token,
                httponly=True,
                secure=True,
                samesite='Lax'
            )
        return response


# JWT Refresh 토큰도 쿠키로 설정
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  # 기본 토큰 갱신 로직 실행
        data = response.data
        access_token = data.pop('access', None)

        # 쿠키에 갱신된 Access 토큰 설정
        response = Response({'message': 'Token refreshed'})
        if access_token:
            response.set_cookie(
                'access_token',
                access_token,
                httponly=True,
                secure=True,
                samesite='Lax'
            )
        return response



# 사용자 등록을 위한 뷰
class RegisterView(generics.CreateAPIView):
    """
    새로운 BusinessMember (사용자)을 등록하는 API 엔드포인트.
    모든 사용자가 접근할 수 있습니다.
    """
    queryset = BusinessMember.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

# 비즈니스 관리용 뷰셋
class BusinessViewSet(viewsets.ModelViewSet):
    """
    Business 모델의 CRUD (생성, 조회, 수정, 삭제) 기능을 제공하는 뷰셋.
    오직 비즈니스 관리자(Admin)만 접근할 수 있습니다.
    """
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [permissions.IsAuthenticated, IsBusinessAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'address', 'phone_number', 'website']
    ordering_fields = ['name']