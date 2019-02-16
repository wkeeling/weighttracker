from django.urls import path

import track.views


urlpatterns = [
    path('', track.views.home_page, name='home'),
    path('chart/', track.views.chart, name='chart'),
    path('data/', track.views.DataView.as_view(), name='data'),
]
