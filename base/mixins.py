import xlrd
import tablib
import datetime
from django.http import HttpResponse
from django.conf import settings
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from base.response import json_api_response



class BulkCreateModelMixin(CreateModelMixin):
    """
    Either create a single or many model instances in bulk by using the
    Serializers ``many=True`` ability from Django REST >= 2.2.5.
    .. note::
        This mixin uses the same method to create model instances
        as ``CreateModelMixin`` because both non-bulk and bulk
        requests will use ``POST`` request method.
    """
    # https://github.com/miki725/django-rest-framework-bulk/blob/master/rest_framework_bulk/drf3/mixins.py

    def create(self, request, *args, **kwargs):
        bulk = isinstance(request.data, list)

        if not bulk:
            return super(BulkCreateModelMixin, self).create(request, *args, **kwargs)

        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_bulk_create(self, serializer):
        return self.perform_create(serializer)


class BulkUpdateModelMixin(object):
    """
    Update model instances in bulk by using the Serializers
    ``many=True`` ability from Django REST >= 2.2.5.
    """

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        if lookup_url_kwarg in self.kwargs:
            return super(BulkUpdateModelMixin, self).get_object()

        # If the lookup_url_kwarg is not present
        # get_object() is most likely called as part of options()
        # which by default simply checks for object permissions
        # and raises permission denied if necessary.
        # Here we don't need to check for general permissions
        # and can simply return None since general permissions
        # are checked in initial() which always gets executed
        # before any of the API actions (e.g. create, update, etc)
        return

    def bulk_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        # restrict the update to the filtered queryset
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()),
            data=request.data,
            many=True,
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_bulk_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.bulk_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()

    def perform_bulk_update(self, serializer):
        return self.perform_update(serializer)


class TreeListMixin(object):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset.filter(parent=None), many=True).data
        for instance in data:
            instance['children'] = self.set_children_nodes(instance["id"], queryset)

        return json_api_response(code=0, data=data, message=None)

    def set_children_nodes(self, pk, qs):
        children_set = qs.filter(parent=pk)  # ???2??? ops, ter, prt
        children_data = self.get_serializer(children_set, many=True).data
        for child in children_data:
            child_qs = qs.filter(parent=child['id'])  # ???3??? monkey, api-gw
            if child_qs.exists():
                child['children'] = self.set_children_nodes(child['id'], qs)
        return children_data


class ExportMixin(object):
    @action(methods=['get'], detail=False)
    def export_data(self, request):
        '''
        ????????????<br>
            query_params:<br>
                file_format: ???????????????xls???csv???json???html???yaml????????????xls<br>
                filename: ?????????????????????download.xls<br>
                scope: ???????????????all???header_only???selected (?????????????????????????????????)????????????all<br>

        '''
        resource = self.resource_class()
        model = resource._meta.model
        file_format = request.query_params.get('file_format', 'xls')
        filename = request.query_params.get('filename', '{}-{}.{}'.format(model._meta.model_name,
                                                                          datetime.datetime.now().strftime('%Y-%m-%d'),
                                                                          file_format))
        scope = request.query_params.get('scope', 'all')
        ids = request.query_params.get('ids', '')
        if scope == 'all':
            queryset = self.filter_queryset(self.get_queryset())
        elif scope == 'header_only':
            queryset = []
        elif scope == 'selected':
            queryset = []
            if ids: queryset = self.filter_queryset(self.get_queryset().filter(pk__in=ids.split(',')))
        export_data = resource.export(queryset)
        export_data.title = model._meta.verbose_name
        content_type = '{};charset=gbk'.format(settings.CONTENT_TYPE[file_format])
        response = HttpResponse(getattr(export_data, file_format), content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(label="????????????", help_text="????????????", required=True)


class ImportMixin(object):
    import_data_serializer_class = UploadSerializer

    def create_dataset(self, in_stream, format, **kwargs):
        dataset = tablib.Dataset()
        if format == 'json': dataset.json = in_stream
        if format == 'csv': dataset.csv = in_stream
        if format == 'xls':
            xls_book = xlrd.open_workbook(file_contents=in_stream)
            sheet = xls_book.sheets()[0]
            dataset.headers = sheet.row_values(0)
            for i in moves.range(1, sheet.nrows):
                dataset.append(sheet.row_values(i))
        return dataset

    @action(methods=['post'], detail=False)
    def import_data(self, request):
        '''
        ????????????<br>
            param???<br>
                file: ??????: json???csv???xls?????????????????????: xls??????<br>
        '''
        file_format = request.query_params.get('file_format', 'xls')
        import_file = request.FILES['file']
        resource = self.resource_class()
        dataset = self.create_dataset(import_file.read(), file_format)
        result = resource.import_data(dataset, dry_run=True)
        if result.has_errors():
            errors = ['{}:{}'.format(row[1][0].error, str(row[1][0].row)) for row in result.row_errors()]
            return Response({"detail": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = resource.import_data(dataset, dry_run=False)
        return Response(result.totals)

    @action(methods=['post'], detail=False)
    def import_json_data(self, request):
        '''
        ??????JSON????????????<br>
            param???<br>
                jsondata: json??????<br>
        '''
        data = request.data['jsondata']
        resource = self.resource_class()
        dataset = tablib.Dataset()
        dataset.json = data
        result = resource.import_data(dataset, dry_run=True)
        if result.has_errors():
            errors = [str(row[1][0].error) for row in result.row_errors()]
            return Response({"detail": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            result = resource.import_data(dataset, dry_run=False)
        return Response(result.totals)
