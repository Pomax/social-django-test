"""
Views to get entries
"""

import django_filters
from rest_framework.generics import (ListCreateAPIView, RetrieveAPIView,)
from rest_framework import filters
from rest_framework.response import Response

from server.users.views import (post_validate, new_nonce_value)

from server.entries.models import Entry
from server.entries.serializers import (
    EntrySerializer,
)


class EntryCustomFilter(filters.FilterSet):
    """
    We add custom filtering to allow you to filter by:
        * Tag - pass the `?tags=` query parameter
    Accepts only one filter value i.e. one tag and/or one
    category.
    """
    tags = django_filters.CharFilter(
        name='tags__name',
        lookup_expr='iexact',
    )

    class Meta:
        """
        entry-specific metadata
        """
        model = Entry
        fields = ['tags']

class  EntryView(RetrieveAPIView):
    """
    A view to retrieve individual entries
    """
    queryset = Entry.objects.public()
    serializer_class = EntrySerializer
    pagination_class = None

class EntriesListView(ListCreateAPIView):
    """
    This is copied from Science
    A view that permits a GET to allow listing all the projects
    in the database

    **Route** - `/entries`

    **Query Parameters** -

    - `?search=` - Allows search terms
    - `?sort=` - Allows sorting of entries.
        - date_created - `?sort=date_created`
        - date_updated - `?sort=date_updated`

        *To sort in descending order, prepend the field with a '-', for e.g.
        `?sort=-date_updated`*

    - `?tags=` - Allows filtering entries by a specific tag
    - `?categories=` - Allows filtering entries by a specific category
    - `?expand=` -
    Forces the response to include basic
    information about a relation instead of just
    hyperlinking the relation associated
    with this project.

           Currently supported values are `?expand=leads`,
           `?expand=events` and `?expand=leads,events`

    """
    queryset = Entry.objects.public()
    # pagination_class = PageNumberPagination
    filter_backends = (
        # filters.DjangoFilterBackend,
        filters.SearchFilter,
        # filters.OrderingFilter,
    )
    filter_class = EntryCustomFilter
    ordering_fields = (
        'date_created',
        'date_updated',
    )
    search_fields = (
        'title',
        'description',
    )
    serializer_class = EntrySerializer

    def list(self, request):
        """
        Before we generate this view (with creation form), we need
        to make sure we have a new nonce value so that form posts
        can be checked for resubmission.
        """
        new_nonce_value(request)
        queryset = self.get_queryset()
        serializer = EntrySerializer(queryset, many=True, context={
            'nonce': request.session['nonce']
        })
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        OVerride the "create" call to make sure we verify that
        the user is signed in, and has communicated the correct
        csrf token, form nonce, etc.
        """
        request = self.request
        validation_result = post_validate(request)

        if validation_result is True:
            # invalidate the nonce, so this form cannot be resubmitted with the current id
            request.session['nonce'] = False
            serializer.save()

        else:
            print(validation_result)
