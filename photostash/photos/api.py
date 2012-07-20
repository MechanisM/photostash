import base64

from django.core.files.uploadedfile import SimpleUploadedFile

from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

from photostash.photos.models import Album, Photo, AlbumPhoto


class BaseModelResource(ModelResource):

    def obj_update(self, bundle, request=None, **kwargs):
        bundle = super(BaseModelResource, self).obj_update(bundle, request, **kwargs)
        # For some reason Tasypie likes to return the pk in the bundle we
        # dont want it because the create call doesn't do it and we want
        # them to match
        if 'pk' not in self._meta.fields:
            del bundle.data['pk']
        return bundle

    def build_schema(self):
        schema = super(BaseModelResource, self).build_schema()
        schema['fields'] = self._patch_type(schema['fields'])
        return schema

    def _patch_type(self, schema_fields):
        # The client needs the old 'related_type' attr to still be supported.
        related_types = {
            fields.ToOneField: 'to_one',
            fields.ToManyField: 'to_many',
        }
        patched_fields = {}
        for name, options in schema_fields.iteritems():
            if options['type'] == 'related':
                options['related_type'] = related_types[self.fields[name].__class__]
            patched_fields[name] = options
        return patched_fields


class PhotoResource(BaseModelResource):
    albumphotos = fields.ToManyField('photostash.photos.api.AlbumPhotoResource', 'albums', null=True)

    class Meta(object):
        queryset = Photo.objects.all()
        resource_name = 'photos'
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {'id': ['exact'], 'albumphotos': ALL_WITH_RELATIONS}

    def hydrate(self, bundle):
        name, content = bundle.data['image'].split(':')
        bundle.data['image'] = SimpleUploadedFile(
            name,
            base64.b64decode(content),
            'application/octet-stream',
        )
        return bundle


class AlbumResource(BaseModelResource):

    class Meta(object):
        queryset = Album.objects.all()
        resource_name = 'albums'
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {'id': ['exact'], 'name': ['exact']}


class AlbumPhotoResource(BaseModelResource):
    photo = fields.ToOneField(PhotoResource, 'photo')
    album = fields.ToOneField(AlbumResource, 'album')

    class Meta(object):
        queryset = AlbumPhoto.objects.all()
        resource_name = 'albumphotos'
        authentication = Authentication()
        authorization = Authorization()
        always_return_data = True
        filtering = {'album': ALL, 'photo': ALL}
