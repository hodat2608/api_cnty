from rest_framework import permissions
from .models import Note
class ModifyNotePermisson(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ('PUT', 'DELETE'):
            try:
                pk = view.kwargs.get('pk')
            except : 
                pass
            user = request.user
            try:
                note = Note.objects.get(pk=pk)
                if note.user == user:
                    return True
                else:
                    return False
            except Note.DoesNotExist:
                return False
        return True
