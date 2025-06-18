from functools import wraps
from django.core.exceptions import PermissionDenied

def cargo_requerido(*cargos_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            colaborador = getattr(request.user, 'colaborador', None)
            if colaborador and colaborador.cargo in cargos_permitidos:
                return view_func(request, *args, **kwargs)

            raise PermissionDenied
        return _wrapped_view
    return decorator
