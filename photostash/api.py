from tastypie.api import Api

from photostash.photos.api import AlbumResource, PhotoResource, AlbumPhotoResource


v1 = Api(api_name='v1')
v1.register(AlbumResource())
v1.register(PhotoResource())
v1.register(AlbumPhotoResource())
