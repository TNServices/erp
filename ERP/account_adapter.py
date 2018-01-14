### Désactive les inscirptions ###
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
class NoNewUsersAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return False


