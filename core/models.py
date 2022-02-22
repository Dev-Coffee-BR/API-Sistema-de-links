from django.db import models
from django.utils.translation import gettext as _
from user.models import User


class Category(models.Model):
    name = models.CharField(_("name"), max_length=50)
    created_in = models.DateTimeField(_("created in"), auto_now_add=True)


class Link(models.Model):
    url = models.URLField(_("url"))
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), max_length=200)
    creator = models.ForeignKey(
        User,
        verbose_name=_("created by"),
        on_delete=models.DO_NOTHING,
        related_name="links",
        blank=True,
        null=True,
    )
    created_in = models.DateTimeField(_("created in"), auto_now_add=True)
    expiration_date = models.DateTimeField(_("expiration date"), blank=True, null=True)
    soft_delet = models.DateTimeField(
        _("deleted"),
        blank=True,
        null=True,
        help_text=_("exclusion data the link if he has been excluded"),
    )


class FileType(models.Model):
    name = models.CharField(_("name"), max_length=50)
    created_in = models.DateTimeField(_("created in"), auto_now_add=True)


class File(models.Model):
    name = models.CharField(_("name"), max_length=50)
    description = models.TextField(_("description"), max_length=200)
    file = models.FileField(_("file"), upload_to="files/")
    creator = models.ForeignKey(
        User,
        verbose_name=_("created by"),
        on_delete=models.DO_NOTHING,
        related_name="files",
        blank=True,
        null=True,
    )
    created_in = models.DateTimeField(_("created in"), auto_now_add=True)
    soft_delet = models.DateTimeField(
        _("deleted"),
        blank=True,
        null=True,
        help_text=_("exclusion data the file if he has been excluded"),
    )
    file_type = models.ForeignKey(
        FileType,
        verbose_name=_("file type"),
        on_delete=models.DO_NOTHING,
        related_name="files",
        blank=True,
        null=True,
    )


class CategoryLink(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name=_("category"),
        on_delete=models.CASCADE,
        related_name="links",
    )
    link = models.ForeignKey(
        Link,
        verbose_name=_("link"),
        on_delete=models.CASCADE,
        related_name="categories",
    )
    created_in = models.DateTimeField(_("created in"), auto_now_add=True)


class CategoryFile(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name=_("category"),
        on_delete=models.CASCADE,
        related_name="files",
    )
    file = models.ForeignKey(
        File,
        verbose_name=_("file"),
        on_delete=models.CASCADE,
        related_name="categories",
    )
    created_in = models.DateTimeField(_("created in"), auto_now_add=True)
