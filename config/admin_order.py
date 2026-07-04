from django.contrib import admin

_original_get_app_list = admin.sites.AdminSite.get_app_list


def _ordered_get_app_list(self, request):
    app_list = _original_get_app_list(self, request)
    preferred_order = [
        'Authentication and Authorization',
        'Annotations',
        'Tasks',
        'Users',
    ]
    order_index = {name: index for index, name in enumerate(preferred_order)}

    def sort_key(app):
        return (order_index.get(app['name'], len(preferred_order)), app['name'])

    return sorted(app_list, key=sort_key)


admin.sites.AdminSite.get_app_list = _ordered_get_app_list
