class UserManager(object):
    def __init__(self):
        self.users = {}
        self.load()

    def load(self):
        pass
        # TODO: read users from some storage

    def save(self):
        pass
        # TODO: save users to same storage

    def has_permission(self, user, permission):
        if user in self.users:
            user_permissions = self._get_user_permissions(user)
            return permission in user_permissions
        else:
            return False

    def grant_permission(self, user, permission):
        permissions = self._get_user_permissions(user)
        if permission not in permissions:
            permissions.append(permission)
            self.users[user]['permissions'] = permissions

    def revoke_permission(self, user, permission):
        permissions = self._get_user_permissions(user)
        if permission not in permissions:
            permissions = [perm for perm in permissions if perm != permission]
            self.users[user]['permissions'] = permissions

    def _get_user_permissions(self, user):
        return self.users[user].get('permissions', [])
