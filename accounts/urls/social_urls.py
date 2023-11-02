from django.urls import re_path

from accounts.auth_social import views

urlpatterns = [
    re_path(
        r"^o/(?P<provider>\S+)/$",
        views.ProviderAuthView.as_view(),
        name="provider-auth",
    )
]
