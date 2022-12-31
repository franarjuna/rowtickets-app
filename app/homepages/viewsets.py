from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets
from rest_framework.response import Response

from events.models import Event
from homepages.models import Homepage, HomepageSlide
from homepages.serializers import HomepageDetailSerializer


class HomepageViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Homepage.objects.all()
    lookup_field = 'country'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.all()

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        print(args)
        print(kwargs)
        country = kwargs['country']
        homepage = get_object_or_404(queryset, country=country)
        homepage_serializer = HomepageDetailSerializer(homepage)
        highlighted_events = Event.objects.filter(published=True, highlighted=True, country=country)[:8]
        print(highlighted_events)
        # queryset = User.objects.all()

        # user = get_object_or_404(queryset, pk=pk)
        # serializer = UserSerializer(user)
        return Response({
            'homepage_data': homepage_serializer.data,
            'highlighted_events': ['dadsadasd']
        })

    def get_serializer_class(self):
        return HomepageDetailSerializer
