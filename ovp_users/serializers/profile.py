from ovp_users import models

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

  class Meta:
    model = models.UserProfile
    fields = ['full_name', 'about', 'public', 'skills', 'causes']

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

  class Meta:
    model = models.UserProfile
    fields = ['full_name', 'about', 'skills', 'public', 'causes']

class ProfileSearchSerializer(serializers.ModelSerializer):
  skills = SkillSerializer(many=True)
  causes = CauseSerializer(many=True)

  class Meta:
    model = models.UserProfile
    fields = ['full_name', 'skills', 'causes']
