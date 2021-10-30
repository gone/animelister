from django.core.exceptions import ImproperlyConfigured
from django.views.generic import FormView, UpdateView
from django.views.generic.base import TemplateResponseMixin, TemplateView


class HtmxTemplateResponseMixin(TemplateResponseMixin):
    htmx_template_name = None

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response() is overridden.
        """
        super().get_template_names()

        if self.template_name is None or self.htmx_template_name is None:
            raise ImproperlyConfigured(
                "HtmxTemplateResponseMixin requires either a definition of "
                "'htmx_template_name' and 'template_name' or an "
                "implementation of 'get_template_names()'"
            )

        if self.request.htmx and not self.request.htmx.boosted:
            return [self.htmx_template_name]

        return [self.template_name]


class HtmxTemplateView(HtmxTemplateResponseMixin, TemplateView):
    """A view for rendering a htmx or regular template response"""


class HtmxFormView(HtmxTemplateResponseMixin, FormView):
    """
    A view for displaying a form and rendering
    a htmx or regular template response.
    """


class HtmxUpdateView(HtmxTemplateResponseMixin, UpdateView):
    """
    A view for displaying a form and rendering
    a htmx or regular template response to update models
    """
