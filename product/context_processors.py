from product import models, forms

def get_viewerd(request):
    viewerd = request.session.get('viewerd', [])
    viwered_prodcuts = []
    for item in viewerd:
        try:
            obj = models.Product.objects.get(id=item)
        except models.Product.DoesNotExist:
            pass
        else:
            viwered_prodcuts.append(obj)

    bucket_id = request.session.get('bucket', 0)
    try:
        bucket = models.Bucket.objects.get(id=bucket_id)
    except models.Bucket.DoesNotExist:
        bucket = None

    return {
        'viwered_prodcuts': viwered_prodcuts,
        'bucket': bucket
    }