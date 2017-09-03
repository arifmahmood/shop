"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from project import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #------------default  and logout ------------
    url(r'^$', views.show_home_page, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),

    #----------------- login ----------------------
    url(r'^login/$', views.show_login_page, name='login'),
    url(r'^login/auth/$',views.auth_method,name='auth'),
    url(r'^home/$', views.show_home_page, name='home'),

    #----------------- item-----------------
    url(r'^item/$',views.show_item_page,name='item_page'),
    url(r'^item/add/$',views.show_item_add_page,name='item_add_page'),
    url(r'^item/delete/$',views.show_item_delete_page,name='item_delete_page'),
    url(r'^item/edit/$',views.show_item_edit_page,name='item_edit_page'),

    #-------------------supplier and customer ------------
    url(r'^sc/$', views.show_sc_page, name='sc_page'),
    url(r'^sc/add/$', views.show_sc_add_page, name='sc_add_page'),
    url(r'^sc/delete/$', views.show_sc_delete_page, name='sc_delete_page'),
    url(r'^sc/edit/$',views.show_sc_edit_page,name='sc_edit_page'),

    #------------------ sale -----------------------
    url(r'^sale/$',views.sale_page_load, name='sale_page'),
    url(r'^sale/sale_add/$',views.sale_add_page_load, name='sale_add_page'),
    url(r'^sale/sale_edit_delete/$',views.sale_edit_delete, name='sale_edit_delete'),

    #------------------- purchase -------------------------

    url(r'^purchase/$',views.purchase_page_load, name='purchase_page'),
    url(r'^purchase/purchase_add/$',views.purchase_add_page_load, name='purchase_add_page'),
    url(r'^purchase/purchase_edit_delete/$',views.purchase_edit_delete, name='purchase_edit_delete'),




    #------------------- report ----------------------
    url(r'^report_item_list/$', views.report_item_list,name='report_item_list'),









]
