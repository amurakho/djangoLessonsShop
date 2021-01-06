from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.http import JsonResponse, FileResponse
import io
from reportlab.pdfgen import canvas

from product import models, forms, filters, tasks


class ProductListView(generic.ListView):
    model = models.Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = filters.ProductFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = forms.SearchForm
        return context

    def get_queryset(self):
        if self.request.POST:
            data = self.request.POST.get('search_field')
            return self.model.objects.filter(name__contains=data)
        else:
            return self.model.objects.all()

    def post(self, request, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)


class ProductDetailView(FormMixin, generic.DetailView):
    model = models.Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    form_class = forms.ReviewForm

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['reviews'] = models.Review.objects.filter(product=self.object)
        context['count_form'] = forms.ProductBuyForm()

        viewerd = self.request.session.get('viewerd', [])
        if not self.object.id in viewerd:
            if len(viewerd) >= 5:
                viewerd.pop()
            viewerd.append(self.object.id)
            self.request.session['viewerd'] = viewerd
        return context

    def get_success_url(self):
        return redirect('product_detail', slug=self.object.slug)
    
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        self.object = self.get_object()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):

        models.Review.objects.create(**form.cleaned_data, author=self.request.user, product=self.object)

        query_set = self.object.review_set.all()
        rating = sum([item.stars for item in query_set]) / len(query_set)
        self.object.rating = rating
        self.object.save()
        return self.get_success_url()


def to_bucket(request):
    def create_product_in_bucket(product, bucket):
        product_in_bucket = models.ProductInBucket(product=product,
                                                   count=count,
                                                   one_product_price=product.price,
                                                   bucket=bucket
                                                   )
        product_in_bucket.save()
        return product_in_bucket

    if request.is_ajax() and request.GET:

        bucket_id = request.session.get('bucket')

        product_slug = request.GET.get('product_slug')
        product = models.Product.objects.get(slug=product_slug)

        count = int(request.GET.get('count'))
        if count > product.count or count < 0:
            return JsonResponse('Bad request', status=500)

        bucket, created = models.Bucket.objects.get_or_create(id=bucket_id)

        if created:
            product_in_bucket = create_product_in_bucket(product, bucket)

            request.session['bucket'] = bucket.id

        else:
            try:
                product_in_bucket = bucket.productinbucket_set.get(product=product)
            except product_in_bucket.DoesNotExist:
                product_in_bucket = create_product_in_bucket(product, bucket)
            else:
                product_in_bucket.count += count
                product_in_bucket.save()

    return JsonResponse({'status':'ok'})


def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, filename='hello.pdf')


def subscribe_view(request):

    tasks.send_email_task.delay(request.user)

    return HttpResponse('OK')
