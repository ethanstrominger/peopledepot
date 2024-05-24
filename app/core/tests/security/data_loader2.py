import copy
from core.models import PermissionAssignment, PermissionType, Project, User
from core.tests.util.seed_constants import (website_project, people_depot_project, wanda_name, wally_name, winona_name, zani_name, patti_name, patrick_name, garry_name, valerie_name, descriptions)
from core.constants import (project_lead, project_team_member, global_admin, verified_user)
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class UserData2:   
    data_loaded = False
    users = {}
    wally_user = None
    wanda_user = None
    winona_user = None
    zani_user = None
    patti_user = None
    patrick_user = None

    @classmethod
    def get_user(cls, first_name):
        print("Debug get_user", first_name, cls.users, cls.users.get(first_name))
        return cls.users.get(first_name)

    @classmethod
    def create_user(cls, *, first_name: str, description: str):
        last_name = f"{description}"
        email = f"{first_name}{description}@example.com"
        username = email

        print("Creating user", first_name)
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email   
        )
        cls.users[first_name] = user
        print("Debug create user", first_name, cls.users)
        user.save()
        return user
        
    @classmethod
    def create_related_data(cls, *, user=None, permission_type_name=None, project_name=None):
        print("Debug create related data", permission_type_name, project_name)
        print(PermissionType.objects.all())
        for permission_type in PermissionType.objects.all():
            print("Debug permission type", permission_type.name)
        permission_type = PermissionType.objects.get(name=permission_type_name)
        if project_name:
            project_data = { "project":  Project.objects.get(name=project_name)}
        else:
            project_data = {}
        user_permission = PermissionAssignment.objects.create(user=user, permission_type=permission_type, **project_data)
        print("Created user permission", user_permission)
        user_permission.save()
        return user_permission
    
    @classmethod
    def load_data(cls):
        projects = [website_project, people_depot_project]
        for project_name in projects:
            project = Project.objects.create(name=project_name)
            project.save()
            
        user_names = [wanda_name, wally_name, winona_name, zani_name, patti_name, patrick_name, garry_name, valerie_name]
        x = 0
        for name in user_names:
            x += 1
            print("Debug about to call create user", name, descriptions[name])
            cls.create_user(first_name=name, description=descriptions[name])
            
        related_data = [
            {"first_name": wanda_name, "project_name": website_project, "permission_type_name": project_lead},
            {"first_name": wally_name, "project_name": website_project, "permission_type_name": project_team_member},
            {"first_name": winona_name, "project_name": website_project, "permission_type_name": project_team_member},
            {"first_name": zani_name, "project_name": people_depot_project, "permission_type_name": project_team_member},
            {"first_name": patti_name, "project_name": people_depot_project, "permission_type_name": project_team_member},
            {"first_name": patrick_name, "project_name": people_depot_project, "permission_type_name": project_lead},
            {"first_name": garry_name, "permission_type_name": global_admin},
            {"first_name": valerie_name, "permission_type_name": verified_user},
            {"first_name": zani_name, "project_name": website_project, "permission_type_name": project_lead},
        ]

        for data in related_data:
            user = cls.get_user(data["first_name"])
            params = copy.deepcopy(data)
            del params["first_name"]
            cls.create_related_data (user=user, **params)
        
        for user in User.objects.all():
            print("debug userx", user.first_name)        

    @classmethod
    def initialize_data(cls):
        print("Initializing data")
        cls.load_data()
        cls.wally_user = cls.get_user(wally_name)
        cls.wanda_user = cls.get_user(wanda_name)
        cls.winona_user = cls.get_user(winona_name)
        cls.zani_user = cls.get_user(zani_name)
        cls.patti_user = cls.get_user(patti_name)
        cls.patrick_user = cls.get_user(patrick_name)
        cls.garry_user = cls.get_user(garry_name)
        cls.valerie_user = cls.get_user(valerie_name)
