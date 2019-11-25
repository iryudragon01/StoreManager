from stock.models import User,Worker,Item
from stock.data2view.user import action,queries


def is_item_exists(url,name=False, id=False):
    if id is False:
        return Item.objects.filter(
        user = queries.get_user(url),
        name = name
    ).exists()
    if name is False:
        return Item.objects.filter(
            id=id,
            user=queries.get_user(url)
        ).exists()