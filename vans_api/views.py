from django.shortcuts import redirect


def index(request):
    """Index view"""
    return redirect('/admin/')