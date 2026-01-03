from django.shortcuts import render

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
