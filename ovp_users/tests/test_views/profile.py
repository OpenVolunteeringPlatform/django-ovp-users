from django.test import TestCase

from ovp_users.tests.helpers import create_user_with_profile

class ProfileTestCase(TestCase):
  def setUp(self):
    self.profile = {
      'full_name': 'Test User',
      'skills': [{'id': 1}, {'id': 2, 'name': 'test'}],
      'about': 'I\'m a test user and that\'s all you must know about me',
    }

  def test_can_create_user_with_profile(self):
    """ Assert profile data gets saved when creating user """
    response = create_user_with_profile(profile=self.profile)
    self.assertTrue(response.data['profile']['full_name'] == 'Test User')
    self.assertTrue(response.data['profile']['about'] == 'I\'m a test user and that\'s all you must know about me')

    self.assertTrue(response.data['profile']['skills'][0]['id'] == 1)
    self.assertTrue('name' in response.data['profile']['skills'][0])

    self.assertTrue(response.data['profile']['skills'][1]['id'] == 2)
    self.assertTrue('name' in response.data['profile']['skills'][1])

  def test_skills_validation(self):
    """ Assert it's impossible to associate with invalid skills """
    profile = self.profile
    profile['skills'] = [{'id': 999}, {'id': 998}]
    response = create_user_with_profile(profile=profile)
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.data['profile']['skills'][0]['id'] == ["Skill with 'id' 999 does not exist."])
    self.assertTrue(response.data['profile']['skills'][1]['id'] == ["Skill with 'id' 998 does not exist."])


  def test_current_user_route_returns_profile(self):
    """ Assert profile data gets returned when fetching current user """
    pass
