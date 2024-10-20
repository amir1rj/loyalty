from django.contrib import messages

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import PointRoleForm, CreatePointRoleForm, CreatePointRoleGroupForm, CreateRewardForm
from .models import UserPointsService, PointRoleGroup, PointRole


class TestView(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.first()
        service = UserPointsService(user)
        service.perform_point_roles()

        # Return an empty HTML structure
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Empty Page</title>
        </head>
        <body>
        </body>
        </html>
        """
        return HttpResponse(html_content, content_type="text/html")


class DisplayPointRolesView(View):

    def get(self, request, *args, **kwargs):
        groups = PointRoleGroup.objects.prefetch_related('point_roles').all()

        # Create a list of tuples (role, form)
        role_forms = []
        for group in groups:
            for role in group.point_roles.all():
                form = PointRoleForm(instance=role)
                role_forms.append((role, form))

        context = {
            'groups': groups,
            'role_forms': role_forms,
        }

        return render(request, 'loyalty_models/display_point_role.html', context)

    def post(self, request, *args, **kwargs):
        forms = []
        has_errors = False

        # Extract IDs to process the corresponding forms
        ids = request.POST.getlist('id')  # Get list of IDs from the POST data

        # Loop through each role ID
        for role_id in ids:
            # Fetch the corresponding PointRole instance
            role = PointRole.objects.get(id=role_id)

            # Prepare the data for this specific role's form
            form_data = {
                'id': role_id,
                'number': request.POST.getlist('number')[ids.index(role_id)],
                'from_date': request.POST.getlist('from_date')[ids.index(role_id)],
                'to_date': request.POST.getlist('to_date')[ids.index(role_id)],
                'point_role_type': request.POST.getlist('point_role_type')[ids.index(role_id)],
                'priority': request.POST.getlist('priority')[ids.index(role_id)],
                'is_active': request.POST.getlist('is_active')[ids.index(role_id)] == 'on',
            }

            # Create a form instance with the prepared data
            form = PointRoleForm(form_data, instance=role)

            if form.is_valid():

                form.save()

                # Handle the many-to-many reward relationship
                reward_ids = request.POST.getlist(f'reward_{role_id}')
                if reward_ids:
                    role.reward.set(reward_ids)
                else:
                    role.reward.clear()
            else:
                has_errors = True  # Set the flag to true if any form is invalid
            forms.append((role, form))  # Append the role and form pair for rendering

        if has_errors:
            # Fetch the groups again and pass the modified role_forms structure
            groups = PointRoleGroup.objects.prefetch_related('point_roles').all()
            role_forms = [(role, form) for role, form in forms]

            return render(request, 'loyalty_models/display_point_role.html', {
                'groups': groups,
                'role_forms': role_forms,
            })

        return redirect('point_role_groups')


class CreatePintRoleView(View):
    def get(self, request, *args, **kwargs):
        form = CreatePointRoleForm()
        return render(request, 'loyalty_models/create_point_role.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreatePointRoleForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('point_role_groups')


class DeletePointRoleView(View):
    def get(self, request, pk, *args, **kwargs):
        role = get_object_or_404(PointRole, pk=pk)
        role.delete()
        messages.success(request, 'Point role deleted successfully.')
        return redirect('point_role_groups')


class CreateGroupView(View):
    def get(self, request, *args, **kwargs):
        form = CreatePointRoleGroupForm()
        return render(request, 'loyalty_models/create_point_role_group.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreatePointRoleGroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('point_role_groups')


class CreateRewardView(View):
    def get(self, request, *args, **kwargs):
        form = CreateRewardForm()
        return render(request, 'loyalty_models/create_reward.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateRewardForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('point_role_groups')
