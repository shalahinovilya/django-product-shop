from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from django.views.generic.list import MultipleObjectMixin

bar_left = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Про нас', 'url_name': 'about'},
]


class ListBarMixin(MultipleObjectMixin):

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['bar_left'] = bar_left
        return context


class DetailBarMixin(SingleObjectMixin):

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['bar_left'] = bar_left
        return context


class TemplateBarMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        self.object = list()
        context = super().get_context_data(**kwargs)
        context['bar_left'] = bar_left
        return context