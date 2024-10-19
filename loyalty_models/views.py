from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import PointRoleForm
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


class CreatePointRolesView(View):

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

        return render(request, 'loyalty_models/create_point_role.html', context)

    def post(self, request, *args, **kwargs):
        # Handle form submissions


        # Initialize a list to store forms
        forms = []
        # Initialize a flag for error checking
        has_errors = False

        # Extract IDs to process the corresponding forms
        ids = request.POST.getlist('id')  # Get list of IDs from the POST data

        # Loop through each role ID
        for role_id in ids:
            # Fetch the corresponding PointRole instance
            role = PointRole.objects.get(id=role_id)

            # Prepare the data for this specific role's form
            form_data = {
                'number': request.POST.getlist('number')[ids.index(role_id)],
                'from_date': request.POST.getlist('from_date')[ids.index(role_id)],
                'to_date': request.POST.getlist('to_date')[ids.index(role_id)],
                'point_role_type': request.POST.getlist('point_role_type')[ids.index(role_id)],
                'priority': request.POST.getlist('priority')[ids.index(role_id)],
                'is_active': request.POST.getlist('is_active')[ids.index(role_id)] == 'on',  # Convert 'on' to True
            }

            # Create a form instance with the prepared data
            form = PointRoleForm(form_data, instance=role)

            # Validate the form
            if form.is_valid():
                form.save()  # Save the form if valid
            else:
                has_errors = True  # Set the flag to true if any form is invalid
                forms.append(form)  # Append the form with errors for rendering
                print(f'Errors for role ID {role_id}:', form.errors)

        if has_errors:
            # Render the same template with forms containing errors
            return render(request, 'your_template_name.html', {'forms': forms})

        return redirect('point_role_groups')
