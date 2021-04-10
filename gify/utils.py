import datetime

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from .models import Action


def create_action(profile, verb, target=None, url=None) -> bool:
    """
    Util function for creating actions
    """
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(profile_id=profile.id,
                                            verb=verb,
                                            created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct,
            target_id=target.id
        )

    if not similar_actions:
        action = Action(profile=profile,
                        verb=verb,
                        target=target,
                        url=url)
        action.save()
        return True
    return False
