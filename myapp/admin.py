from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Question)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_text','is_correct')


admin.site.register(Answer,AnswerAdmin)

class ResultsAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_decrypted_marks','timestamp')

    def get_decrypted_marks(self, obj):
        return obj.get_decrypted_marks()

admin.site.register(Results,ResultsAdmin)
