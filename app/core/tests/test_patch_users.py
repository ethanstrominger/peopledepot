import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from constants import project_lead
from core.api.views import UserViewSet
from core.base_user_cru_constants import user_field_permissions
from core.derived_user_cru_permissions import derive_cru_fields
from core.permission_util import PermissionUtil
from core.tests.utils.seed_constants import garry_name
from core.tests.utils.seed_constants import patti_name
from core.tests.utils.seed_constants import valerie_name
from core.tests.utils.seed_constants import wally_name
from core.tests.utils.seed_constants import wanda_name
from core.tests.utils.seed_constants import winona_name
from core.tests.utils.seed_constants import zani_name
from core.tests.utils.seed_user import SeedUser

count_website_members = 4
count_people_depot_members = 3
count_members_either = 6


def fields_match(first_name, user_data, fields):
    for user in user_data:
        if user["first_name"] == first_name:
            return set(user.keys()) == set(fields)
    return False


def patch_request_to_view(requester, target_user, update_data):
    factory = APIRequestFactory()
    request = factory.patch(
        reverse("user-detail", args=[target_user.uuid]), update_data, format="json"
    )
    force_authenticate(request, user=requester)
    view = UserViewSet.as_view({"patch": "partial_update"})
    response = view(request, uuid=requester.uuid)
    return response


@pytest.mark.django_db
class TestPatchUser:
    def test_admin_update_request_succeeds(self):  #
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        target_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[target_user.uuid])
        data = {
            "last_name": "Updated",
            "gmail": "update@example.com",
        }
        response = client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_admin_cannot_update_created_at(self):
        requester = SeedUser.get_user(garry_name)
        client = APIClient()
        client.force_authenticate(user=requester)

        target_user = SeedUser.get_user(valerie_name)
        url = reverse("user-detail", args=[target_user.uuid])
        data = {
            "created_at": "2022-01-01T00:00:00Z",
        }
        response = client.patch(url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "created_at" in response.json()[0]

    def validate_fields_updateable(self):
        PermissionUtil.validate_fields_updateable(
            SeedUser.get_user(garry_name),
            SeedUser.get_user(valerie_name),
            ["first_name", "last_name", "gmail"],
        )

    def test_created_at_not_updateable(self):
        with pytest.raises(ValidationError):
            PermissionUtil.validate_fields_updateable(
                SeedUser.get_user(garry_name),
                SeedUser.get_user(valerie_name),
                ["created_at"],
            )

    def test_project_lead_can_update_name(self):
        PermissionUtil.validate_fields_updateable(
            SeedUser.get_user(wanda_name),
            SeedUser.get_user(wally_name),
            ["first_name", "last_name"],
        )

    def test_project_lead_cannot_update_current_title(self):
        with pytest.raises(ValidationError):
            PermissionUtil.validate_fields_updateable(
                SeedUser.get_user(wanda_name),
                SeedUser.get_user(wally_name),
                ["current_title"],
            )

    def test_cannot_update_first_name_for_member_of_other_project(self):
        with pytest.raises(PermissionError):
            PermissionUtil.validate_fields_updateable(
                SeedUser.get_user(wanda_name),
                SeedUser.get_user(patti_name),
                ["first_name"],
            )

    def test_team_member_cannot_update_first_name_for_member_of_same_project(self):
        with pytest.raises(PermissionError):
            PermissionUtil.validate_fields_updateable(
                SeedUser.get_user(wally_name),
                SeedUser.get_user(winona_name),
                ["first_name"],
            )

    def test_multi_project_requester_can_update_first_name_of_member_if_requester_is_project_leader(
        self,
    ):
        PermissionUtil.validate_fields_updateable(
            SeedUser.get_user(zani_name), SeedUser.get_user(wally_name), ["first_name"]
        )

    def test_multi_project_user_cannot_update_first_name_of_member_if_reqiester_is_project_member(
        self,
    ):
        with pytest.raises(PermissionError):
            PermissionUtil.validate_fields_updateable(
                SeedUser.get_user(zani_name),
                SeedUser.get_user(patti_name),
                ["first_name"],
            )

    def test_allowable_update_fields_configurable(self):
        """Test that the fields that can be updated are configurable.

        This test mocks a PATCH request to skip submitting the request to the server and instead
        calls the view directly with the request.  This is done so that variables used by the
        server can be set to test values.
        """

        user_field_permissions[project_lead] = {
            "last_name": "CRU",
            "gmail": "CRU",
        }

        requester = SeedUser.get_user(wanda_name)  # project lead for website
        update_data = {"last_name": "Smith", "gmail": "smith@example.com"}
        target_user = SeedUser.get_user(wally_name)
        derive_cru_fields()
        response = patch_request_to_view(requester, target_user, update_data)

        assert response.status_code == status.HTTP_200_OK

    def test_not_allowable_update_fields_configurable(self):
        """Test that the fields that are not configured to be updated cannot be updated.

        See documentation for test_allowable_update_fields_configurable for more information.
        """

        requester = SeedUser.get_user(wanda_name)  # project lead for website
        update_data = {"last_name": "Smith"}
        target_user = SeedUser.get_user(wally_name)
        derive_cru_fields()
        response = patch_request_to_view(requester, target_user, update_data)

        assert response.status_code == status.HTTP_200_OK