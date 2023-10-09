from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from rest_framework import permissions
from hms.interface.user.urls import router as user_router


from django.contrib import admin
from django.urls import path
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from hms.interface.user.urls import router as user_router
from hms.interface.patient.urls import router as patient_router
from hms.interface.doctor.urls import router as doctor_router


ENABLE_API = settings.ENABLE_API
PROJECT_URL = ""
API_SWAGGER_URL = "api/v0/"
REDIRECTION_URL = API_SWAGGER_URL if ENABLE_API else PROJECT_URL

urlpatterns = [
    path("superadmin/", admin.site.urls),
    path("", RedirectView.as_view(url="api/v0/", permanent=False)),
]

urlpatterns += [
    path(
        API_SWAGGER_URL,
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(API_SWAGGER_URL, include(user_router.urls)),
    path(API_SWAGGER_URL, include(patient_router.urls)),
    path(API_SWAGGER_URL, include(doctor_router.urls)),
    path("api/v0/schema/", SpectacularAPIView.as_view(), name="schema"),
    # path(
    #     "api/token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    # ),
    # path(
    #     "api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    # ),
]
