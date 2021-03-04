from .views import index,post1,listall,edit,diet,close,findFood,about_us,history,choose_date,choose_date_three,choose_date_week
from django.conf.urls import url
urlpatterns = [
    url(r'^index/', index),
    url(r'^listall/', listall),
    url(r'^post/', post1),
    url(r'^edit/(\w+)/(\w+)$',edit),
    url(r'^diet/',diet),
    url(r'^findfood/',findFood),
    url(r'^about_us/',about_us),
    url(r'^history/(\w+)/(\w+)/(\w+)$',history),
    url(r'^choose/',choose_date),
    url(r'^choose_three/',choose_date_three),
    url(r'^choose_week/',choose_date_week),
]