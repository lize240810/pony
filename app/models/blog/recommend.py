from django.db import models
from django.core.cache import cache
from app.models.blog.article import BlogArticle
from app.models.blog.image import Image
import django.utils.timezone as timezone

CACHE_KEY_ID = "Pony:HomeRecommend:CacheId:"
CACHE_TIME = 60*20


class HomeRecommend(models.Model):

    share_id = models.IntegerField(default=0)
    reco_cover = models.IntegerField(default=0)
    reco_intro = models.CharField(default='')
    weight = models.IntegerField(default=0)
    operator_id = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def query_recommend_list(page=0, per_page=10):
        recom_list = HomeRecommend.objects.filter(status=1).order_by("-weight")[page: per_page]
        result = []
        for recommend in recom_list:
            result.append(HomeRecommend.format_recommend(recommend))
        return result

    @staticmethod
    def query_recommend_by_share_id(share_id=0, use_cache=True):
        key = CACHE_KEY_ID + str(share_id)
        if use_cache:
            recom = cache.get(key)
            if recom:
                return recom
        try:
            recom = HomeRecommend.objects.filter(status=1).get(share_id=share_id)
            recom = HomeRecommend.format_recommend(recom, False)
            cache.set(key, recom, CACHE_TIME)
            return recom
        except HomeRecommend.DoesNotExist:
            return None

    @staticmethod
    def format_recommend(recommend, full_info=True):
        result = dict()
        result["id"] = recommend.id
        result["reco_into"] = recommend.reco_intro
        result["cover"] = Image.query_image_by_id(recommend.reco_cover)

        if full_info:
            article = BlogArticle.query_article_by_id(recommend.share_id)
            del article["content"]
            result["article_info"] = article

        return result

    class Meta:
        app_label = "b_blog"
        db_table = "home_recommend"
