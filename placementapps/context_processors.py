# placementapps/context_processors.py
from .models import TutorNotification

def notifications_count(request):
    # Ensure this matches your login session key (e.g., 'id' or 'tutor_id')
    tutor_id = request.session.get('id')
    if tutor_id:
        count = TutorNotification.objects.filter(tutor_id=tutor_id, is_read=False).count()
        return {'notifications_count': count}
    return {'notifications_count': 0}   