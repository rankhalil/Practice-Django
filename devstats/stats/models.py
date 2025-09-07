from django.db import models
from github import Github, GithubException
from django.conf import settings

# Create your models here.

class Developer(models.Model):
    username = models.CharField(max_length=100,
                                unique=True)
    name = models.CharField(max_length=100,blank=True)
    location = models.CharField(max_length=100,blank=True)
    company = models.CharField(max_length=100,blank=True)
    avatar_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    total_followers = models.PositiveIntegerField(default=0)
    total_following = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gh_user = None

    def __str__(self):
        return self.username

    def _get_github_user(self):
        if self._gh_user == None:
            gh = Github(settings.GITHUB_TOKEN,
                        per_page=settings.GITHUB_OBJECTS_PER_PAGE)
            self._gh_user = gh.get_user(self.username)
        return self._gh_user

    def update_profile_from_github(self):
        user_obj = self._get_github_user()
        self.name = user_obj.name or ''
        self.location = user_obj.location or ''
        self.company = user_obj.company or ''
        self.avatar_url = user_obj.avatar_url or ''
        self.website_url = user_obj.blog or ''
        self.total_followers = user_obj.followers or 0
        self.total_following = user_obj.following or 0

        self.save()

    def update_repos_from_github(self):
        gh_repos = self._get_github_user().get_repos(type='owner')
        for gh_repo in gh_repos:
            repo, created = self.repos.get_or_create(name=gh_repo.name)
            repo.stargazers_count = gh_repo.stargazers_count
            repo.watchers_count = gh_repo.watchers_count
            repo.forks_count = gh_repo.forks_count

            repo.save()
            
class Repository(models.Model):
    name = models.CharField(max_length=250)
    developer = models.ForeignKey(Developer,
                                  related_name='repos',
                                  on_delete=models.CASCADE
    )
    stargazers_count = models.PositiveIntegerField(default=0)
    watchers_count = models.PositiveIntegerField(default=0)
    forks_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together= [('developer','name')]

    def __str__(self):
        return f'{self.developer.username}/{self.name}'

    def get_github_url(self):
        return 'https://github.com' + self.__str__()
