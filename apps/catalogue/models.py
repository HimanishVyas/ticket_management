import re
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image, ImageDraw, ImageFont
from django.core.files import File
from io import BytesIO
from django.db.models.signals import post_save
import qrcode
# Create your models here.

def validate_phone_number(value):
    # Check if the value contains only digits and the first digit is between 6 and 9
    if not re.match(r"^[6-9]\d*$", value):
        raise ValidationError(
            "Invalid phone number. Phone numbers can only contain digits, and the first digit should be between 6 and 9."
        )

class Catalogue(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    qr_image = models.ImageField(
        _("QR Image"),
        upload_to="media/QR",
        height_field=None,
        width_field=None,
        max_length=None,
        null=True,
        blank=True,
    )
    urls = models.CharField(_("URL"),max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)


    def __str__(self):
        return str(self.id)
    
    # @classmethod
#     def post_create(cls, sender, instance, created, *args, **kwargs):
#         print("===========>>>", instance.urls)
#         if created:
#             qr_image = qrcode.make("https://3213-180-211-99-146.ngrok-free.app/catalogue/" + str(instance.id))
#             qr_offset = Image.new("RGB", (410, 410), "white")
#             ImageDraw.Draw(qr_offset)
#             qr_offset.paste(qr_image)
#             file_name = f"{instance.id}.png"
#             stream = BytesIO()
#             qr_offset.save(stream, "PNG")
#             instance.qr_image.save(file_name, File(stream), save=False)
#             qr_offset.close()
#             instance.save()

# post_save.connect(Catalogue.post_create, sender=Catalogue)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        print("post_create signal triggered")
        try:
            # if created:
            #     # Generate QR code
            #     qr_data = "https://3213-180-211-99-146.ngrok-free.app/catalogue/" + str(instance.id)
            #     qr_image = qrcode.make(qr_data)

            #     # Save the image to a BytesIO buffer
            #     buffer = BytesIO()
            #     qr_image.save(buffer, "PNG")

            #     # Create or update the ImageField with the QR code
            #     file_name = f"{instance.id}.png"
            #     instance.qr_image.save(file_name, File(buffer), save=True)

            if created:
                # Generate QR code
                qr_data = "http://staging-india.csm.conairgroup.in:8069/catalogue/" + str(instance.id)
                qr_image = qrcode.make(qr_data)

                font_path = "arial"  # Replace with the path to your TrueType font file
                font_size = 20
                font = ImageFont.load_default()
                # Add text below the QR code
                draw = ImageDraw.Draw(qr_image)
                # font = ImageFont.load_default()  # You can use a custom font if needed
                text = f"Catalogue Name: {instance.name}"
                text_width, text_height = draw.textsize(text, font)
                text_position = ((qr_image.width) * 4, qr_image.height - text_height - 10)
                # text_position = ((qr_image.width - text_width) // 2, qr_image.height - text_height - 10)
                draw.text(text_position, text, fill="black", font=font)

                # Save the image to a BytesIO buffer
                buffer = BytesIO()
                qr_image.save(buffer, "PNG")

                # Create or update the ImageField with the QR code
                file_name = f"{instance.id}.png"
                instance.qr_image.save(file_name, File(buffer), save=True)

        except Exception as e:
            print(f"Error in post_create: {e}")

post_save.connect(Catalogue.post_create, sender=Catalogue)
    

class Visitor(models.Model):
    catalogue_fk = models.ForeignKey(Catalogue,verbose_name=_("Catalogue"),on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"), max_length=100)
    mobile = models.CharField(_("Mobile"), max_length=10, validators=[validate_phone_number])
    company_name = models.CharField(_("Company Name"), max_length=100)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    def __str__(self):
        return self.name