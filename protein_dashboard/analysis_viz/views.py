from django.shortcuts import render
from .utils import load_and_validate_data
import os

def analysis_dashboard(request):
    # Pass image filenames to template
    # We assume images are in static/analysis_viz/
    context = {
        'pca_variance_plot': 'analysis_viz/pca_variance_plot.png',
        'trajectory_pca_plot': 'analysis_viz/trajectory_pca_plot.png'
    }
    return render(request, 'analysis_viz/dashboard.html', context)

def context_view(request):
    return render(request, 'analysis_viz/context.html')

def step1_view(request):
    data_dir = r"c:\Users\alfredo\Desktop\Protein Dynamics"
    validation_results = load_and_validate_data(data_dir)
    context = {
        'validation_results': validation_results
    }
    return render(request, 'analysis_viz/step1.html', context)

def step2_view(request):
    return render(request, 'analysis_viz/step2.html')

def step3_view(request):
    return render(request, 'analysis_viz/step3.html')

def step4_view(request):
    return render(request, 'analysis_viz/step4.html')
