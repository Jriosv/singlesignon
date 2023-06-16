from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from polls import models

def is_profile_complete(user):
    site = user.profile.site
    form = models.ProfileForm.objects.get(site=site)
    form_fields = form.form_fields['fields']
    required_fields = [field['id'] for field in form_fields if field['required']]
    
    allowed_data = ['london','spain','bulgaria','Manager']
    is_complete = None
    if 'location' in user.profile.dynamic_fields:
        if user.profile.dynamic_fields['location'] not in allowed_data:
            is_complete = False
    else:
        is_complete = all([field in user.profile.dynamic_fields for field in required_fields])
    
    return is_complete

class ProfileRedirectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        current_user = request.user
        skip_urls = [
            '/polls/myprofile',
            '/accounts/logout/',
        ]

        if (
            current_user.is_authenticated
            and request.path not in skip_urls
            and not is_profile_complete(current_user)
        ):
            #print(current_user)
            return HttpResponseRedirect(reverse_lazy("my_profile"))
        else:
           
            pass #print(current_user.profile.dynamic_fields)