from urlparse import urlparse

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import simplejson

from photostash.photos.models import Album, Photo, AlbumPhoto


class ApiTestCase(TestCase):

    def list_url(self, resource_name=None):
        resource_name = resource_name or self.resource_name
        kwargs = {'api_name': 'v1', 'resource_name': resource_name}
        return reverse('api_dispatch_list', kwargs=kwargs)

    def detail_url(self, obj, resource_name=None):
        resource_name = resource_name or self.resource_name
        kwargs = {'api_name': 'v1', 'resource_name': resource_name, 'pk': obj.pk}
        return reverse('api_dispatch_detail', kwargs=kwargs)

    def list(self, **kwargs):
        return self.client.get(self.list_url(), kwargs, 'application/json')

    def create(self, **kwargs):
        data = simplejson.dumps(kwargs)
        return self.client.post(self.list_url(), data, 'application/json')

    def read(self, obj, **kwargs):
        return self.client.get(self.detail_url(obj), kwargs, 'application/json')

    def update(self, obj, **kwargs):
        data = simplejson.dumps(kwargs)
        return self.client.put(self.detail_url(obj), data, 'application/json')

    def delete(self, obj):
        return self.client.delete(self.detail_url(obj), {}, 'application/json')

    def assertLocation(self, response, obj):
        path = urlparse(response['location']).path
        self.assertEqual(path, self.detail_url(obj))

    def assertJSONEqual(self, response, expected, keyfunc=None):
        actual = simplejson.loads(response.content)
        if keyfunc is not None:
            actual = keyfunc(actual)
        self.assertEqual(actual, expected)


class AlbumApiTestCase(ApiTestCase):
    resource_name = 'albums'

    def to_dict(self, obj):
        return {
            'id': unicode(obj.pk),
            'name': obj.name,
            'resource_uri': self.detail_url(obj),
        }

    def test_create(self):
        response = self.create(name='album')
        album = Album.objects.all()[0]
        self.assertEqual(response.status_code, 201)
        self.assertLocation(response, album)
        self.assertJSONEqual(response, self.to_dict(album))

    def test_list(self):
        album1 = Album.objects.create(name='one')
        album2 = Album.objects.create(name='two')
        albums = [self.to_dict(album1), self.to_dict(album2)]
        response = self.list()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response, albums, lambda x: x['objects'])

    def test_read(self):
        album = Album.objects.create(name='album')
        response = self.read(album)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response, self.to_dict(album))

    def test_update(self):
        album = Album.objects.create(name='album')
        response = self.update(album, name='new name')
        updated = Album.objects.get(pk=album.pk)
        self.assertEqual(response.status_code, 202)
        self.assertJSONEqual(response, self.to_dict(updated))

    def test_delete(self):
        album = Album.objects.create(name='album')
        response = self.delete(album)
        self.assertEqual(response.status_code, 204)
        self.assertRaises(Album.DoesNotExist, Album.objects.get, pk=album.pk)


class PhotoApiTestCase(ApiTestCase):
    resource_name = 'photos'

    def to_dict(self, obj):
        return {
            'id': unicode(obj.pk),
            'image': obj.image.url,
            'resource_uri': self.detail_url(obj),
            'albumphotos': [],
        }

    def test_create(self):
        response = self.create(image='photo.jpg:MQ==')
        photo = Photo.objects.all()[0]
        self.assertEqual(response.status_code, 201)
        self.assertLocation(response, photo)
        self.assertJSONEqual(response, self.to_dict(photo))

    def test_list(self):
        photo1 = Photo.objects.create(image='one')
        photo2 = Photo.objects.create(image='two')
        photos = [self.to_dict(photo1), self.to_dict(photo2)]
        response = self.list()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response, photos, lambda x: x['objects'])

    def test_list_by_album(self):
        album1 = Album.objects.create(name='album1')
        photo1 = Photo.objects.create(image='photo1')
        AlbumPhoto.objects.create(photo=photo1, album=album1)
        album2 = Album.objects.create(name='album2')
        photo2 = Photo.objects.create(image='photo2')
        AlbumPhoto.objects.create(photo=photo2, album=album2)
        response = self.list(albumphotos__album=album1.pk)
        objects = simplejson.loads(response.content)['objects']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(objects), 1)
        self.assertJSONEqual(
            response,
            photo1.image.url,
            lambda x: x['objects'][0]['image']
        )

    def test_read(self):
        photo = Photo.objects.create(image='photo')
        response = self.read(photo)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response, self.to_dict(photo))

    def test_delete(self):
        photo = Photo.objects.create(image='photo')
        response = self.delete(photo)
        self.assertEqual(response.status_code, 204)
        self.assertRaises(Photo.DoesNotExist, Photo.objects.get, pk=photo.pk)


class AlbumPhotoApiTestCase(ApiTestCase):
    resource_name = 'albumphotos'

    def to_dict(self, obj):
        return {
            'id': unicode(obj.pk),
            'album': self.detail_url(obj.album, 'albums'),
            'photo': self.detail_url(obj.photo, 'photos'),
            'resource_uri': self.detail_url(obj),
        }

    def test_create(self):
        album = Album.objects.create(name='album')
        photo = Photo.objects.create(image='photo')
        response = self.create(
            album=self.detail_url(album, 'albums'),
            photo=self.detail_url(photo, 'photos'),
        )
        album_photo = AlbumPhoto.objects.all()[0]
        self.assertEqual(response.status_code, 201)
        self.assertLocation(response, album_photo)
        self.assertJSONEqual(response, self.to_dict(album_photo))

    def test_list(self):
        album = Album.objects.create(name='album')
        photo1 = Photo.objects.create(image='one')
        photo2 = Photo.objects.create(image='two')
        album_photo1 = AlbumPhoto.objects.create(photo=photo1, album=album)
        album_photo2 = AlbumPhoto.objects.create(photo=photo2, album=album)
        album_photos = [self.to_dict(album_photo1), self.to_dict(album_photo2)]
        response = self.list()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response, album_photos, lambda x: x['objects'])

    def test_list_by_album_and_photo(self):
        album1 = Album.objects.create(name='album1')
        photo1 = Photo.objects.create(image='photo1')
        album2 = Album.objects.create(name='album2')
        photo2 = Photo.objects.create(image='photo2')
        AlbumPhoto.objects.create(photo=photo1, album=album1)
        response = self.list(album=album1.pk, photo=photo1.pk)
        objects = simplejson.loads(response.content)['objects']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(objects), 1)

    def test_read(self):
        album = Album.objects.create(name='album')
        photo = Photo.objects.create(image='photo')
        album_photo = AlbumPhoto.objects.create(photo=photo, album=album)
        response = self.read(album_photo)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response, self.to_dict(album_photo))

    def test_delete(self):
        album = Album.objects.create(name='album')
        photo = Photo.objects.create(image='photo')
        album_photo = AlbumPhoto.objects.create(photo=photo, album=album)
        response = self.delete(album_photo)
        self.assertEqual(response.status_code, 204)
        self.assertRaises(AlbumPhoto.DoesNotExist, AlbumPhoto.objects.get, pk=album_photo.pk)
