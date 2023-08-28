from django.contrib import admin
from .models import *

admin.site.site_header = "ADOJ Admin"
admin.site.site_title = "Welcome to ADOJ Admin Portal"
admin.site.index_title = "ADOJ Admin"

# admin.site.index_template = "home/leaderboard.html"

# Register your models here.
admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(Testcase)
