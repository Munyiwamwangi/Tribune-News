import datetime as dt
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Article, NewsLetterRecipients, MoringaMerch
from .forms import NewsLetterForm, NewArticleForm
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from .forms import NewArticleForm, NewsLetterForm
from django.http import JsonResponse
from .serializer import MerchSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .permissions import IsAdminOrReadOnly

# Create your views here.


def welcome(request):
    return render(request, 'welcome.html')


def news_today(request):
    date = dt.date.today()
    # news = Article.todays_news()
    news = Article.objects.all()
    form = NewsLetterForm()
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if request.method == 'POST':
            form = NewsLetterForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['your_name']
                email = form.cleaned_data['email']
                recipient = NewsLetterRecipients(name=name, email=email)
                recipient.save()
                send_welcome_email(name, email)

                HttpResponseRedirect('news_today')
    else:
        form = NewsLetterForm()

    return render(request, 'all-news/today-news.html', {"date": date, "news": news, "letterForm": form})


def past_days_news(request, past_date):
    try:
        # Converts data from the string Url
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()
    except ValueError:
        # Raise 404 error when ValueError is thrown
        raise Http404()
        assert False

    if date == dt.date.today():
        return redirect(news_today)

    news = Article.days_news(date)
    return render(request, 'all-news/past-news.html', {"date": date, "news": news})


def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html', {"message": message, "articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html', {"message": message})


@login_required(login_url='/accounts/login/')
def article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except DoesNotExist:
        raise Http404()
    return render(request, "all-news/article.html", {"article": article})


@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
        return redirect('newsToday')

    else:
        form = NewArticleForm()
    return render(request, 'new_article.html', {"form": form})


def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

#RESTFUL APIs

class MerchList(APIView):
    def get(self, request, format=None):
        all_merch = MoringaMerch.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)


    def post(self, request, format=None):
        serializers = MerchSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = (IsAdminOrReadOnly,)


class MerchDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_merch(self, pk):
        try:
            return MoringaMerch.objects.get(pk=pk)
        except MoringaMerch.DoesNotExist:
            return Http404

#Update an object

    def put(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch)
        return Response(serializers.data)

#Deleting an Object

    def delete(self , request, pk, format = None):
      merch = se;f.get+merch(pk)
      merch.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
