from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Index, UserActivity, Article
from accounts.models import CustomUser
from .forms import IndexForm
from django.http import JsonResponse
import json
import os
from collections import Counter

# import openai

from hanspell import spell_checker  # 한글 맞춤법 교정에 사용
from PyKomoran import *  # 한글 키워드 추출에 사용

# 영문 NLP
from spellchecker import SpellChecker  # 맞춤법
from textblob import TextBlob  # 키워드 추출

# 영문 keyword 분석에 필요한 코드
import nltk

# 아래 데이터도 다운 받아야한다.
# nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger")


# openai.api_key = os.getenv("OPENAI_API_KEY")
komoran = Komoran("EXP")


def index(request):
    index_table = Index.objects.all()
    context = {
        "index_table": index_table,
        "login_user": request.user,
    }
    return render(request, "crud/index.html", context)


def create(request):
    article = Article()
    index = Index()
    if request.user.is_authenticated:
        if request.method == "POST":
            article.user = request.user
            article.title = request.POST.get("title")
            article.content = request.POST.get("content")
            article.save()
            index.article = article
            index.save()
            return redirect("crud:index")
    return render(request, "crud/create.html")


def detail(request, pk):
    selected = Article.objects.get(pk=pk)
    context = {
        "selected": selected,
    }
    if request.user.is_authenticated:
        return render(request, "crud/detail.html", context)


def update(request, pk):
    index = Index.objects.get(pk=pk)
    to_update = Article.objects.get(pk=index.id)
    context = {
        "to_update": to_update,
    }
    if request.user.is_authenticated:
        if request.method == "POST":
            to_update.user = request.user
            to_update.title = request.POST.get("title")
            to_update.content = request.POST.get("content")
            to_update.title = json.loads(request.body)["title"]
            to_update.content = json.loads(request.body)["content"]
            to_update.save()
            index.article = to_update
            index.save()
            return redirect("crud:index")
        return render(request, "crud/update.html", context)
    else:
        return redirect("crud:detail", pk)


def delete(request, pk):
    if request.user.is_authenticated:
        if Article.objects.filter(pk=pk):
            to_delete = Article.objects.get(pk=pk)
            to_delete.delete()
    return redirect("crud:index")


def like(request, pk):
    selected = Article.objects.get(pk=pk)
    if request.user.is_authenticated:
        if (
            UserActivity.objects.filter(user_id=request.user.id)
            .filter(liked_article_id=selected.id)
            .exists()
            == False
        ):
            liked = UserActivity(user=request.user, liked_article=selected)
            liked.save()
        return redirect("crud:detail", pk)


def like_delete(request, pk):
    if request.user.is_authenticated:
        seleted_like = UserActivity.objects.filter(pk=pk)
        seleted_like.delete()
    return redirect("crud:user_page")


def user_page(request):
    activity_table = UserActivity.objects.filter(user=request.user)
    article = Article.objects.filter(user=request.user)
    context = {
        "activity_table": activity_table,
        "article": article,
    }
    return render(request, "crud/user_page.html", context)


def user_profile(request):
    return render(request, "crud/user_profile.html")


# 게시물 세부페이지에서 버튼을 클릭할 시 작동하는 기능들
def new_feature_one(request):
    if request.method == "POST":
        text = json.loads(request.body)
        # spell check (맞춤법 교정)
        strip_text = str(list(text.values())).strip("[]").strip("''")
        spell_text = spell_checker.check(strip_text).as_dict()["checked"]
        checked_text = spell_text.split(" ")
        # English spell_check (영문 맞춤법 교정)
        if strip_text.isalpha():
            spell = SpellChecker()
            spell_text = spell.correction(strip_text)

        # keyword(키워드 추출)
        keyword = komoran.get_plain_text(strip_text)
        split_sentence = keyword.split(" ")
        keyword_set = []
        # 함수를 적용한 내용의 범주가 token_to_get 리스트 안에 있으면
        # keyword_set 리스트에 추가한다.
        token_to_get = ["NN", "NP", "NR", "SL", "NF", "SH", "NV", "MM", "MA"]
        for i in split_sentence:
            for j in token_to_get:
                if j in i:
                    keyword_set.append(i)
        words = [word.split("/")[0] for word in keyword_set]
        # 가장 빈도가 높은 단어를 키워드로 한다.
        word_count = Counter(words).items()
        word_count_top = max(Counter(words).values())
        top_words = [i[0] for i in word_count if i[1] == word_count_top]
        # English keyword (영문 키워드 추출)
        if strip_text.isalpha():
            blob = TextBlob(strip_text)
            top_words = [word for word, pos in blob.tags if pos.startswith("NN")]
        context = {
            "keyword_text": top_words,
            "spell_text": spell_text,
        }
    return render(request, "crud/new_feature_one.html", context)
