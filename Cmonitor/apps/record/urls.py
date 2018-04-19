from django.conf.urls import url

from apps.record import views

urlpatterns = [
    url('task/', views.task_view, name='task'),
    url('taskRecord/', views.taskRecord_view, name='taskRecord'),
    url('runTask/', views.runTaskfunc_view),
    url('item/search/', views.searchTaskItem),
    url('state/search/', views.searchTaskState),
]