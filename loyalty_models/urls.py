from django.urls import path

from .views import TestView, DisplayPointRolesView, CreatePintRoleView, DeletePointRoleView, CreateRewardView, \
    CreateGroupView

urlpatterns = [
    path('/', TestView.as_view()),
    path('/diplay_point_role', DisplayPointRolesView.as_view(), name='point_role_groups'),
    path('/create_point_role', CreatePintRoleView.as_view(), name='create_point_role'),
    path('/create_point_role_group', CreateGroupView.as_view(), name='create_point_role_group'),
    path('/create_reward', CreateRewardView.as_view(), name='create_reward'),
    path('/point-role/delete/<int:pk>/', DeletePointRoleView.as_view(), name='delete_point_role'),

]
