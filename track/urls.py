from django.urls import path

import track.views


urlpatterns = [
    path('', track.views.home_page, name='home'),
    path('chart/', track.views.chart, name='chart'),
    path('data/', track.views.MyDataView.as_view(), name='data'),
    path('add/', track.views.AddMeasurementView.as_view(), name='add'),
]
