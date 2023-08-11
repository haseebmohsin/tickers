from django.contrib import admin
from .models import words_to_be_searched_model,Ticker_Extraction_Model,Character_Comparison
admin.site.register(Ticker_Extraction_Model)
admin.site.register(Character_Comparison)
admin.site.register(words_to_be_searched_model)

# Register your models here.
