from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from nuvu.settings import BASE_DIR
from rest_framework import serializers
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    context_dict["path"] = BASE_DIR
    html = template.render(context_dict)
    print("--------------------------------")
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


class RequiredFields:
    required_fields = []
    required_fields_methods = []

    def check_required_fields(self, request):
        for field in self.required_fields:
            if field not in request.data:
                message = f"{field} is a required field"
                raise serializers.ValidationError({"Error": message})
