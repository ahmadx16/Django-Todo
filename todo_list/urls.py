from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('user/', include('users.urls'))
]

handler404 = 'users.views.error_404_view'
handler500 = 'users.views.error_500_view'
