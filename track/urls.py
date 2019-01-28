from django.urls import path

import track.views


urlpatterns = [
    path('', track.views.home_page, name='home'),

]
