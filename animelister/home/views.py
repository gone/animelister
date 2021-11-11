# Create your views here.

# from django.views.generic.base import TemplateView
# from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from annoying.functions import get_object_or_None
from django.urls import reverse_lazy
from django.contrib import messages

from django.db.models import F
from django.shortcuts import get_object_or_404

# from django.utils.decorators import method_decorator

# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.views.generic.detail import DetailView

from django_htmx.http import HttpResponseClientRedirect


from .models import Anime, UserRating
from .forms import UserRatingForm, AnimeForm
from django.views.generic import ListView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from animelister.util.views import HtmxTemplateResponseMixin
from django.views.generic.edit import DeletionMixin


def error(request):
    """Generate an exception. Useful for e.g. configuing Sentry"""
    raise Exception("Make response code 500!")


class HomeView(ListView, HtmxTemplateResponseMixin):
    model = Anime
    context_object_name = "animes"
    template_name = "home/index.html"
    htmx_template_name = "home/partials/anime_table.html"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        sort, search, reverse = (
            self.request.GET.get("sort"),
            self.request.GET.get("search"),
            self.request.GET.get("reverse"),
        )
        if search:
            qs = qs.filter(name__icontains=search)
        if sort:
            if sort.startswith("-"):
                query = F(sort[1:]).desc(nulls_last=True)
            else:
                query = F(sort).asc(nulls_last=True)
            qs = qs.order_by(query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        page_obj = context["page_obj"]
        if not page_obj.has_next():
            context["next_page_qs"] = ""
        else:
            next_page = page_obj.next_page_number()
            newget = self.request.GET.copy()
            newget["page"] = next_page
            context["next_page_qs"] = newget.urlencode()
        context["table_headers"] = {
            "id": "ID",
            "name": "Name",
            "avg_rating": "Avg. Rating",
            "status": "Status",
            "season": "Season",
            "genre": "Genre",
        }
        # messages.info(self.request, 'Test Message for home view')

        return context


class FixedHomeView(HomeView):
    template_name = "home/index_fixed.html"


class AnimeDetailView(DetailView):
    model = Anime

    def get_context_data(self, object):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            rating = get_object_or_None(
                UserRating, user=self.request.user, anime=object
            )
            context["userrating"] = rating = rating or UserRating(
                user=self.request.user, anime=object
            )
            context["form"] = UserRatingForm(instance=rating)
        return context


class AnimeWrite(UpdateView, HtmxTemplateResponseMixin):
    template_name = "home/anime_update.html"
    htmx_template_name = "home/partials/anime_form.html"
    model = Anime
    form_class = AnimeForm

    def get_object(self):
        self.anime = get_object_or_None(Anime, slug=self.kwargs.get("slug"))
        return self.anime or Anime()

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        return HttpResponseClientRedirect(self.get_success_url())


class UserRatingView(UpdateView):
    template_name = "home/partials/user_rating_form.html"
    model = UserRating
    form_class = UserRatingForm

    # push back to self for post and delete to get new form instance to add into dom
    def get_success_url(self):
        return reverse_lazy("rate-anime", kwargs={"slug": self.anime.slug})

    # because this is a m2m through table, get both sides of the relationship explicity
    # so that we can populate them in our form
    # ****IMPORTANT**** return an object no matter what so this form acts identically for get and create
    # you might not want that behavior all the time but it's useful
    def get_object(self):
        self.anime = get_object_or_404(Anime, slug=self.kwargs.get("slug"))
        obj = get_object_or_None(UserRating, user=self.request.user, anime=self.anime)
        return obj or UserRating(user=self.request.user, anime=self.anime)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["anime"] = self.anime
        return context

    def form_valid(self, form):
        messages.info(self.request, "added to your list")
        return super().form_valid(form)

    # TODO; this is copy pasted from django source, do this with subclassing
    # althogh the 303 bug is annoying - if you redirct to the same location
    # and do so with a 302 it will just keep trying to delete vs switching to GET
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.info(self.request, "Removed from your list")
        return HttpResponseRedirect(success_url, status=303)


@login_required
def dashboard(request):
    context = {}
    context["animes"] = request.user.animes.all()
    return render(request, "home/dashboard.html", context)
