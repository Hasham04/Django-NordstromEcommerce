import datetime
import json
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse,HttpResponse 
from django.shortcuts import get_object_or_404, reverse, redirect
from django.views import generic,View
from .forms import AddToCartForm, AddressForm,CouponForm,CommentForm
from .models import Product, OrderItem, Address, Payment, Order, Category,Coupon,Comment
from .utils import get_or_set_order_session


class ProductListView(generic.ListView):
    template_name = 'cart/product_list.html'

    def get_queryset(self):
        qs = Product.objects.all()
        category = self.request.GET.get('category', None)
        try:
            search = self.request.GET.get('search')
        except:
            search = ''
        if (search != '' and search is not None ):
            qs = Product.objects.filter(Q(title__icontains = search) |
                           Q(description__icontains = search))
        else:
            qs = Product.objects.all()
        if category:
            qs = qs.filter(Q(primary_category__name=category) |
                           Q(secondary_categories__name=category)).distinct()
            print('this is herer right now')
        return qs
        

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context.update({
            "categories": Category.objects.values("name")
        })
        return context

class ProductDetailView(generic.TemplateView):
    template_name = 'cart/product_detail.html'
    
    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs["slug"])
    
    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product= self.get_object().id
        context['product'] = self.get_object()
        comments = Comment.objects.filter(product=product,reply= None).order_by('-id')
        context['comment_form'] = CommentForm()
        context['form'] = AddToCartForm(product_id= product,request=self.request)
        context['comments'] = comments

        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        context= self.get_context_data()
        if self.request.POST.get('quantity'):
            form = AddToCartForm(self.request.POST or None, product_id= product.id,request=self.request)
            if form.is_valid():
                order = get_or_set_order_session(self.request)
                item_filter = order.items.filter(
                    product=product,
                    colour=form.cleaned_data['colour'],
                    size=form.cleaned_data['size'],
                )
                if item_filter.exists():
                    item = item_filter.first()
                    item.quantity += int(form.cleaned_data['quantity'])                    
                    item.save()
                else:
                    new_item = form.save(commit=False)
                    new_item.product = product
                    new_item.order = order
                    new_item.save()
            if self.request.is_ajax():
                if (self.request.POST.get('quantity')):
                    html = render_to_string('cart/product-form.html',context= context, request= self.request)
                    html2 = render_to_string('cart/cartCount.html',context= context, request= self.request)
                    return JsonResponse({'form': html,'cartcount':html2})

        if self.request.POST.get('content'):
            comment_form = CommentForm(self.request.POST or None) 
            if comment_form.is_valid():
                content = self.request.POST.get('content')
                reply_id = self.request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = Comment.objects.get(id=reply_id)
                comment= Comment.objects.create(product=product,user=self.request.user,content=content,reply=comment_qs)
                comment.save()
            if self.request.is_ajax():
                if (self.request.POST.get('content')):
                    html = render_to_string('cart/comments.html',context= context, request= self.request)
                    print('this is working')
                    return JsonResponse({'form':html})
              #  return redirect(product.get_absolute_url())
        if self.request.is_ajax():
            if self.request.method == 'POST':
                if self.request.POST.get('count'):
                    rating=round((product.rating+int(self.request.POST.get('count')))/2, 1)
                    product.rating = rating
                    product.save()
                    html = render_to_string('cart/ratings.html',context= context, request= self.request)
                    print('this is working')
                    return JsonResponse({'form':html})

class CartView(generic.TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        
        return context


class IncreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity += 1
        order_item.save()
        return redirect("cart:summary")


class DecreaseQuantityView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        return redirect("cart:summary")


class RemoveFromCartView(generic.View):
    def get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()
        return redirect("cart:summary")


class CheckoutView(generic.FormView):
    template_name = 'cart/checkout.html'
    form_class = AddressForm

    def get_success_url(self):
        return reverse("cart:payment")

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        selected_shipping_address = form.cleaned_data.get(
            'selected_shipping_address')
        selected_billing_address = form.cleaned_data.get(
            'selected_billing_address')

        if selected_shipping_address:
            order.shipping_address = selected_shipping_address
        else:
            address = Address.objects.create(
                address_type='S',
                user=self.request.user,
                address_line_1=form.cleaned_data['shipping_address_line_1'],
                address_line_2=form.cleaned_data['shipping_address_line_2'],
                zip_code=form.cleaned_data['shipping_zip_code'],
                city=form.cleaned_data['shipping_city'],
            )
            order.shipping_address = address

        if selected_billing_address:
            order.billing_address = selected_billing_address
        else:
            address = Address.objects.create(
                address_type='B',
                user=self.request.user,
                address_line_1=form.cleaned_data['billing_address_line_1'],
                address_line_2=form.cleaned_data['billing_address_line_2'],
                zip_code=form.cleaned_data['billing_zip_code'],
                city=form.cleaned_data['billing_city'],
            )
            order.billing_address = address

        order.save()
        messages.info(
            self.request, "You have successfully added your addresses")
        return super(CheckoutView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs["user_id"] = self.request.user.id
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context["order"] = get_or_set_order_session(self.request)
        context["couponform"] = CouponForm()
        return context


class PaymentView(generic.TemplateView):
    template_name = 'cart/payment.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        context["PAYPAL_CLIENT_ID"] = settings.PAYPAL_CLIENT_ID
        context['order'] = get_or_set_order_session(self.request)
        context['CALLBACK_URL'] = self.request.build_absolute_uri(
        reverse("cart:thank-you"))
        return context

class ConfirmOrderView(generic.View):
    def post(self, request, *args, **kwargs):
        order = get_or_set_order_session(request)
        body = json.loads(request.body)
        payment = Payment.objects.create(
            order=order,
            successful=True,
            raw_response=json.dumps(body),
            amount=float(body["purchase_units"][0]["amount"]["value"]),
            payment_method='PayPal'
        )
        order.ordered = True
        order.ordered_date = datetime.date.today()
        order.save()
        return JsonResponse({"data": "Success"})

class ThankYouView(generic.TemplateView):
    template_name = 'cart/thanks.html'

class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'order.html'
    queryset = Order.objects.all()
    context_object_name = 'order'

def get_coupon(request,code):
    try:
        coupon= Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request,"This coupon does not exist ")
        return redirect("cart:checkout")

class AddCouponView(View):

    def post(self, request, *args, **kwargs):
        form=CouponForm(self.request.POST or None )
        if form.is_valid():
            try:
                code= form.cleaned_data.get('code')
                order = Order.objects.get(user=request.user,ordered=False)
                order.coupon = get_coupon(self.request,code)
                order.save()
                messages.success(self.request,"Coupon successfully added ")
                return redirect("cart:checkout")

            except ObjectDoesNotExist:
                messages.info(self.request,"You do not have an active order ")
                return redirect("cart:checkout")