from django.forms import ModelForm
from .models import Survey


# Класс-форма(анкета) для опроса абитуриента
class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['worker', 'city', 'points', 'main_direction']