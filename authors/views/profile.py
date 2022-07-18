from authors.models import Profile
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView


class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = context.get('id')
        profile = get_object_or_404(Profile.objects.filter(
            pk=profile_id).select_related('user')
        )
        context.update({
            'profile': profile
        })
        return context
