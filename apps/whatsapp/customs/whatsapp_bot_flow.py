# # from apps.ticket.models import Installation, Ticket
# from apps.whatsapp.models import WhatsappTempData

# installation = [
#     """
# Enter Your Name""",
#     """
# Enter Your Email""",
#     """
# 1.Please Enter Work Order No. """,
#     """
# 2.Packing slip No.
# """,
#     """
# 3.Equipement Brief
# """,
#     """
# 4.Received In good Condition
# Enter only yes or no
# """,
#     """
# 5.Pre Installation Checking Status
# A.Pending
# B.Ready
# C.During engg visit
# D.Not Understood list
# E.Further Tech Guidance needed
# """,
#     """
# 6.Production Trial readliness date
# """,
# ]
# tickets_msg = {1: installation}


# def MessageGenerator(mobile, msg):
#     whtastapp_history = WhatsappTempData.objects.filter(mobile=mobile)
#     if whtastapp_history.count() > 0:
#         last_obj = whtastapp_history.last()
#         if not last_obj.ticket_type:
#             last_obj.ticket_type = int(msg)
#             last_obj.save()
#             reply = "Please enter Below Fields " + tickets_msg[last_obj.ticket_type][0]

#             return reply
#         else:
#             ticket_type = last_obj.ticket_type
#             if last_obj.field_number is None:
#                 whatsapp = WhatsappTempData.objects.create(
#                     mobile=mobile, field_number=0, ticket_type=ticket_type, data=msg
#                 )
#             else:
#                 field_number = last_obj.field_number + 1
#                 whatsapp = WhatsappTempData.objects.create(
#                     mobile=mobile,
#                     field_number=field_number,
#                     ticket_type=ticket_type,
#                     data=msg,
#                 )
#             try:
#                 reply = (
#                     "Please enter Below Fields "
#                     + tickets_msg[ticket_type][whatsapp.field_number + 1]
#                 )
#             except Exception:
#                 if msg == "yes":
#                     whtastapp_history.delete()

#                 reply = create_last_msg(whtastapp_history)
#             return reply

#     else:
#         reply = """Select anyone option on below this:
#         1.Installation
#         2.Service
#         3.Spares
#         4.Sales Inquiry
#         5.Other
#         6.Repair
#         """
#         WhatsappTempData.objects.create(mobile=mobile)
#     print(reply)
#     return reply


# def create_last_msg(whtastapp_history):
#     msg = ""
#     for i in whtastapp_history[1:]:
#         print(i.ticket_type)
#         msg = msg + "/n" + tickets_msg[i.ticket_type][i.field_number] + "/n"
#         msg += i.data
#     msg = msg + "are you sure want to submit this data"
#     return msg


# def create_ticket(whtastapp_history):
#     kwargs = {}
#     ticket_fields = [
#         "customer_phone_number",
#         "customer_name",
#         "customer_email",
#         "work_order_no",
#         "packing_slip_no",
#         "",
#     ]
#     kwargs[ticket_fields[0]] = whtastapp_history.first().phone
