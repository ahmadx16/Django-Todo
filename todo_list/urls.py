
from django.urls import path, include


urlpatterns = [
    path('', include('tasks.urls')),
    path('user/', include('users.urls'))
]

handler404 = 'users.views.error_404_view'
handler500 = 'users.views.error_500_view'
