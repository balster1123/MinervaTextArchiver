"""minerva URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from minerva.webapp.views import DiscussionStatsView, AppGroupStatsView, DiscussionMessagesView, DiscussionSummaryView, \
    UserHashtagsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webapp/discussions/stats', DiscussionStatsView.as_view(), name='discussion_stats'),
    path('webapp/discussions/summary', DiscussionSummaryView.as_view(), name='discussion_summary'),
    path('webapp/messages', DiscussionMessagesView.as_view(), name='discussion_messages'),
    path('webapp/apps/groups', AppGroupStatsView.as_view(), name='app_group_stats'),
    path('webapp/hashtags', UserHashtagsView.as_view(), name='user_hashtags')
]
