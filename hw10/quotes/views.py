from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .utils import conn, Authors, Quotes
from django.core.paginator import Paginator
from .forms import AuthorForm, TagForm, QuoteForm
from .models import Author, Tag, Quote


def index(request, page=1):
    quotes = Quote.objects.all().order_by('id')  # noqa
    paginator = Paginator(quotes, 10)
    quotes_on_page = paginator.page(page)
    return render(request, template_name='quotes/index.html',
                  context={'quotes': quotes_on_page})


@login_required
def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            form.save()
            Authors(fullname=form.cleaned_data['fullname'], born_date=form.cleaned_data['born_date'],
                    born_location=form.cleaned_data['born_location'],
                    description=form.cleaned_data['description']).save()
            return redirect(to='quotes:index')
    return render(request, template_name='quotes/add_author.html', context={"form": form})


@login_required
def add_quote(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=Quote())
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            tag_names = form.cleaned_data['tags'].split(',')
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name.strip())
                quote.tags.add(tag)
            Quotes(quote=form.cleaned_data['quote'], tags=form.cleaned_data['tags'].split(','),
                   author=form.cleaned_data['author'].pk).save()
            return redirect(to='quotes:index')
        print(form.errors)
    return render(request, template_name='quotes/add_quote.html', context={'authors': authors})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})


def tag_search(request, tag):
    quotes = Quote.objects.filter(tags__name=tag)
    return render(request, 'quotes/tag_search.html', {'quotes': quotes})


def quote_comments(request, quote_id):
    quote = Quote.objects.filter(pk=quote_id).first()
    return render(request, template_name='quotes/quote_comments.html', context={'quote': quote})
