from django.urls import path
from auths.views import *
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('comments/', include('comments.urls')),
