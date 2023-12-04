from django.shortcuts import render, redirect
from .utils import conn, Authors, Quotes
from django.core.paginator import Paginator
from .forms import AuthorForm, TagForm, QuoteForm
from .models import Author, Tag, Quote


def index(request, page=1):
    quotes = Quotes.objects.all()
    paginator = Paginator(quotes, 10)  # Show 10 quotes per page
    quotes_on_page = paginator.page(page)
    return render(request, template_name='quotes/index.html', context={'page': page, 'quotes': quotes_on_page})


def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            form.save()
            return redirect(to='quotes:index')
    return render(request, template_name='quotes/add_author.html', context={"form": form})


def add_quote(request):
    quotes = Quotes.objects.all()
    authors = Authors.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=Quote())
        if form.is_valid():
            form.save()
            return redirect(to='quotes:index')
    return render(request, template_name='quotes/add_quote.html', context={'authors': authors})
