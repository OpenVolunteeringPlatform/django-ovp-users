from ovp_users import models

from ovp_core.models import Skill
from ovp_core.models import Cause
from ovp_core.serializers.skill import SkillSerializer, SkillAssociationSerializer
from ovp_core.serializers.cause import CauseSerializer, CauseAssociationSerializer

from rest_framework import serializers


class ProfileCreateSerializer(serializers.ModelSerializer):
  # we do not allow the user to create skills, only associate with
  # existing skills, so we do it manually on .create method
  skills = SkillAssociationSerializer(many=True)
  causes = CauseAssociationSerializer(many=True)

  class Meta:
    model = models.UserProfile
    fields = ['full_name', 'about', 'skills', 'causes']

  def create(self, validated_data):
    skills = validated_data.pop('skills', [])
    causes = validated_data.pop('causes', [])

    # Create profile
    profile = models.UserProfile.objects.create(**validated_data)

    # Associate skills
    for skill in skills:
      s = Skill.objects.get(pk=skill['id'])
      profile.skills.add(s)

    # Associate causes
    for cause in causes:
      c = Cause.objects.get(pk=cause['id'])
      profile.causes.add(c)

    return profile

class ProfileRetrieveSerializer(serializers.ModelSerializer):
  skills = SkillSerializer(many=True)
  causes = CauseSerializer(many=True)

  class Meta:
    model = models.UserProfile
    fields = ['full_name', 'about', 'skills', 'causes']
