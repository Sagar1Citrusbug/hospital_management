from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from hms.interface.user.urls import router as user_router
# from hms.interface.doctor.urls import router as user_router
# from hms.interface.user.urls import router as user_router
# from hms.interface.user.urls import router as user_router


schema_view = get_schema_view(
    openapi.Info(
        title="HMS",
        default_version='v0',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),

  path('', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
  path("", include(user_router.urls)),
    # path("", include(doctor_router.urls)),
    # path("", include(patient_router.urls)),
    # path("", include(appointment_router.urls)),
]