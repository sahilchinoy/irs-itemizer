from django.shortcuts import render
import watson
from djqscsv import render_to_csv_response
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from irs.models import F8872, Contribution, Expenditure, Committee

class FilingListView(ListView):
    """
    List of all F8872 filings: quarterly, year-end
    or mid-year reports of contributions and expenditures.
    """

    model = F8872
    template_name = 'itemizer/filing_list.html'
    paginate_by = 15
    queryset = F8872.objects.exclude(is_amended=True)


class FilingSearchView(ListView):
    """
    Search F8872 filings.
    """

    model = F8872
    template_name = 'itemizer/filing_search.html'
    paginate_by = 15
    queryset = F8872.objects.exclude(is_amended=True)

    def get_queryset(self):
        """Returns the initial queryset."""
        return watson.search(self.get_query(self.request))

    def get_query(self, request):
        """Parses the query from the request."""
        return request.GET.get('q', "").strip()


class SAView(ListView):
    """
    List of contributions for a particular filing.
    """
    model = Contribution
    template_name = 'itemizer/sa_list.html'

    def get_queryset(self, **kwargs):
        return Contribution.objects.filter(
            form_id_number=self.kwargs['filing_id'])

    def get_context_data(self, **kwargs):
        context = super(SAView, self).get_context_data(**kwargs)
        EIN = F8872.objects.get(form_id_number=self.kwargs['filing_id']).EIN
        context['EIN'] = EIN
        committee_name = Committee.objects.get(EIN=EIN).name
        context['committee_name'] = committee_name
        context['filing_id'] = self.kwargs['filing_id']
        return context


class SACSV(TemplateView):
    """
    CSV of contributions for a particular filing.
    """
    def render_to_response(self, context, **kwargs):
        qs = Contribution.objects.filter(
            form_id_number=self.kwargs['filing_id'])
        return render_to_csv_response(qs)


class SBView(ListView):
    """
    List of expenditures for a particular filing.
    """
    model = Expenditure
    template_name = "itemizer/sb_list.html"

    def get_queryset(self, **kwargs):
        return Expenditure.objects.filter(
            form_id_number=self.kwargs['filing_id'])

    def get_context_data(self, **kwargs):
        context = super(SBView, self).get_context_data(**kwargs)
        EIN = F8872.objects.get(form_id_number=self.kwargs['filing_id']).EIN
        context['EIN'] = EIN
        committee_name = Committee.objects.get(EIN=EIN).name
        context['committee_name'] = committee_name
        context['filing_id'] = self.kwargs['filing_id']
        return context


class SBCSV(TemplateView):
    """
    CSV of expenditures for a particular filing.
    """
    def render_to_response(self, context, **kwargs):
        qs = Expenditure.objects.filter(
            form_id_number=self.kwargs['filing_id'])
        return render_to_csv_response(qs)


class CommitteeDetailView(DetailView):
    """
    Information about a specific committee.
    """
    model = Committee
    template_name = "itemizer/committee_detail.html"
    slug_url_kwarg = 'EIN'
    slug_field = 'EIN'
