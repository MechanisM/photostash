from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from photostash.photos.models import Album, Photo, AlbumPhoto


class AlbumPhotoTestCase(TestCase):

    def test_deleting_removes_photo_when_no_one_else_using_it(self):
        album = Album.objects.create(name='album')
        photo = Photo.objects.create(image='photo')
        album_photo = AlbumPhoto.objects.create(photo=photo, album=album)
        album_photo.delete()
        self.assertRaises(Photo.DoesNotExist, Photo.objects.get, pk=photo.pk)


class PhotoTestCase(TestCase):

    def test_deleting_removes_image_file(self):
        image = SimpleUploadedFile('photo.jpg', 'content', 'image/jpg')
        photo = Photo()
        photo.image.save('photo.jpg', image, save=True)
        storage, path = photo.image.storage, photo.image.path
        photo.delete()
        self.assertFalse(storage.exists(path))
