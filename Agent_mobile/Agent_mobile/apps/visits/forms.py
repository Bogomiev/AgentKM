from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.admin.widgets import AdminTimeWidget
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from .models import Visit
from .models import Shop
from django.forms import widgets


class EventSplitDateTime(forms.SplitDateTimeWidget):
    def __init__(self, attrs=None):
        widgets = [forms.TextInput(attrs={'class': 'vDateField'}),
                   forms.TextInput(attrs={'class': 'vTimeField'})]
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return mark_safe(u'%s%s' % (rendered_widgets[0], rendered_widgets[1]))


class VisitForm(forms.ModelForm):
    visitTime = forms.CharField(max_length=8, widget=AdminTimeWidget())

    def __init__(self, *args, **kwargs):
        super(VisitForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        return super(VisitForm, self).save(*args, **kwargs)

    class Meta:
        model = Visit
        fields = ('visitDate', 'shop', 'result', 'note', 'visitTime')
        help_texts = {
            'visitDate': '',
            'shop': '',
            'result': '',
            'note': '',
        }

        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'cols': 10, 'rows': 4}),
            'visitDate': widgets.SelectDateWidget(),
            'shop': widgets.Select(attrs={'choice': Shop.objects.all()})
        }
