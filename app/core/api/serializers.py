from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from constants import global_admin
from constants import project_team_member
from core.models import Affiliate
from core.models import Affiliation
from core.models import CheckType
from core.models import Event
from core.models import Faq
from core.models import FaqViewed
from core.models import Location
from core.models import PermissionType
from core.models import PracticeArea
from core.models import ProgramArea
from core.models import Project
from core.models import Sdg
from core.models import Skill
from core.models import SocMajor
from core.models import StackElement
from core.models import StackElementType
from core.models import UrlType
from core.models import User
from core.models import UserPermissions
from core.permission_util import PermissionUtil
from core.user_cru_permissions import UserCruPermissions
from core.models import UserPermission
from core.models import UserStatusType


class PracticeAreaSerializer(serializers.ModelSerializer):
    """Used to retrieve practice area info"""

    class Meta:
        model = PracticeArea
        fields = (
            "uuid",
            "created_at",
            "updated_at",
            "name",
            "description",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class UserPermissionSerializer(serializers.ModelSerializer):
    """Used to retrieve user permissions"""

    class Meta:
        model = UserPermission
        fields = (
            "uuid",
            "created_at",
            "updated_at",
            "user",
            "permission_type",
            "project",
            "practice_area",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class UserSerializer(serializers.ModelSerializer):
    """Used to retrieve user info"""

    time_zone = TimeZoneSerializerField(use_pytz=False)

    class Meta:
        model = User

        # to_representation overrides the need for fields
        # if fields is removed, syntax checker will complain
        fields = "__all__"

    @staticmethod
    def _get_read_fields(__cls__, requesting_user: User, serialized_user: User):
        if PermissionUtil.can_read_all_user(requesting_user, serialized_user):
            represent_fields = UserCruPermissions.read_fields["user"][global_admin]
        elif PermissionUtil.can_read_basic_user(requesting_user, serialized_user):
            represent_fields = UserCruPermissions.read_fields["user"][
                project_team_member
            ]
        else:
            message = "You do not have permission to view this user"
            raise PermissionError(message)
        return represent_fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        requesting_user: User = request.user
        serialized_user: User = instance
        if request.method != "GET":
            return representation

        read_fields = UserSerializer._get_read_fields(
            self, requesting_user, serialized_user
        )

        new_representation = {}
        for field_name in read_fields:
            new_representation[field_name] = representation[field_name]
        return new_representation


class ProjectSerializer(serializers.ModelSerializer):
    """Used to retrieve project info"""

    sdgs = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = (
            "uuid",
            "name",
            "description",
            "created_at",
            "updated_at",
            "completed_at",
            "github_org_id",
            "github_primary_repo_id",
            "hide",
            "google_drive_id",
            "image_logo",
            "image_hero",
            "image_icon",
            "sdgs",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
            "completed_at",
        )


class EventSerializer(serializers.ModelSerializer):
    """Used to retrieve event info"""

    class Meta:
        model = Event
        fields = (
            "uuid",
            "name",
            "start_time",
            "duration_in_min",
            "video_conference_url",
            "additional_info",
            "project",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class AffiliateSerializer(serializers.ModelSerializer):
    """Used to retrieve Sponsor Partner info"""

    class Meta:
        model = Affiliate
        fields = (
            "uuid",
            "partner_name",
            "partner_logo",
            "is_active",
            "url",
            "is_org_sponsor",
            "is_org_partner",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class FaqSerializer(serializers.ModelSerializer):
    """Used to retrieve faq info"""

    class Meta:
        model = Faq
        fields = (
            "uuid",
            "question",
            "answer",
            "tool_tip_name",
        )
        read_only_fields = ("uuid", "created_on", "last_updated")


class FaqViewedSerializer(serializers.ModelSerializer):
    """
    Retrieve each date/time the specified FAQ is viewed
    """

    class Meta:
        model = FaqViewed
        fields = (
            "uuid",
            "faq",
        )
        read_only_fields = (
            "uuid",
            "faq",
        )


class LocationSerializer(serializers.ModelSerializer):
    """Used to retrieve Location info"""

    class Meta:
        model = Location
        fields = (
            "uuid",
            "name",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "zip",
            "phone",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


LocationSerializer._declared_fields["zip"] = serializers.CharField(source="zipcode")


class ProgramAreaSerializer(serializers.ModelSerializer):
    """Used to retrieve program_area info"""

    class Meta:
        model = ProgramArea
        fields = ("uuid", "name", "description", "image")
        read_only_fields = ("uuid", "created_at", "updated_at")


class SkillSerializer(serializers.ModelSerializer):
    """
    Used to retrieve Skill info
    """

    class Meta:
        model = Skill
        fields = (
            "uuid",
            "name",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class StackElementSerializer(serializers.ModelSerializer):
    """Used to retrieve stack element info"""

    class Meta:
        model = StackElement
        fields = (
            "uuid",
            "name",
            "description",
            "url",
            "logo",
            "active",
            "element_type",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class PermissionTypeSerializer(serializers.ModelSerializer):
    """
    Used to retrieve each permission_type info
    """

    class Meta:
        model = PermissionType
        fields = ("uuid", "name", "description")
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class StackElementTypeSerializer(serializers.ModelSerializer):
    """Used to retrieve stack element types"""

    class Meta:
        model = StackElementType
        fields = (
            "uuid",
            "name",
            "description",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class SdgSerializer(serializers.ModelSerializer):
    """
    Used to retrieve Sdg
    """

    projects = serializers.StringRelatedField(many=True)

    class Meta:
        model = Sdg
        fields = (
            "uuid",
            "name",
            "description",
            "image",
            "projects",
        )
        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class AffiliationSerializer(serializers.ModelSerializer):
    """
    Used to retrieve Affiliation
    """

    class Meta:
        model = Affiliation
        fields = (
            "uuid",
            "affiliate",
            "project",
            "created_at",
            "ended_at",
            "is_sponsor",
            "is_partner",
        )
        read_only_fields = ("uuid", "created_at", "updated_at")


class CheckTypeSerializer(serializers.ModelSerializer):
    """
    Used to retrieve check_type info
    """

    class Meta:
        model = CheckType
        fields = ("uuid", "name", "description")
        read_only_fields = ("uuid", "created_at", "updated_at")


class SocMajorSerializer(serializers.ModelSerializer):
    """Used to retrieve soc_major info"""

    class Meta:
        model = SocMajor
        fields = ("uuid", "occ_code", "title")
        read_only_fields = ("uuid", "created_at", "updated_at")


class UrlTypeSerializer(serializers.ModelSerializer):
    """Used to retrieve url_type info"""

    class Meta:
        model = UrlType
        fields = ("uuid", "name", "description")
        read_only_fields = ("uuid", "created_at", "updated_at")


class UserStatusTypeSerializer(serializers.ModelSerializer):
    """Used to retrieve user_status_type info"""

    class Meta:
        model = UserStatusType
        fields = ("uuid", "name", "description")
        read_only_fields = ("uuid", "created_at", "updated_at")
