import os
import uuid

from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from djangoblog.utils import get_current_site


def avatar_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"avatars/{filename}"
# Create your models here.


class BlogUser(AbstractUser):
    nickname = models.CharField(_('nick name'), max_length=100, blank=True)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('last modify time'), default=now)
    source = models.CharField(_('create source'), max_length=100, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to=avatar_upload_to, blank=True, null=True)

    def save(self, *args, **kwargs):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import ContentFile

        # 保存前先记录旧的头像路径（用于之后判断是否删除旧文件）
        try:
            old_avatar = BlogUser.objects.get(pk=self.pk).avatar
        except BlogUser.DoesNotExist:
            old_avatar = None

        if self.avatar:
            # 打开上传的图片
            img = Image.open(self.avatar)
            # 转换为 RGB 模式（如果是 PNG 或其他格式）
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # 压缩图片
            img.thumbnail((300, 300))  # 设置最大尺寸为 300x300
            filename = os.path.basename(self.avatar.name)
            # 保存压缩后的图片到内存
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=85)  # 设置 JPEG 格式和质量
            buffer.seek(0)
            # 替换原始图片
            self.avatar = ContentFile(buffer.read(), name=f"avatars/{filename}")
        super().save(*args, **kwargs)

        # 删除旧的头像文件（前提是用户换了头像）
        if old_avatar and old_avatar != self.avatar and os.path.isfile(old_avatar.path):
            try:
                os.remove(old_avatar.path)
            except Exception:
                pass

        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def get_absolute_url(self):
        return reverse('blog:author_detail', kwargs={'author_name': self.username})

    def get_user_profile_url(self):
        return reverse('accounts:user_profile', kwargs={'username': self.username})

    def __str__(self):
        return self.email

    def get_full_url(self):
        site = get_current_site().domain
        url = "https://{site}{path}".format(site=site,
                                            path=self.get_absolute_url())
        return url

    class Meta:
        ordering = ['-id']
        verbose_name = _('user')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'
