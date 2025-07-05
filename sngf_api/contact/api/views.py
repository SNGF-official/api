from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from sngf_api.contact.api.serializers import ContactSerializer


class ContactCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save()
            current_datetime = now()

            html_content = render_to_string("email/feedback_contact.html", {
                "name": contact.name or "Anonyme",
                "email": contact.customer_email,
                "number": contact.number,
                "message": contact.message,
                "now": current_datetime,
            })

            text_content = f"""
📩 NOUVEAU MESSAGE DE CONTACT – Feedback Client

🧑 Nom :
{contact.name or 'Anonyme'}

📧 Email :
{contact.customer_email or 'Non renseigné'}

📱 Téléphone :
{contact.number or 'Non renseigné'}

🕒 Date :
{current_datetime.strftime('%A %d %B %Y à %H:%M')}

💬 Message :
{contact.message or 'Aucun message'}

────────────────────────────────────
Ce message a été généré via le formulaire de feedback sur sngf-silo.com
"""

            email = EmailMultiAlternatives(
                subject="📩 Nouveau message via le formulaire de feedback (retour client)",
                body=text_content.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=["contact@sngf-silo.com", "tech-ylan@sngf-silo.com"],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"message": "Message reçu avec succès"}, status=201)

        return Response(serializer.errors, status=400)


class ContactSimpleAPIView(APIView):
    permission_classes = []

    def post(self, request):
        data = {
            "name": request.data.get("name"),
            "customer_email": request.data.get("customer_email"),
            "message": request.data.get("message"),
        }
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            contact = serializer.save()
            current_datetime = now()

            html_content = render_to_string("email/feedback_contact.html", {
                "name": contact.name or "Anonyme",
                "email": contact.customer_email,
                "number": contact.number,
                "message": contact.message,
                "now": current_datetime,
            })

            text_content = f"""
📨 MESSAGE RAPIDE DE CONTACT

🧑 Nom :
{contact.name or 'Anonyme'}

📧 Email :
{contact.customer_email or 'Non renseigné'}

🕒 Date :
{current_datetime.strftime('%A %d %B %Y à %H:%M')}

💬 Message :
{contact.message or 'Aucun message'}

────────────────────────────────────
Ce message a été soumis via le formulaire rapide de contact sur sngf-silo.com
"""
            admin_emails = settings.ORDER_NOTIFICATION_EMAILS

            email = EmailMultiAlternatives(
                subject="📨 Nouveau message via formulaire contact pour administration",
                body=text_content.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=admin_emails,
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"message": "Message reçu avec succès"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
