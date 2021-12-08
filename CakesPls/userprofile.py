from app.models import Profile

def profile(request):
    if request.user.is_authenticated:
        currentProfile, status = Profile.objects.get_or_create(user = request.user)
        if status:
            currentProfile.role = 'client'
            currentProfile.save()
    else:
        currentProfile = None
    return {
            'userprofile': currentProfile
            }
