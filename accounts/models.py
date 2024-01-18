from PIL import Image
from datetime import datetime
import hashlib
from django.utils.crypto import get_random_string
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


def create_id():
    return get_random_string(10)


def _user_profile_avatar_upload_to(instance, filename):
    current_time = datetime.now()
    pre_hash_name = '%s%s%s' % (instance.id, filename, current_time)
    extension = str(filename).split('.')[-1]
    hs_filename = '%s.%s' % (hashlib.md5(
        pre_hash_name.encode()).hexdigest(), extension)
    saved_path = 'Users/ProfileImages/'
    return '%s%s' % (saved_path, hs_filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('メールアドレス', unique=True, null=False)
    first_name = models.CharField("姓", max_length=30, null=False)
    last_name = models.CharField("名", max_length=30, null=False)
    call_name = models.CharField("呼び名", max_length=100, blank=True, null=True)
    nick_name = models.CharField("ニックネーム", max_length=30, blank=True, null=True)
    user_screen_id = models.SlugField("ユーザーID", max_length=30, unique=True, default=create_id, null=False)
    year = models.DateTimeField("生年月日", blank=True, null=True, default=datetime.strftime(timezone.now(), '%Y-%m-%d'))
    course = models.CharField("コース", max_length=30, blank=True, null=True)
    city = models.CharField("住所", max_length=30, blank=True, null=True)
    tel = models.CharField("電話番号", max_length=30, blank=True, null=True)
    job = models.CharField("職業", max_length=30, blank=True, null=True)
    text = models.TextField("PR文章", blank=True, null=True)
    created = models.DateTimeField("入会日", default=timezone.now)
    banner = models.ImageField("バナー画像", upload_to=_user_profile_avatar_upload_to, default='Users/default.jpg', blank=True, null=True)
    avatar = models.ImageField("プロフィール画像", upload_to=_user_profile_avatar_upload_to, default='Users/default.jpg', blank=True, null=True)
    read_terms = models.BooleanField("利用規約同意", default=False, blank=False, null=False)

    is_staff = models.BooleanField(
        ("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ("ユーザー")
        verbose_name_plural = ("ユーザー")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


def certificationImage(instance, filename):
    current_time = datetime.now()
    pre_hash_name = '%s%s%s' % (instance.id, filename, current_time)
    extension = str(filename).split('.')[-1]
    hs_filename = '%s.%s' % (hashlib.md5(
        pre_hash_name.encode()).hexdigest(), extension)
    saved_path = 'Users/Certification/'
    return '%s%s' % (saved_path, hs_filename)

class Certification(models.Model):
    orderby = models.IntegerField("順番")
    name = models.CharField("資格名", max_length=100, null=False)
    date = models.DateTimeField("取得日", default=timezone.now)
    image = models.ImageField("画像", upload_to=certificationImage, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.date}"

    class Meta:
        verbose_name = ("資格情報")
        verbose_name_plural = ("資格情報")

class Skill(models.Model):
    orderby = models.IntegerField("順番")
    name = models.CharField('名前', max_length=20)
    year = models.IntegerField('年数')

    def __str__(self):
        return f'{self.name} | {self.year}'
    
    class Meta:
        verbose_name = "スキル一覧"
        verbose_name_plural = "スキル一覧"

class Reward(models.Model):
    orderby = models.IntegerField("順番")
    name = models.CharField('名前', max_length=20)
    date = models.DateTimeField("取得日", default=timezone.now)

    def __str__(self):
        return f'{self.name} | {self.date}'
    
    class Meta:
        verbose_name = "賞罰一覧"
        verbose_name_plural = "賞罰一覧"



class Post_Inquiry(models.Model):
    email = models.EmailField('メールアドレス', blank=False, null=False)
    first_name = models.CharField("姓", max_length=30,
                                    blank=False,
                                    null=False
                                    )
    last_name = models.CharField("名", max_length=30,
                                    blank=False,
                                    null=False
                                    )
    title = models.CharField("件名", max_length=100,
                                blank=False,
                                null=False
                                )
    summary = models.TextField(
        "お問い合わせ内容",
        blank=False,
        null=False)
    complete = models.BooleanField("対応済み", default=False)
    created = models.DateTimeField("お問い合わせ日", default=timezone.now)
    read_field = models.BooleanField("お問い合わせ送信確認", default=False, blank=False, null=False)
    
    def __str__(self):
        return f"名前: {self.first_name} {self.last_name} 件名: {self.title}"

    class Meta:
        verbose_name = ("お問い合わせ一覧")
        verbose_name_plural = ("お問い合わせ一覧")

