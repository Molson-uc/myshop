import braintree
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order
from django.conf import settings

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        # retrieve nonce
        nonce = request.POST.get("payment_method_nonce", None)
        # create and submit transaction
        result = gateway.transaction.sale(
            {
                "amount": "{:.2f}".format(order.get_total_cost()),
                "payment_method_nonce": nonce,
                "options": {"submit_for_settlement": True},
            }
        )
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # launch asynchronous task

            return redirect("payment:done")
        else:
            return redirect("payment:canceled")
    else:
        # generate token
        print(settings.BRAINTREE_MERCHANT_ID)
        client_token = gateway.client_token.generate(
            params={"merchant_account_id": settings.BRAINTREE_MERCHANT_ID}
        )
        return render(
            request,
            "payment/process.html",
            {"order": order, "client_token": client_token},
        )


def payment_done(request):
    return render(request, "payment/done.html")


def payment_canceled(request):
    return render(request, "payment/canceled.html")
