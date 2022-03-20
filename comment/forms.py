# from django import forms
# from .models import Comment
# from mptt.forms import TreeNodeChoiceField
#
#
# class NewCommentForm(forms.ModelForm):
#     parent = TreeNodeChoiceField(queryset=Comment.objects.all())
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['parent'].label = ''
#         self.fields['parent'].required = False
#
#     class Meta:
#         model = Comment
#         fields = ('user', 'parent', 'content', 'content_type', 'object_id')
#
#
#     def save(self, *args, **kwargs):
#         Comment.objects.rebuild()
#         return super(NewCommentForm, self).save(*args, **kwargs)
#
# def perform_create(self, serializer):
#     comment_form = NewCommentForm({'content': self.request.data.get('content'),
#                                            'user': self.request.user,
#                                            'parent': self.request.data.get('parent'),
#                                            'content_type': self.request.data.get('content_type'),
#                                             'object_id': self.request.data.get('object_id'), })
#             if comment_form.is_valid():
#                 comment_form.save()
