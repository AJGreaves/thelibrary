from django.contrib.auth.models import User
from django.test import TestCase
from .models import UserProfile
from posts.models import PostTag, PostCategory, Post
import datetime


class UserProfileTestCase(TestCase):
    def setUp(self):
        user_a = User(username="testUsername", email="test@email.com")
        user_a.set_password('testing321')
        user_a.save()

    def test_userprofile_created_with_new_user(self):
        user_a = User.objects.get(pk=1)
        profile = UserProfile.objects.get(pk=1)
        self.assertEqual(profile.user, user_a)
    
    def test_userprofile_bio_blank_by_default(self):
        profile = UserProfile.objects.get(pk=1)
        self.assertIsNone(profile.bio)

    def test_set_userprofile_bio_value(self):
        profile = UserProfile.objects.get(pk=1)
        profile.bio = 'Test bio'
        self.assertEqual(profile.bio, 'Test bio')

    def test_userprofile_is_admin_value_set_to_false_by_default(self):
        profile = UserProfile.objects.get(pk=1)
        self.assertFalse(profile.is_admin)

    def test_set_userprofile_is_admin_value(self):
        profile = UserProfile.objects.get(pk=1)
        profile.is_admin = True
        self.assertTrue(profile.is_admin)

    def test_userprofile_is_mod_value_set_to_false_by_default(self):
        profile = UserProfile.objects.get(pk=1)
        self.assertFalse(profile.is_mod)

    def test_set_userprofile_is_mod_value(self):
        profile = UserProfile.objects.get(pk=1)
        profile.is_mod = True
        self.assertTrue(profile.is_mod)

    def test_userprofile_is_staff_value_set_to_false_by_default(self):
        profile = UserProfile.objects.get(pk=1)
        self.assertFalse(profile.is_staff)

    def test_set_userprofile_is_staff_value(self):
        profile = UserProfile.objects.get(pk=1)
        profile.is_staff = True
        self.assertTrue(profile.is_staff)

    def test_userprofile_date_joined(self):
        profile = UserProfile.objects.get(pk=1)
        self.assertEqual(profile.date_joined, datetime.date.today())

    def test_userprofile_linkedin_blank_by_default(self):
        profile = UserProfile.objects.get(pk=1)
        self.assertIsNone(profile.linkedin)

    def test_set_userprofile_linkedin_value(self):
        profile = UserProfile.objects.get(pk=1)
        profile.linkedin = 'http://linkedin.com/in/test/'
        self.assertEqual(profile.linkedin, 'http://linkedin.com/in/test/')

    def test_userprofile_github_blank_by_default(self):
        profile = UserProfile.objects.get(pk=1)
        self.assertIsNone(profile.github)

    def test_set_userprofile_github_value(self):
        profile = UserProfile.objects.get(pk=1)
        profile.github = 'https://github.com/test'
        self.assertEqual(profile.github, 'https://github.com/test')

    def test_userprofile_dunder_string_with_defaults(self):
        profile = UserProfile.objects.get(pk=1)
        today = datetime.date.today()
        self.assertEqual(
            str(profile), f"testUsername | {today}"
        )

    def test_userprofile_dunder_string_with_admin_and_mod_true(self):
        profile = UserProfile.objects.get(pk=1)
        profile.is_admin = True
        profile.is_mod = True
        profile.save()
        today = datetime.date.today()
        self.assertEqual(
            str(profile), f"testUsername *admin | {today}"
        )

    def test_userprofile_dunder_string_with_admin_false_and_mod_true(self):
        profile = UserProfile.objects.get(pk=1)
        profile.is_mod = True
        profile.save()
        today = datetime.date.today()
        self.assertEqual(
            str(profile), f"testUsername *mod | {today}"
        )

    def test_default_profile_pic_created(self):
        profile = UserProfile.objects.get(pk=1)
        expected = '/media/images/profiles/default-profile-pic.png'
        self.assertEqual(profile.profile_pic.url, expected)


class GetAuthorNameMethodTestCase(TestCase):
    def setUp(self):
        user = User(username="testUsername", email="test@email.com")
        user.set_password('testing321')
        user.save()

    def test_first_name_does_not_exist(self):
        user = User.objects.get(pk=1)
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')

    def test_get_author_name_when_only_username_exists(self):
        user = User.objects.get(pk=1)
        expected = "testUsername"
        result = user.userprofile.get_author_name()
        self.assertEqual(result, expected)

    def test_get_author_name_when_only_first_name_exists(self):
        user = User.objects.get(pk=1)
        user.first_name = 'Arthur'
        user.save()

        expected = "testUsername"
        result = user.userprofile.get_author_name()
        self.assertEqual(result, expected)

    def test_get_author_name_when_first_and_last_names_exist(self):
        user = User.objects.get(pk=1)
        user.first_name = 'Arthur'
        user.last_name = 'Dent'
        user.save()

        expected = "Arthur Dent"
        result = user.userprofile.get_author_name()
        self.assertEqual(result, expected)
