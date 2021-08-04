import os
import tempfile

from PIL import Image

from django.contrib.auth.hashers import check_password
from django.core.files.images import ImageFile
from django.db.utils import IntegrityError
from django.test import TestCase

from photky.models import Photo, User

class PhotkyTestCase(TestCase):
    """Parent testing class containing global setup"""

    TEST_USER_PASSWORD="123456" # Testuser password

    def setUp(self):
        """Global test setup:
                - Create testing user "Test User <testuser@example.com>
        """
        User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            password=PhotkyTestCase.TEST_USER_PASSWORD
        )


class UserModelTestCase(PhotkyTestCase):
    """Testing class for User model."""

    def test_users_exist(self):
        """DB should contain at least one user stored during setup."""
        users = User.objects.all()
        self.assertTrue(users.count() > 0)

    def test_user_exists(self):
        """Tests whether testuser exists and testuser2 not."""
        user1 = User.objects.get(username="testuser")
        self.assertIsNotNone(user1) # Assuming testuser exists

        try:
            user2 = User.objects.get(username="testuser2")
        except User.DoesNotExist:
            user2 = None
        self.assertIsNone(user2) # Assuming testuser does not exist

    def test_user_password(self):
        """Password must be encrypted in the DB"""
        user1 = User.objects.get(username="testuser")

        self.assertNotEqual(PhotkyTestCase.TEST_USER_PASSWORD, user1.password)

        passCheck = check_password(PhotkyTestCase.TEST_USER_PASSWORD, user1.password)
        self.assertTrue(passCheck)


class PhotoModelTestCase(PhotkyTestCase):
    """Testing class for Photo model."""

    TEST_IMAGE_NAME="test.jpg"  # Test image filename

    def setUp(self):
        """Test setup:
            - Create temp image file.
            - Create Photo from the temp image.
        """
        super(PhotoModelTestCase, self).setUp()
        user = User.objects.first()

        self.img_fd, self.img_filename = tempfile.mkstemp()
        pilImg = Image.new("RGB", (640, 480))
        pilImg.save(self.img_filename, "JPEG")

        self.imageFile = ImageFile(open(self.img_filename, "rb"))
        self.imageFile.content_type = "image/jpeg"
        self.imageFile.name=PhotoModelTestCase.TEST_IMAGE_NAME
        Photo.objects.create(image=self.imageFile, owner=user)

    def tearDown(self):
        """Test teardown:
            - Close image file.
            - Close and delete temp file.
        """
        self.imageFile.close()
        os.close(self.img_fd)
        os.remove(self.img_filename)

    def test_photos_exist(self):
        """DB should contain at least one photo stored during setup."""
        photos = Photo.objects.all()
        self.assertTrue(photos.count() > 0)

    def test_photo_exists(self):
        """Tests whether test image exists and 123456789.jpg not."""
        photo1 = Photo.objects.get(filename=PhotoModelTestCase.TEST_IMAGE_NAME)
        self.assertIsNotNone(photo1) # Assuming test image exists in the DB

        try:
            photo2 = Photo.objects.get(filename="123456789.jpg")
        except Photo.DoesNotExist:
            photo2 = None
        self.assertIsNone(photo2) # Assuming image 123456789.jpg does not exist in the DB

    def test_create_no_owner(self):
        """Photo must be created with the user owner specified."""
        try:
            photo = Photo.objects.create(image=self.imageFile)
        except IntegrityError:
            photo = None
        self.assertIsNone(photo)

    def test_thumbnail_exists(self):
        """Each Photo must contain thumbnail created when Photo saved."""
        photo = Photo.objects.first()
        self.assertIsNotNone(photo.thumbnail)
        # Check whether the thumbnail has resolution > 0
        pilImageThumb = Image.open(photo.thumbnail)
        self.assertGreater(pilImageThumb.width, 0)
        self.assertGreater(pilImageThumb.height, 0)