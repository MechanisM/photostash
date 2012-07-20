from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Photo(models.Model):
    image = models.ImageField(_('image'), upload_to='photos')

    def delete(self):
        # Removing files like this is not really recommended. Its
        # better to have a background process removed unused files.
        self.image.delete()
        super(Photo, self).delete()


class Album(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=64, validators=[RegexValidator(r'^[\w-]+$')])


class AlbumPhoto(models.Model):
    photo = models.ForeignKey(Photo, verbose_name=_('photo'), related_name='albums')
    album = models.ForeignKey(Album, verbose_name=_('album'), related_name='photos')

    class Meta(object):
        unique_together = ['photo', 'album']

    def delete(self):
        if self.__class__._default_manager.filter(photo=self.photo).count() <= 1:
            self.photo.delete()
        super(AlbumPhoto, self).delete()
