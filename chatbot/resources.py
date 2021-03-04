from import_export import resources
from .models import Gym,Recipe,User,Record

# class FoodResource(resources.ModelResource):
#     class Meta:
#         model =Food
#         skip_unchanged = True
#         report_skipped = True
#         exclude = ('id')
#         import_id_fields = ('edx_id')

class GymResource(resources.ModelResource):
    class Meta:
        model =Gym
        skip_unchanged = True
        report_skipped = True
        exclude = ('id')
        import_id_fields = ('edx_id')


class RecipeResource(resources.ModelResource):
    class Meta:
        model =Recipe
        skip_unchanged = True
        report_skipped = True
        exclude = ('id')
        import_id_fields = ('edx_id')

class UserResource(resources.ModelResource):
    class Meta:
        model=User


class RecordResource(resources.ModelResource):
    class Meta:
        model=Record


