from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
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

            html_content = render_to_string("email/feedback_contact.html", {
                "name": contact.name or "Anonyme",
                "email": contact.customer_email,
                "number": contact.number,
                "message": contact.message,
            })

            text_content = f"""
    Nouveau message de contact :

    Nom : {contact.name or 'Anonyme'}
    Email : {contact.customer_email}
    Téléphone : {contact.number}
    Message :
    {contact.message}
                """

            email = EmailMultiAlternatives(
                subject="📩 Nouveau message via le formulaire de contact",
                body=text_content.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=["support@soibytrust.com"],
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

            html_content = render_to_string("email/feedback_contact.html", {
                "name": contact.name or "Anonyme",
                "email": contact.customer_email,
                "number": contact.number,
                "message": contact.message,
            })

            text_content = f"""
            Message contact :
            Nom : {contact.name or 'Anonyme'}
            Email : {contact.customer_email}
            Message :
            {contact.message}
            """

            email = EmailMultiAlternatives(
                subject="📨 Nouveau message via formulaire contact rapide",
                body=text_content.strip(),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=["support@soibytrust.com"],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            return Response({"message": "Message reçu avec succès"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
