from django.db import models  # NOQA
from django_extensions.db.models import AutoSlugField  # NOQA
from model_utils.models import TimeStampedModel  # NOQA

from animelister.user.models import User
from django.utils.translation import gettext_lazy as _

from django.urls import reverse

from taggit.managers import TaggableManager

# Create your models here.


class TypeChoices(models.TextChoices):
    TV = "TV", _("TV")
    MOVIE = "MOVIE", _("Movie")


class StatusChoices(models.TextChoices):
    AIRING = "AIRING", "Currently Aring"
    FINISHED = "FINISHED", "Finished Airing"


class UserRating(TimeStampedModel):
    rating = models.IntegerField()
    anime = models.ForeignKey("Anime", on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")

    def __str__(self):
        return f"{self.user} - {self.anime} - {self.rating}"


class AnimeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(avg_rating=models.Avg("ratings__rating"))


class Anime(TimeStampedModel):
    name = models.CharField("anime's name", max_length=255)
    slug = AutoSlugField(populate_from=["name"])
    poster = models.ImageField(blank=True)
    type = models.CharField(
        "where did the anime air", choices=TypeChoices.choices, max_length=255
    )
    status = models.CharField(
        "current status of anime", choices=StatusChoices.choices, max_length=255
    )
    aired = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    genre = TaggableManager()
    seiyuu = models.ManyToManyField("Seiyuu", blank=True, related_name="anime",)
    studio = models.ManyToManyField("Studio", blank=True, related_name="anime")
    description = models.TextField()
    season = models.CharField("Season the anime aried in", max_length=255)

    users = models.ManyToManyField(User, through=UserRating, related_name="animes")

    objects = AnimeManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("anime-detail", kwargs={"slug": self.slug})


class Studio(TimeStampedModel):
    name = models.CharField("Name", max_length=255)

    def __str__(self):
        return self.name


class Seiyuu(TimeStampedModel):
    name = models.CharField("Name", max_length=255)

    def __str__(self):
        return self.name
