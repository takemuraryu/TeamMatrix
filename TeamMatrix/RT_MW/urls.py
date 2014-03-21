from django.conf.urls import patterns, url
from RT_MW import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^user_interface/$', views.user_interface, name='user_interface'),
                       url(r'^user_interface/create_project/$', views.create_project, name='create_project'),
                       url(r'^user_interface/search_project/$', views.search_project, name='search_project'),
                       url(r'^user_interface/join_project/$', views.join_project, name='join_project'),
                       url(r'^project_detail/(?P<projectid>\w+)/$', views.project_detail, name='project_detail'),
                       url(r'^project_detail/(?P<projectid>\w+)/delete_project/$', views.delete_project, name='delete_project'),
                       url(r'^project_detail/(?P<projectid>\w+)/quit_project/$', views.quit_project, name='quit_project'),
                       url(r'^project_detail/(?P<projectid>\w+)/complete_project/$', views.complete_project, name='complete_project'),
                       url(r'^project_detail/(?P<projectid>\w+)/create_todo_attr/$', views.create_todo_attr, name='create_todo_attr'),
                       url(r'^project_detail/(?P<projectid>\w+)/invite_member/$', views.invite_member, name='invite_member'),
                       url(r'^project_detail/(?P<projectid>\w+)/search_member/$', views.search_member, name='search_member'),
                       url(r'^project_detail/(?P<projectid>\w+)/detail_todo_attr/(?P<attrid>\w+)/$', views.detail_todo_attr, name='detail_todo_attr'),
                       url(r'^project_detail/(?P<projectid>\w+)/single_todo_attr/(?P<attrid>\w+)/$', views.single_todo_attr, name='single_todo_attr'),
                       url(r'^project_detail/(?P<projectid>\w+)/detail_todo_attr/(?P<attrid>\w+)/delete_todo_attr/$', views.delete_todo_attr, name='delete_todo_attr'),
                       url(r'^project_detail/(?P<projectid>\w+)/detail_todo_attr/(?P<attrid>\w+)/tick_todo_attr/$', views.tick_todo_attr, name='tick_todo_attr'),
)
