from django.contrib import admin
from django.urls import path
from analysis_viz.views import analysis_dashboard, context_view, step1_view, step2_view, step3_view, step4_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', analysis_dashboard, name='dashboard'),
    path('context/', context_view, name='context'),
    path('step1/', step1_view, name='step1'),
    path('step2/', step2_view, name='step2'),
    path('step3/', step3_view, name='step3'),
    path('step4/', step4_view, name='step4'),
]
