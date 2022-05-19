from kivymd.uix.textfield import MDTextField
import re


class TextInput(MDTextField):

    def text_validate(self, instance, value, max_text_length=50):
        """ Category text box validation and removal of double spaces and tabs"""
        value = re.sub('(\s{2,})|([\t,\n,\r])', ' ', value)
        instance.text = value.lstrip()
        if len(value) > max_text_length:
            instance.error = True
            instance.text = value[:-1]
            # self.ids.text_category.helper_text = "максимальная длина"
            return
        elif len(instance.text) <= max_text_length:
            instance.error = False
            instance.helper_text = ""


class TextInputCategory(TextInput):

    def recording_category(self, instance, root):
        """Entering the category name from the text field when focus is lost"""
        if instance.focus is False and instance.error is False:
            instance.text = instance.text.rstrip()
            root.data_for_query.update({'title': instance.text})


class TextInputSumma(TextInput):

    def recording_summa(self, instance, root):
        """Entering the category name from the text field when focus is lost"""
        instance.error = False
        # instance.helper_text = ""
        if instance.focus is False:
            root.data_for_query.update({
                    'summa': instance.text
            })

    def text_validate_summa(self, instance, value):
        """ limit the number of characters to enter, and 2 decimal places"""
        status = re.match('.*\..{3,}', value)
        if status or len(value) > 10:
            instance.text = value[:-1]


class TextInputComent(TextInput):
    def recording_comment(self, instance, root):
        """Entering the category name from the text field when focus is lost"""
        if instance.focus is False and instance.error is False:
            instance.text = instance.text.rstrip()
            root.data_for_query.update({'comment': instance.text})

    def text_validate_comment(self, instance, value, max_text_length):
        """ Category text box validation and removal of double spaces and tabs"""
        super().text_validate(instance, value, max_text_length)
