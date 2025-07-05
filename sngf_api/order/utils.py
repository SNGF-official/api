from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now

from sngf_api.plant.models import Seed, Plant


def send_order_confirmation_email(order):
    now_dt = now().strftime("%d/%m/%Y %H:%M")
    items = []

    for item in order.items.all():
        if item.type == "SEED":
            item.seed = Seed.objects.filter(id=item.product_id).first()
        else:
            item.plant = Plant.objects.filter(id=item.product_id).first()
        items.append(item)

    total_order_amount = sum(
        float(item.price) * int(item.quantity)
        for item in items
        if item.price and item.quantity
    )

    plain_lines = []
    for item in items:
        if item.type == "SEED":
            name = getattr(item.seed, "scientific_name", "Graine inconnue")
            unit_price = f"{item.seed.price_per_kilo:.0f} Ar/kg" if item.seed else "-"
            size_label = "-"
        else:
            name = getattr(item.plant, "scientific_name", "Plante inconnue")
            size_map = {"PM": "Petit modèle", "MM": "Modèle moyen", "GM": "Grand modèle"}
            size_label = size_map.get(item.size, item.size or "-")
            unit_price = f"{item.price:.0f} Ar"

        total_price = item.price * item.quantity
        plain_lines.append(
            f"- Produit : {name} | Type : {'Graine' if item.type == 'SEED' else 'Plante'} | "
            f"Quantité : {item.quantity} {item.unit or ''} | Taille : {size_label} | "
            f"Prix unitaire : {unit_price} | Total : {total_price:.0f} Ar"
        )

    plain_body = f"""
    Nouvelle commande reçue le {now_dt}

    Client :
    - Nom : {order.contact_name}
    - Email : {order.contact_email}
    - Téléphone : {order.contact_number}

    Commande :
    {chr(10).join(plain_lines)}

    Merci de vérifier dans l'administration de SNGF.
    """

    html_body = render_to_string("email/order_confirmation.html", {
        "order": order,
        "items": items,
        "now": now_dt,
        "total": f"{total_order_amount:.2f}",
    })

    subject = f"Nouvelle commande au nom de #{order.contact_name}"
    admin_emails = settings.ORDER_NOTIFICATION_EMAILS
    from_email = order.contact_email or settings.DEFAULT_FROM_EMAIL

    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_body.strip(),
        from_email=from_email,
        to=admin_emails,
    )
    email.attach_alternative(html_body, "text/html")
    email.send()
