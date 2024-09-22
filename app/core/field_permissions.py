"""Variables that define the fields that can be read or updated by a user based on user permissionss

Variables:
    me_endpoint_read_fields: list of fields that can be read by the requesting user for the me endpoint
    me_endpoint_patch_fields: list of fields that can be updated by the requesting user for the me endpoint
    * Note: me_end_point gets or updates information about the requesting user

    user_read_fields:
        user_read_fields[global_admin]: list of fields a global admin can read for a user
        user_read_fields[project_lead]: list of fields a project lead can read for a user
        user_read_fields[project_member]: list of fields a project member can read for a user
        user_read_fields[practice_area_admin]: list of fields a practice area admin can read for a user
    user_patch_fields:
        user_patch_fields[global_admin]: list of fields a global admin can update for a user
        user_patch_fields[project_lead]: list of fields a project lead can update for a user
        user_patch_fields[project_member]: list of fields a project member can update for a user
        user_patch_fields[practice_area_admin]: list of fields a practice area admin can update for a user
    user_post_fields:
        user_post_fields[global_admin]: list of fields a global admin can specify when creating a user
"""

from constants import global_admin
from constants import practice_area_admin
from constants import project_lead
from constants import project_member
from core.user_field_permissions_constants import me_endpoint_permissions
from core.user_field_permissions_constants import self_register_fields
from core.user_field_permissions_constants import user_field_permissions


class FieldPermissions:
    # *************************************************************
    # See pydoc at top of file for description of these variables *
    # *************************************************************

    user_read_fields = {
        project_lead: [],
        project_member: [],
        practice_area_admin: [],
        global_admin: [],
    }
    user_patch_fields = {
        project_lead: [],
        project_member: [],
        practice_area_admin: [],
        global_admin: [],
    }
    user_post_fields = {
        project_lead: [],
        project_member: [],
        practice_area_admin: [],
        global_admin: [],
    }
    me_endpoint_read_fields = []
    me_endpoint_patch_fields = []
    self_register_fields = []

    # Gets the fields in field_permission that have the permission specified by cru_permission
    # Args:
    #   field_permissions (dictionary): dictionary of field permissions.  Key: field name. Value: "CRU" or subset.
    #   cru_permission (str): permission to check for in field_permissions (C, R, or U)
    # Returns:
    #   [str]: list of field names that have the specified permission
    @classmethod
    def _get_fields_with_priv(cls, field_permissions, cru_permission):
        ret_array = []
        for key, value in field_permissions.items():
            if cru_permission in value:
                ret_array.append(key)
        return ret_array

    @classmethod
    def derive_cru_fields(cls):
        cls.me_endpoint_read_fields = cls._get_fields_with_priv(
            me_endpoint_permissions, "R"
        )
        cls.me_endpoint_patch_fields = cls._get_fields_with_priv(
            me_endpoint_permissions, "R"
        )
        cls.self_register_fields = self_register_fields
        for permission_type in [
            project_lead,
            project_member,
            practice_area_admin,
            global_admin,
        ]:
            cls.user_read_fields[permission_type] = cls._get_fields_with_priv(
                user_field_permissions[permission_type], "R"
            )
            cls.user_patch_fields[permission_type] = cls._get_fields_with_priv(
                user_field_permissions[permission_type], "U"
            )
            cls.user_post_fields[permission_type] = cls._get_fields_with_priv(
                user_field_permissions[permission_type], "C"
            )


FieldPermissions.derive_cru_fields()