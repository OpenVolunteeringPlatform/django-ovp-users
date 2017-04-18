from ovp_users.models.profile import get_profile_model
from ovp_users.models.profile import gender_choices
from ovp_users.helpers import get_settings, import_from_string

from ovp_core.models import Skill
from ovp_core.models import Cause
from ovp_core.serializers.skill import SkillSerializer, SkillAssociationSerializer
from ovp_core.serializers.cause import CauseSerializer, CauseAssociationSerializer

from rest_framework import serializers


class ProfileCreateUpdateSerializer(serializers.ModelSerializer):
  # we do not allow the user to create skills, only associate with
  # existing skills, so we do it manually on .create method
  skills = SkillAssociationSerializer(many=True, required=False)
  causes = CauseAssociationSerializer(many=True, required=False)
  gender = serializers.ChoiceField(choices=gender_choices)

  class Meta:
    model = get_profile_model()
    fields = ['full_name', 'about', 'skills', 'causes', 'gender']

  def create(self, validated_data):
    skills = validated_data.pop('skills', [])
    causes = validated_data.pop('causes', [])

    # Create profile
    profile = get_profile_model().objects.create(**validated_data)

    # Associate skills
    for skill in skills:
      s = Skill.objects.get(pk=skill['id'])
      profile.skills.add(s)

    # Associate causes
    for cause in causes:
      c = Cause.objects.get(pk=cause['id'])
      profile.causes.add(c)

    return profile


  def update(self, instance, validated_data):
    skills = validated_data.pop('skills', None)
    causes = validated_data.pop('causes', None)

    # Associate skills
    if skills:
      instance.skills.clear()
      for skill in skills:
        s = Skill.objects.get(pk=skill['id'])
        instance.skills.add(s)

    # Associate causes
    if causes:
      instance.causes.clear()
      for cause in causes:
        c = Cause.objects.get(pk=cause['id'])
        instance.causes.add(c)

    return super(ProfileCreateUpdateSerializer, self).update(instance, validated_data)

class ProfileRetrieveSerializer(serializers.ModelSerializer):
  skills = SkillSerializer(many=True)
  causes = CauseSerializer(many=True)
  gender = serializers.ChoiceField(choices=gender_choices)

  class Meta:
    model = get_profile_model()
    fields = ['full_name', 'about', 'skills', 'causes', 'gender']

class ProfileSearchSerializer(serializers.ModelSerializer):
  skills = SkillSerializer(many=True)
  causes = CauseSerializer(many=True)
  gender = serializers.ChoiceField(choices=gender_choices)

  class Meta:
    model = get_profile_model()
    fields = ['full_name', 'skills', 'causes', 'gender']


def get_profile_serializers():
  s = get_settings()
  serializers = s.get('PROFILE_SERIALIZER_TUPLE', None)
  if isinstance(serializers, tuple):
    return [import_from_string(s) for s in serializers]
  return (ProfileCreateUpdateSerializer, ProfileRetrieveSerializer, ProfileSearchSerializer)

