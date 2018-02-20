"""
kairozu base-level URLconf: https://docs.djangoproject.com/en/1.10/topics/http/urls/

function views: from my_app import views, url(r'^$', views.home, name='home')
cbv: from other_app.views import Home, url(r'^$', Home.as_view(), name='home')
import urlconf: from django.conf.urls import url, include, url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler404, handler500
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from main import reg_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^accounts/$', reg_views.account, name='account'),
    url(r'^accounts/profile/$', reg_views.account, name='profile'),
    url(r'^accounts/newuser/$', reg_views.newuser, name='newuser'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^accounts/register/$', reg_views.register, name='register'),
    # url(r'^accounts/activation_sent/$', reg_views.activation_sent, name='activation_sent'),
    # url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', reg_views.activate, name='activate'),
    url(r'^main/', include('main.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^sandbox/', include('sandbox.urls')),
    url(r'^demo/', include('demo.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = reg_views.error_404
handler500 = reg_views.error_500

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]
