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
from django.urls import reverse
from rest_framework.test import APIClient

from constants import global_admin
from constants import project_lead
from constants import project_member
from core.derived_user_cru_permissions import user_read_fields
from core.permission_util import PermissionUtil
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import patrick_name
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_name
from core.tests.utils.seed_constants import winona_name
from core.tests.utils.seed_constants import zani_name
from core.tests.utils.seed_user import SeedUser

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6

_user_get_url = reverse("user-list")


def fields_match_for_get_user(first_name, response_data, fields):
    for user in response_data:
        if user["first_name"] == first_name:
            return set(user.keys()) == set(fields)
    return False


@pytest.mark.django_db
class TestGetUser:
    def test_global_admin_user_is_admin(self):
        assert PermissionUtil.is_admin(SeedUser.get_user(garry_name))

    def test_non_global_admin_user_is_not_admin(self):
        assert not PermissionUtil.is_admin(SeedUser.get_user(wanda_name))

    def test_admin_highest_for_admin(self):
        assert (
            PermissionUtil.get_lowest_ranked_permission_type(
                SeedUser.get_user(garry_name), SeedUser.get_user(valerie_name)
            )
            == global_admin  # noqa W503
        )

    def test_team_member_highest_for_two_team_members(self):
        assert (
            PermissionUtil.get_lowest_ranked_permission_type(
                SeedUser.get_user(wally_name), SeedUser.get_user(winona_name)
            )
            == project_member  # noqa W503
        )
        assert (
            PermissionUtil.get_lowest_ranked_permission_type(
                SeedUser.get_user(wally_name), SeedUser.get_user(wanda_name)
            )
            == project_member  # noqa W503
        )

    def test_team_member_cannot_read_fields_of_non_team_member(self):
        assert (
            PermissionUtil.get_lowest_ranked_permission_type(
                SeedUser.get_user(wally_name), SeedUser.get_user(garry_name)
            )
            == ""  # noqa W503
        )

    def test_team_member_cannot_read_ields_of_other_team(self):
        assert (
            not PermissionUtil.get_lowest_ranked_permission_type(
                SeedUser.get_user(wally_name), SeedUser.get_user(wanda_name)
            )
            == ""  # noqa W503
        )

    def test_get_url_results_for_multi_project_requester_when_project_lead(self):
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(zani_name))
        response = client.get(_user_get_url)
        assert response.status_code == 200
        assert len(response.json()) == count_members_either
        # assert fields for zani, who is a project lead on same team as wanda,
        # match project_lead fields
        assert fields_match_for_get_user(
            wanda_name,
            response.json(),
            user_read_fields[project_lead],
        )

    def test_get_url_results_for_multi_project_requester_when_project_member(self):
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(zani_name))
        response = client.get(_user_get_url)
        assert response.status_code == 200
        assert len(response.json()) == count_members_either
        # assert fields for zani, who is a project member on same team as wanda,
        # match project_member fields
        assert fields_match_for_get_user(
            SeedUser.get_user(patrick_name).first_name,
            response.json(),
            user_read_fields[project_member],
        )

    def test_get_url_results_for_project_admin(self):
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(wanda_name))
        response = client.get(_user_get_url)
        assert response.status_code == 200
        assert len(response.json()) == count_website_members
        assert fields_match_for_get_user(
            SeedUser.get_user(winona_name).first_name,
            response.json(),
            user_read_fields[global_admin],
        )

    def test_get_results_for_users_on_same_teamp(self):
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(wally_name))
        response = client.get(_user_get_url)

        assert response.status_code == 200
        assert fields_match_for_get_user(
            SeedUser.get_user(winona_name).first_name,
            response.json(),
            user_read_fields[project_member],
        )
        assert fields_match_for_get_user(
            SeedUser.get_user(wanda_name).first_name,
            response.json(),
            user_read_fields[project_member],
        )
        assert len(response.json()) == count_website_members

    def test_no_user_permission(self):
        client = APIClient()
        client.force_authenticate(user=SeedUser.get_user(valerie_name))
        response = client.get(_user_get_url)
        assert response.status_code == 200
        assert len(response.json()) == 0