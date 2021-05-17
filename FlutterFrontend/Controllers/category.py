from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from database.models import *
from ..utils import *

@csrf_exempt
@require_http_methods(["GET"])
def category(req):
    categories = Category.objects.order_by("category_id").values()
    return jsonify(list(categories), status_code=200)