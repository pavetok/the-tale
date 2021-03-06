# coding: utf-8

from django.conf.urls import patterns, include

from dext.views import resource_patterns

from the_tale.linguistics import views


urlpatterns = patterns('',
                       (r'^words/', include(resource_patterns(views.WordResource), namespace='words') ),
                       (r'^templates/', include(resource_patterns(views.TemplateResource), namespace='templates') ) )


urlpatterns += resource_patterns(views.LinguisticsResource)
