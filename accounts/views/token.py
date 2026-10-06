
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView


class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
       

        refresh_token = request.COOKIES.get("refresh_token")

        

        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found."},
                status=401,
            )

        try:
            refresh = RefreshToken(refresh_token)

            access_token = str(
                refresh.access_token
            )

            return Response({
                "access": access_token,
            })

        except Exception as error:
           

            return Response(
                {
                    "detail": "Invalid or expired refresh token."
                },
                status=401,
            )


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        response = Response({
            "detail": "Logged out successfully."
        })

        response.delete_cookie(
            "refresh_token",
            samesite="Lax",
        )

        return response
