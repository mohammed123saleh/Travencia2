from django.db.models import Q, Case, When, Value, IntegerField

class SearchResultsAdminMixin(object):
    def get_search_results(self, request, queryset, search_term):
        ''' Show exact match for title and slug at top of admin search results.
        '''
        qs, use_distinct = \
            super(SearchResultsAdminMixin, self).get_search_results(
                request, queryset, search_term)

        search_term = search_term.strip()
        if not search_term:
            return qs, use_distinct

        def cond_int(query):
            return Case(
                When(query, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )

        qs = qs.annotate(
            exact_title=cond_int(Q(title__iexact=search_term)),
            exact_convention=cond_int(Q(convention__iexact=search_term)),
        )

        order_by = []
        if qs.filter(exact_title=1).exists():
            order_by.append('-exact_title')
        if qs.filter(exact_convention=1).exists():
            order_by.append('-exact_convention')

        if order_by:
            qs = qs.order_by(*order_by)

        return qs, use_distinct