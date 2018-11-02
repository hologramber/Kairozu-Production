from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.static import static
from django.conf import settings
from main import reg_views

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'favicon/favicon.ico')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^privacy/', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    url(r'^hikai/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^accounts/$', reg_views.account, name='account'),
    url(r'^accounts/profile/$', reg_views.account, name='profile'),
    # url(r'^accounts/newuser/$', reg_views.newuser, name='newuser'),
    url(r'^accounts/login/$', auth_views.LoginView, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView, {'next_page': 'login'}, name='logout'),
    url(r'^accounts/register/$', reg_views.BetaEmailView.as_view(), name='register'),
    url(r'^accounts/beta-confirm/$', reg_views.BetaConfirmView.as_view(), name='betaconfirm'),
    # url(r'^accounts/register/$', reg_views.register, name='register'),
    # url(r'^accounts/activation_sent/$', reg_views.activation_sent, name='activation_sent'),
    # url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', reg_views.activate, name='activate'),
    url(r'^main/', include('main.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^sandbox/', include('sandbox.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^analysis/', include('analysis.urls'))
    ]
