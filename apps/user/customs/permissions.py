from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 1:
            return True
        return False


class IsClient(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 2:
            return True
        return False


class IsEngineer(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 3:
            return True
        return False


class IsNotEngineer(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 3:
            return False
        return True


class IsRegionInCharge(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 4:
            return True
        return False


class IsHqInCharge(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 5:
            return True
        return False


class IsRegionTeam(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 6:
            return True
        return False


class IsHqTeam(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 7:
            return True
        return False


class IsCallUpdater(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 8:
            return True
        return False


class IsRegionCoordinator(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 9:
            return True
        return False


class IsDispatchUpdater(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 10:
            return True
        return False


class IsCoordinatorTeam(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 11:
            return True
        return False


class IsCustomerOperator(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 12:
            return True
        return False


class IsCustomerManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 13:
            return True
        return False


class IsCustomerOwaner(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 14:
            return True
        return False


class IsCustomerOEM(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 15:
            return True
        return False


class IsTelEngineer(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 16:
            return True
        return False


class IsVisitEngineer(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 17:
            return True
        return False


class IsRegionServiceInCharge(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 18:
            return True
        return False


class IsStoreUpdater(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 19:
            return True
        return False


class IsProductionUpdater(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 20:
            return True
        return False


class IsPurchaseUpdate(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 21:
            return True
        return False


class IsAsstManage(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 22:
            return True
        return False


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 23:
            return True
        return False


class IsDirector(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 24:
            return True
        return False


class IsTestingInCharge(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 25:
            return True
        return False


class IsQualityManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.user_role == 26:
            return True
        return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class WriteOnly(BasePermission):
    def has_permission(self, request, view):
        WRITE_METHODS = [
            "POST",
        ]
        return request.method in WRITE_METHODS


class ExceptDelete(BasePermission):
    message = "dont allow for delete"

    def has_permission(self, request, view):
        WRITE_METHODS = [
            "DELETE",
        ]
        return request.method not in WRITE_METHODS


class DeleteOnly(BasePermission):
    def has_permission(self, request, view):
        DELETE_METHODS = [
            "DELETE",
        ]
        return request.method in DELETE_METHODS


class UpdateOnly(BasePermission):
    def has_permission(self, request, view):
        UPDATE_METHODS = [
            "UPDATE",
        ]
        return request.method in UPDATE_METHODS
