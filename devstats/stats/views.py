from django.shortcuts import render, get_object_or_404, redirect
from stats.models import Developer
from stats.forms import DeveloperCreateForm

# Create your views here.
def developer_list(request):
    developers= Developer.objects.all()

    return render(request,
                  'developer/list.html',
                  {'developers':developers})

def developer_detail(request, username):
    developer = get_object_or_404(Developer,username=username)
    top_repos = developer.repos.all()

    return render(request,
                  'developer/detail.html',
                  {'developer':developer,
                  'toprepos':top_repos})

def developer_create(request):
    if request.method == 'POST':
        form = DeveloperCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            developer = Developer.objects.create(username=username)
            developer.update_profile_from_github()
            developer.update_repos_from_github()

            return redirect('developer_detail', username=username)
    else:
        form = DeveloperCreateForm()
    return render(request,
                  'developer/create.html',
                  {'form':form})