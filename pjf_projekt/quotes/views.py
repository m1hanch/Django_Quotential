from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .utils import conn, Authors, Quotes
from django.core.paginator import Paginator
from .forms import AuthorForm, TagForm, QuoteForm, CommentForm
from .models import Author, Tag, Quote, Comment
from django.contrib.auth.models import User


def get_top_ten_tags():
    return Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]


def index(request, page=1):
    """
    The index function is the main view for the quotes app.
    It displays a list of all quotes in the database, ordered by id.
    The list is paginated to display 10 items per page.

    :param request: Get the request object
    :param page: Determine which page of quotes to display
    :return: A response object with a template
    """
    quotes = Quote.objects.all().order_by('id')  # noqa
    paginator = Paginator(quotes, 10)
    quotes_on_page = paginator.page(page)
    top_tags = get_top_ten_tags()
    return render(request, template_name='quotes/index.html',
                  context={'quotes': quotes_on_page, 'top_tags': top_tags})


@login_required
def add_author(request):
    """
    The add_author function is a view that allows the user to add an author.
    The function takes in a request and returns a rendered template with the form for adding an author.
    If the method of the request is POST, then it will take in all of the data from that form and save it as an Author object.

    :param request: Get the request object
    :return: An html page with a form to add an author
    """
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
    """
    The add_quote function is a view that allows the user to add a quote.
    The function first gets all of the authors from the database and passes them into
    the context dictionary. If it's a POST request, then we create an instance of QuoteForm with
    the data from request.POST and an empty instance of Quote(). We check if form is valid, if so, we save it without committing to database yet (commit=False). Then we save our quote object in order to get its id for use in Quotes model later on. Next, we split up tags by commas and iterate through each tag name using strip() method

    :param request: Get the data from the form
    :return: A redirect to the index page
    """
    authors = Author.objects.all()  # noqa
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
    """
    The author_detail function takes a request and an author_id,
    gets the Author object with that id (or raises a 404 error if it can't find one),
    and renders the 'quotes/author_detail.html' template with that Author object.

    :param request: Pass information from the browser to the server
    :param author_id: Specify the author that we want to display
    :return: The author_detail
    """
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes/author_detail.html', {'author': author})


def tag_search(request, tag):
    """
    The tag_search function takes a request and tag as parameters.
    It then filters the quotes by the tag name, and renders them to a template.

    :param request: Pass the request object to the view
    :param tag: Filter the quotes by tag
    :return: The quotes that have the tag in their tags field
    """
    quotes = Quote.objects.filter(tags__name=tag)
    return render(request, 'quotes/tag_search.html', {'quotes': quotes})


def quote_comments(request, quote_id):
    """
    The quote_comments function takes a request and quote_id as parameters.
    It then filters the Quote model for the quote with that id, and assigns it to a variable called 'quote'.
    It also filters the Comment model for all comments associated with that quote, and assigns them to a variable called 'comments'.
    Finally, it renders an HTML template named &quot;quotes/quote_comments.html&quot; using those variables as context.

    :param request: Pass the request object to the view
    :param quote_id: Filter the quote object from the database
    :return: A rendered template with the quote and comments
    """
    quote = Quote.objects.filter(pk=quote_id).first()  # noqa
    comments = Comment.objects.filter(quote=quote)  # noqa
    return render(request, template_name='quotes/quote_comments.html', context={'quote': quote, 'comments': comments})


@login_required
def add_comment(request, quote_id):
    """
    The add_comment function takes in a request and quote_id,
        then creates a new comment object with the data from the form.
        The function also renders the quote_comments template.

    :param request: Get the request object from the view
    :param quote_id: Find the quote that is being commented on
    :return: A rendered template
    """
    quote = Quote.objects.filter(pk=quote_id).first()  # noqa
    comments = Comment.objects.filter(quote=quote)  # noqa
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.quote = quote
            comment.user = request.user
            comment.save()
        else:
            print(form.errors)
    return render(request, template_name='quotes/quote_comments.html', context={'quote': quote, 'comments': comments})
