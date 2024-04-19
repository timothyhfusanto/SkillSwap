from django.urls import path
from accounts import views, templates

app_name = "accounts"

urlpatterns = [
	path("sign-up/", views.register_view, name="sign-up"),
 	path("sign-in/", views.login_view, name="sign-in"),
  	path("sign-out/", views.logout_view, name="sign-out"),
]