from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.templatetags.static import static


def admin_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/avatar/<filename>
    return f'user_{instance.user.id}/avatar/{filename}'


class AdminProfile(models.Model):
    is_self_visible = models.BooleanField(default=False, null=True, blank=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, gettext("Erkak")),
        (GENDER_FEMALE, gettext("Ayol")),
    ]
    user = models.OneToOneField(User, related_name="admin_profile", on_delete=models.CASCADE)
    admin_avatar = models.ImageField(upload_to="static/admin/profiles/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        verbose_name = gettext('Profile')
        verbose_name_plural = gettext('Profiles')

    @property
    def get_admin_avatar(self):
        return self.admin_avatar.url if self.admin_avatar else static('admins/default-profile-picture.png')
 
    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Ushbu misolda allaqachon fayl borligini tekshiring
        try:
            this = AdminProfile.objects.get(id=self.id)
            # Agar fayl mavjud bo'lsa va yangi fayl bilan bir xil bo'lmasa, eski faylni o'chiring
            if this.admin_avatar and this.admin_avatar != self.admin_avatar:
                this.admin_avatar.delete(save=False)
        except AdminProfile.DoesNotExist:
            pass

        super(AdminProfile, self).save(*args, **kwargs)