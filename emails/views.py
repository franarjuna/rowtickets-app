from django.views.generic import TemplateView

from emails.demo_email_contexts import contexts
# from relevant.frontend_urls import get_frontend_url


class EmailTemplateView(TemplateView):
    def get_template_names(self):
        return f'emails/{self.kwargs["template_name"]}.{"txt" if self.kwargs["template_type"] == "text" else "html"}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(contexts[self.kwargs['template_name']])

        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Set the proper content type for plain text & HTML
        """
        response_kwargs.setdefault(
            'content_type',
            'text/plain; charset=utf-8' if self.kwargs['template_type'] == 'text' else 'text/html'
        )

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )
