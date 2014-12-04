from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from api.models import Tag

class TagViewSet(ViewSet):

    def list(self, request):
        site_name = request.GET.get('community')
        tags = Tag(site_name)
        return Response(tags.get_all(pk))        

    def retrieve(self, request, pk=None):
        site_name = request.GET.get('community')
        tags = Tag(site_name)
        return Response(tags.get_by_name(pk))