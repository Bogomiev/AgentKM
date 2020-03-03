from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.utils.safestring import mark_safe
from .models import Visit
from django.forms import widgets
from ..main_menu.models import Agent


class EventSplitDateTime(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(attrs={'class': 'vDateField'}),
                   forms.TextInput(attrs={'class': 'vTimeField'})]
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return mark_safe(u'%s%s' % (rendered_widgets[0], rendered_widgets[1]))


CHOICE_ALPH = [('...', '...'), ('а', 'А'), ('б', 'Б'), ('в', 'В'), ('г', 'Г'), ('д', 'Д'), ('е', 'Е'), ('ё', 'Ё'),
               ('ж', 'Ж'), ('з', 'З'), ('и', 'И'), ('й', 'Й'), ('к', 'К'), ('л', 'Л'), ('м', 'М'), ('н', 'Н'),
               ('о', 'О'), ('п', 'П'), ('р', 'Р'), ('с', 'С'), ('т', 'Т'), ('у', 'У'), ('ф', 'Ф'), ('х', 'Х'),
               ('ц', 'Ц'), ('ч', 'Ч'), ('ш', 'Ш'), ('щ', 'Щ'), ('ы', 'Ы'), ('э', 'Э'), ('ю', 'Ю'), ('я', 'Я')]


class VisitForm(forms.ModelForm):
    filter_shop = forms.ChoiceField(widget=widgets.Select(), required=False, choices=CHOICE_ALPH)
    visitTime = forms.CharField(max_length=8, widget=AdminTimeWidget())

    def __init__(self, *args, **kwargs):
        super(VisitForm, self).__init__(*args, **kwargs)
        if kwargs.__contains__('initial'):
            agent = Agent.objects.get(id=kwargs['initial']['agent_id'])
            self.fields['shop'].queryset = agent.available_shops()

    def save(self, *args, **kwargs):
        return super(VisitForm, self).save(*args, **kwargs)

    class Meta:
        model = Visit
        fields = ('visitDate', 'shop', 'result', 'note', 'visitTime', 'filter_shop')
        help_texts = {
            'visitDate': '',
            'shop': '',
            'result': '',
            'note': '',
        }

        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 4}),
            'visitDate': widgets.SelectDateWidget(),
            'shop': widgets.Select(attrs={'choice': Agent.objects.none()})
        }
