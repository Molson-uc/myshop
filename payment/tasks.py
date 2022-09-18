from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def peyment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"Mój sklep - rachunek nr {order.id}"
    message = "W załączniku przesyłam rachunek dla ostatniego zakupu."
    email = EmailMessage(subject, message, "admin@myshop.com", [order.email])
    html = render_to_string("orders/order/pdf.html", {"order": order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + "css/pdf.css")]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
    email.attach("order_{}.pdf".format(order.id), out.getvalue(), "application/pdf")
    email.send()
