from django.urls import path

from .views import TestView, CreatePointRolesView

urlpatterns = [
    path('/', TestView.as_view()),
    path('/create_point_role', CreatePointRolesView.as_view(), name='point_role_groups'),

]
