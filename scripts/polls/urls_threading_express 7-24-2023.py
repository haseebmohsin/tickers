
from django.urls import path, include
# from .views import whatsapp_sender,getting_offline_collage,getting_live_collage,index,dunya_ticker,table_view,ary_ticker,samaa_ticker,express_ticker,geo_ticker,ninety_two_ticker
from django.conf import settings
from django.conf.urls.static import static
from .views import ticker_express_frame_saver,login_view,logout_view,register_view,getting_offline_collage,getting_live_collage,index,dunya_ticker,table_view,ary_ticker,samaa_ticker,express_ticker,geo_ticker,ninety_two_ticker
# from .views import login_view,logout_view,register_view,getting_offline_collage,getting_live_collage,index,dunya_ticker,table_view,ary_ticker,samaa_ticker,express_ticker,geo_ticker,ninety_two_ticker


urlpatterns = [
    path('index/' ,index, name='index' ),
        path('dunya_ticker/' ,dunya_ticker, name='dunya_ticker' ),
        path('ary_ticker/' ,ary_ticker, name='ary_ticker' ),
                path('samaa_ticker/' ,samaa_ticker, name='samaa_ticker' ),
                                path('express_ticker/' ,express_ticker, name='express_ticker' ),

                                path('geo_ticker/' ,geo_ticker, name='geo_ticker' ),

                                path('ninety_two_ticker/' ,ninety_two_ticker, name='ninety_two_ticker' ),

    path('table/', table_view, name='table_view'),
    path('getting_live_collage/', getting_live_collage, name='getting_live_collage'),

    path('getting_offline_collage/', getting_offline_collage, name='getting_offline_collage'),
       path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
        path('ticker_express_frame_saver/', ticker_express_frame_saver, name='ticker_express_frame_saver'),

    
    # path('whatsapp_sender/', whatsapp_sender, name='whatsapp_sender'),
    

        
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)