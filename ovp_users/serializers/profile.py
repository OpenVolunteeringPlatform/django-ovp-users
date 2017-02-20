from ovp_users import models

from ovp_core.serializers.skill import SkillSerializer

from rest_framework import serializers



class ProfileCreateSerializer(serializers.ModelSerializer):
  # we do not allow the user to create skills, only associate with
  # existing skills, so we do it manually on .create method
  skills = SkillAssociationSerializer(many=True)

  class Meta:
    model = models.UserProfile
    fields = ['full_name', 'skills', 'about']

  def create(self, validated_data):
    skills = validated_data.pop('skills', {})

    # Create profile
    profile = models.UserProfile.objects.create(**validated_data)

    # Associate skills
    for skill in skills:
      s = Skill.objects.get(pk=skill['id'])
      profile.skills.add(s)

    return profile

class ProfileRetrieveSerializer(serializers.ModelSerializer):
  skills = SkillSerializer()

  class Meta:
    model = models.UserProfile
    fields = ['full_name', 'skills', 'about']
