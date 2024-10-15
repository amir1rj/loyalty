from django.db.models import Prefetch

from loyalty_program_models.loyalty_models.models import PointRoleGroup, PointRole, UserPoints


# class UserPointsService:
#     def __init__(self, user):
#         self.user = user
#         self.user_points, created = UserPoints.objects.get_or_create(user=user)
#
#     # def calculate_points(self):
#     #     """
#     #     Calculate points for the user based on their PointRoles.
#     #     """
#     #     # Get all point roles associated with this user
#     #     point_roles = PointRole.objects.filter(group__user=self.user)
#     #
#     #     # Initialize total points
#     #     total_points = 0
#     #
#     #     # Add points based on each PointRole's logic
#     #     for role in point_roles:
#     #         if role.point_role_type == 'some_condition':  # Customize logic for roles
#     #             total_points += 10  # Add points based on your logic here
#     #         elif role.point_role_type == 'another_condition':
#     #             total_points += 20  # Different logic for another type
#     #         # Add more conditions as needed based on role type, group, etc.
#     #
#     #     # Update the user's points in the UserPoints model
#     #     self.user_points.points += total_points
#     #     self.user_points.save()
#     #
#     # def add_points_based_on_role(self, point_role):
#     #     """
#     #     Add points based on a specific PointRole.
#     #     """
#     #     points_to_add = 0
#     #
#     #     self.user_points.points += points_to_add
#     #     self.user_points.save()
#     #
#     #     return points_to_add
#
#     @staticmethod
#     def get_all_groups():
#         # Fetch all PointRoleGroup instances that have at least one active PointRole
#         active_groups_with_roles = PointRoleGroup.objects.prefetch_related(
#             Prefetch(
#                 'poit_roles',
#                 queryset=PointRole.objects.filter(is_active=True).order_by('priority'),
#                 to_attr='active_roles'  # Store the prefetched PointRoles in this attribute
#             )
#         )
#         return active_groups_with_roles
#
#     def perform_point_roles(self):
#         groups = self.get_all_groups()
#         should_continue = False
#         for role_group in groups:
#             for role in role_group.active_roles:
#                 if role.type == "number_of_purchases":
#                     if role.check_number_of_purchases(self.user).get('success'):
#                         break
#
#                     print(role.check_number_of_purchases(self.user))
