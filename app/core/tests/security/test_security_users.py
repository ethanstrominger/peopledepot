# Change fields that can be viewed in code to what Bonnie specified
# Add update api test
# Write API to get token
# Create a demo script for adding users with password of Hello2024.
# Create a shell script for doing a get
# Create a shell script for doing a patch
# Change fields that can be viewed in my wiki to what Bonnie specified
# Add more tests for update
# Add print statements to explain what is being tested
# Add tests for the patch API
# Add tests for and implement put (disallow), post, and delete API
# Update my Wiki for put, patch, post, delete
# Add proposals:
#   - use flag instead of role for admin and verified
# . -
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from constants import global_admin
from constants import project_team_member
from core.permission_util import PermissionUtil
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import patrick_name
from core.tests.utils.seed_constants import patti_name
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_name
from core.tests.utils.seed_constants import winona_name
from core.tests.utils.seed_constants import zani_name
from core.tests.utils.seed_user import SeedUser
from core.tests.utils.utils_test import show_test_info
from core.user_cru_permissions import UserCruPermissions

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6


def fields_match(first_name, user_data, fields):
    for user in user_data:
        if user["first_name"] == first_name:
            return set(user.keys()) == set(fields)
    return False


@pytest.mark.django_db
class TestUser:
    @classmethod
    def authenticate_user(cls, user_name):
        client = APIClient()
        response = SeedUser.force_authenticate_get_user(client, user_name)
        return response


    def test_can_read_logic(self, load_test_user_data):
        show_test_info("=== Validating logic for can read===")
        show_test_info("==> is admin")
        show_test_info(
            "Validate is_admin returns true for a global admin and false for a project admin"
        )
        assert PermissionUtil.is_admin(SeedUser.get_user(garry_name))
        assert not PermissionUtil.is_admin(SeedUser.get_user(wanda_name))

        show_test_info("Globan admin can read senstive fields of any user")
        assert PermissionUtil.can_read_all_user(
            SeedUser.get_user(garry_name), SeedUser.get_user(valerie_name)
        )

        show_test_info("==> project member")
        show_test_info("Project member can read basic info for another project member")
        assert PermissionUtil.can_read_basic_user(
            SeedUser.get_user(wally_name), SeedUser.get_user(winona_name)
        )
        show_test_info("Team member can read basic info for another project member")
        assert PermissionUtil.can_read_basic_user(
            SeedUser.get_user(wally_name), SeedUser.get_user(wanda_name)
        )
        show_test_info("Team member can read basic info for another project member")
        assert not PermissionUtil.can_read_basic_user(
            SeedUser.get_user(wally_name), SeedUser.get_user(garry_name)
        )
        assert not PermissionUtil.can_read_all_user(
            SeedUser.get_user(wally_name), SeedUser.get_user(wanda_name)
        )

        show_test_info("==> project admin")
        assert PermissionUtil.can_read_all_user(
            SeedUser.get_user(wanda_name), SeedUser.get_user(wally_name)
        )

    def test_global_admin(self, load_test_user_data):
        logged_in_userresponse = self.authenticate_user(SeedUser.get_user(garry_name).first_name)
        assert logged_in_user is not None
        assert response.status_code == 200
        assert get_user_model().objects.count() > 0
        assert len(response.json()) == len(SeedUser.users)

    def test_multi_project_user(self, load_test_user_data):
        response = self.authenticate_user(SeedUser.get_user(zani_name).first_name)
        assert response.status_code == 200
        assert len(response.json()) == count_members_either
        assert fields_match(
            SeedUser.get_user(wanda_name).first_name,
            response.json(),
            UserCruPermissions.read_fields["user"][global_admin],
        )
        assert fields_match(
            SeedUser.get_user(patrick_name).first_name,
            response.json(),
            UserCruPermissions.read_fields["user"][project_team_member],
        )

    def test_project_admin(self, load_test_user_data):
        response = self.authenticate_user(SeedUser.get_user(wanda_name).first_name)
        assert response.status_code == 200
        print("debug 2", response.json())
        assert len(response.json()) == count_website_members
        assert fields_match(
            SeedUser.get_user(winona_name).first_name,
            response.json(),
            UserCruPermissions.read_fields["user"][global_admin],
        )

    def test_project_team_member(self, load_test_user_data):
        response = self.authenticate_user(SeedUser.get_user(wally_name).first_name)
        assert response.status_code == 200
        assert fields_match(
            SeedUser.get_user(winona_name).first_name,
            response.json(),
            UserCruPermissions.read_fields["user"][project_team_member],
        )
        assert fields_match(
            SeedUser.get_user(wanda_name).first_name,
            response.json(),
            UserCruPermissions.read_fields["user"][project_team_member],
        )
        assert len(response.json()) == count_website_members

    def test_no_project(self, load_test_user_data):
        response = self.authenticate_user(valerie_name)
        assert response.status_code == 200
        assert len(response.json()) == 0
