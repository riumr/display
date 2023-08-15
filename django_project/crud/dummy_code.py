def like(request,pk):
    cached_username=r.keys()[0].decode('utf-8')
    article = Article.objects.get(pk=pk)
    custom_user = CustomUser.objects.get(username=cached_username)
    if r.dbsize() != 0:
        liked = UserActivity(user=custom_user,liked_article=article) # user profile
        liked.save()
        return redirect("crud:like_page")
    else:
        return redirect("crud:detail")