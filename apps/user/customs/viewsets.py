from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

# from apps.user.customs.paginations import CustomPageNumberPagination
from apps.user.utilities.swaggers import limit, page, search


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        manual_parameters=[page, limit, search],
        operation_description="description from swagger_auto_schema via method_decorator",
    ),
)
class CustomViewSet(ModelViewSet, SearchFilter):
    filter_backends = [SearchFilter]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        response = {
            "message": "Created Succesfully",
            "data": serializer.data,
            "status": status.HTTP_201_CREATED,
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, *args, **kwargs):
        response = {
            "data": self.get_serializer(self.get_object()).data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        results = super().filter_queryset(queryset=self.get_queryset())
        print("results: ", results)
        results = self.get_serializer(results, many=True).data
        print(results)
        response = {"data": results}
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response = {
            "message": "Updated Succesfully",
            "data": serializer.data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response = {
            "message": "Deleted Succesfully",
            "data": "deleted",
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)


class CustomViewSetFilter(ModelViewSet, SearchFilter):
    filter_backends = [SearchFilter]
    response_tag = "data"

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        response = {
            "message": "Created Succesfully",
            "data": serializer.data,
            "status": status.HTTP_201_CREATED,
        }
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, *args, **kwargs):
        response = {
            "data": self.get_serializer(self.get_object()).data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        # results = super().paginate_queryset(
        #     queryset=super().filter_queryset(queryset=self.get_queryset(request)),
        # )

        results = self.get_serializer(self.get_queryset(request), many=True).data
        response = {self.response_tag: results}
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        response = {
            "message": "Updated Succesfully",
            "data": serializer.data,
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response = {
            "message": "Deleted Succesfully",
            "data": "deleted",
            "status": status.HTTP_200_OK,
        }
        return Response(response, status=status.HTTP_200_OK)
