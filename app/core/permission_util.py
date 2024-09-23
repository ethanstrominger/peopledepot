from rest_framework.exceptions import ValidationError

from constants import global_admin
from core.field_permissions import FieldPermissions
from core.models import User
from core.models import UserPermission


class PermissionUtil:
    @staticmethod
    def get_lowest_ranked_permission_type(requesting_user: User, target_user: User):
        """Get the highest ranked permission type a requesting user has relative to a target user.

        If the requesting user is an admin, returns global_admin.

        Otherwise, it looks for the projects that both the requesting user and the serialized user are granted
        in user permissions. It then returns the permission type name of the lowest ranked matched permission.

        If the requesting user has no permissions over the serialized user, returns an empty string.

        Args:
            requesting_user (User): user that initiates the API request
            target_user (User): a user that is part of the API response currently being serialized

        Returns:
            str: permission type name of highest permission type the requesting user has relative
            to the serialized user
        """

        if PermissionUtil.is_admin(requesting_user):
            return global_admin
        print("Debug 4", target_user)
        target_user_project_names = UserPermission.objects.filter(
            user=target_user
        ).values_list("project__name", flat=True)
        print("Debug 5")

        matched_requester_permissions = UserPermission.objects.filter(
            user=requesting_user, project__name__in=target_user_project_names
        ).values("permission_type__name", "permission_type__rank")
        print("Debug 6", matched_requester_permissions, requesting_user.first_name)

        lowest_permission_rank = 1000
        lowest_permission_name = ""
        for matched_permission in matched_requester_permissions:
            matched_permission_rank = matched_permission["permission_type__rank"]
            matched_permission_name = matched_permission["permission_type__name"]
            if matched_permission_rank < lowest_permission_rank:
                lowest_permission_rank = matched_permission_rank
                lowest_permission_name = matched_permission_name

        return lowest_permission_name

    @staticmethod
    def get_user_queryset(request):
        """Get the queryset of users that the requesting user has permission to view.

        Called from get_queryset in UserViewSet in views.py.

        Args:
            request: the request object

        Returns:
            queryset: the queryset of users that the requesting user has permission to view
        """
        current_username = request.user.username

        current_user = User.objects.get(username=current_username)
        user_permissions = UserPermission.objects.filter(user=current_user)

        if PermissionUtil.is_admin(current_user):
            queryset = User.objects.all()
        else:
            # Get the users with user permissions for the same projects
            # that the requester has permission to view
            projects = [p.project for p in user_permissions if p.project is not None]
            queryset = User.objects.filter(permissions__project__in=projects).distinct()
        return queryset

    @staticmethod
    def is_admin(user):
        """Check if user is an admin"""
        return user.is_superuser

    @staticmethod
    def validate_patch_request(request):
        """Validate that the requesting user has permission to patch the specified fields
        of the target user.

        Args:
            request: the request object

        Raises:
            PermissionError or ValidationError

        Returns:
            None
        """
        request_fields = request.json().keys()
        requesting_user = request.context.get("request").user
        target_user = User.objects.get(uuid=request.context.get("uuid"))
        PermissionUtil.validate_fields_patchable(
            requesting_user, target_user, request_fields
        )

    @staticmethod
    def validate_fields_patchable(requesting_user, target_user, request_fields):
        """Validate that the requesting user has permission to patch the specified fields
        of the target user.

        Args:
            requesting_user (user): the user that is making the request
            target_user (user): the user that is being updated
            request_fields (json): the fields that are being updated

        Raises:
            PermissionError or ValidationError

        Returns:
            None
        """

        lowest_ranked_name = PermissionUtil.get_lowest_ranked_permission_type(
            requesting_user, target_user
        )
        if lowest_ranked_name == "":
            raise PermissionError("You do not have permission to patch this user")
        valid_fields = FieldPermissions.user_patch_fields[lowest_ranked_name]
        if len(valid_fields) == 0:
            raise PermissionError("You do not have permission to patch this user")

        disallowed_fields = set(request_fields) - set(valid_fields)
        if disallowed_fields:
            raise ValidationError(f"Invalid fields: {', '.join(disallowed_fields)}")

    @staticmethod
    def validate_fields_postable(requesting_user, request_fields):
        """Validate that the requesting user has permission to post the specified fields
        of the new user

        Args:
            requesting_user (user): the user that is making the request
            target_user (user): data for user being created
            request_fields (json): the fields that are being updated

        Raises:
            PermissionError or ValidationError

        Returns:
            None
        """

        if not PermissionUtil.is_admin(requesting_user):
            raise PermissionError("You do not have permission to create a user")
        valid_fields = FieldPermissions.user_post_fields[global_admin]
        disallowed_fields = set(request_fields) - set(valid_fields)
        if disallowed_fields:
            invalid_fields = ", ".join(disallowed_fields)
            valid_fields = ", ".join(valid_fields)
            raise ValidationError(
                f"Invalid fields: {invalid_fields}.   Valid fields are {valid_fields}."
            )

    @staticmethod
    def get_user_read_fields(requesting_user, target_user):
        """Get the fields that the requesting user has permission to view for the target user.

        Args:
            requesting_user (_type_): _description_
            target_user (_type_): _description_

        Raises:
            PermissionError if the requesting user does not have permission to view any
            fields for the target user.

        Returns:
            [User]: List of fields that the requesting user has permission to view for the target user.
        """
        lowest_ranked_name = PermissionUtil.get_lowest_ranked_permission_type(
            requesting_user, target_user
        )
        if lowest_ranked_name == "":
            raise PermissionError("You do not have permission to view this user")
        print("lowest rank", lowest_ranked_name)
        return FieldPermissions.user_read_fields[lowest_ranked_name]
