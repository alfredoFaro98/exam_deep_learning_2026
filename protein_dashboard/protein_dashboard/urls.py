from django.contrib import admin
from django.urls import path
from analysis_viz.views import analysis_dashboard, context_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', analysis_dashboard, name='dashboard'),
    path('context/', context_view, name='context'),
]
