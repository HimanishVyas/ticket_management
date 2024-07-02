# from datetime import datetime
import traceback

from apps.ticket.models import CustomerWiseItem
from apps.ticket.models import Installation as MainInstallation
from apps.ticket.models import OtherService as MainOtherService
from apps.ticket.models import Repair as MainRepair
from apps.ticket.models import SalesInquiry as MainSalesInquiry
from apps.ticket.models import Service as MainService
from apps.ticket.models import SpareDetail as MainSpareDetail
from apps.ticket.models import Spares as MainSpares
from apps.ticket.models import Ticket as MainTicket
import requests

# from apps.user.models import Company
from apps.whatsapp.models import (
    Installation,
    OtherService,
    Repair,
    SalesInquiry,
    Service,
    SpareDetail,
    Ticket,
    WhatsappMsg,
)

installation = [
    """
Enter Your Name""",
    """
Enter Your Email""",
    """
1.Please Enter Work Order No. """,
    """
2.Packing slip No.
""",
    """
3.Equipement Brief
""",
    """
4.Received In good Condition
Enter only yes or no
""",
    """
5.Pre Installation Checking Status
A.Pending
B.Ready
C.During engg visit
D.Not Understood list
E.Further Tech Guidance needed
""",
    """
6.Production Trial readliness date
""",
]
tickets_msg = {1: installation}
models_list = {
    1: Installation,
    2: Service,
    3: SpareDetail,
    4: SalesInquiry,
    5: OtherService,
    6: Repair,
}

# class MyClass:
#     static_var = 0
#
#     def __init__(self):
#         MyClass.static_var += 1
#         self.instance_var = MyClass.static_var
#
# obj1 = MyClass()
# # print(obj1.instance_var)  # Output: 1

# obj2 = MyClass()
count = 0


# def MessageGenerator(mobile, msg):

#     url = "https://f014-180-211-99-146.ngrok-free.app/"
#     global count
#     if str(msg) in ["hi", "Hi", "hello", "Hello", "Help", "help"]:
#         count = 1
#         return (
#             "Hello! How can I assist you? \n 1. Claim Intimation. \n 2. Claim Submission. \n 3. Know your "
#             "Claim Status.")
#     elif str(msg) == "1":
#         return ("Follow This Link to Create New Claim intimation \n "
#                 f"{url}web#cids=1&menu_id=222&action=335&model=claim.intimation&view_type=form")
#     elif str(msg) == "3":
#         count = 3
#         return "Enter your claim intimation number"

#     elif str(msg) == "2":
#         count = 2
#         return "Enter claim intimation number"

#     elif msg and count == 2:
#         count = 2
#         print("here --------------------")
#         url = f"{url}api/raise_claim/{msg}"
#         response = requests.get(url)
#         print("hehehehehehehehehe", response)
#         print("url", url)
#         if response.status_code == 200:
#             test = response.json()["message"]
#             return test
#         else:
#             if response.json["message"]:
#                  return response.json()["message"]
#             else:
#                 return "Claim not available"
#     elif msg and count == 3:
#         count = 3
#         print("here")
#         url = f"{url}api/claims_status/{msg}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json()["message"]

#     else:
#         return "Please enter valid Claim Intimation Number..!"


# Nikhil Here

import requests

# BASE_URL = "https://7ae7-180-211-99-146.ngrok-free.app/"
# count = 0

def MessageGenerator(mobile, msg):

    # url = "https://f014-180-211-99-146.ngrok-free.app/"
    # global count
    # if str(msg) in ["hi", "Hi", "hello", "Hello", "Help", "help"]:
    #     count = 1
    #     return (
    #         "Hello! How can I assist you? \n 1. Claim Intimation. \n 2. Claim Submission. \n 3. Know your "
    #         "Claim Status.")
    # elif str(msg) == "1":
    #     return ("Follow This Link to Create New Claim intimation \n "
    #             f"{url}web#cids=1&menu_id=222&action=335&model=claim.intimation&view_type=form")
    # elif str(msg) == "3":
    #     count = 3
    #     return "Enter your claim intimation number"
    #
    # elif str(msg) == "2":
    #     count = 2
    #     return "Enter claim intimation number"
    #
    # elif msg and count == 2:
    #     count = 2
    #     print("here --------------------")
    #     url = f"{url}api/raise_claim/{msg}"
    #     response = requests.get(url)
    #     print("hehehehehehehehehe", response)
    #     print("url", url)
    #     if response.status_code == 200:
    #         test = response.json()["message"]
    #         return test
    #     else:
    #         if response.json["message"]:
    #              return response.json()["message"]
    #         else:
    #             return "Claim not available"
    # elif msg and count == 3:
    #     count = 3
    #     print("here")
    #     url = f"{url}api/claims_status/{msg}"
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         return response.json()["message"]
    #
    # else:
    #     return "Please enter valid Claim Intimation Number..!"

    if msg.lower() == "yes":
        msg = True
    elif msg.lower() == "no":
        msg = False
    print("msg: ", msg)

    ticket = Ticket.objects.get_or_create(
        current_mobile_no=mobile, defaults={"current_mobile_no": mobile}
    )
    first_time_ticket = ticket[1]
    ticket = ticket[0]
    ticket_models = Ticket._meta.get_fields()
    ticket_fields = [field.name for field in ticket_models if field.concrete]
    for i in ticket_fields:  # first models save msg
        if first_time_ticket:
            break
        if getattr(ticket, i) is None:
            try:
                if i == "ticket_type":
                    msg = int(msg)
                setattr(ticket, i, msg)
                ticket.save()
                break
            except Exception:
                break
            finally:
                ticket.refresh_from_db()
    for i in ticket_fields:  # first models send msg
        if getattr(ticket, i) is None:
            reply = WhatsappMsg.objects.filter(key=i).first().msg
            return reply
    if ticket.ticket_type == 3:
        print(SpareDetail.objects.filter(ticket_fk=ticket))
        sub_model = SpareDetail.objects.filter(ticket_fk=ticket).last()
        is_first_time = False
        if not sub_model:
            sub_model = SpareDetail.objects.create(ticket_fk=ticket)
            is_first_time = True
    else:
        sub_model = models_list[ticket.ticket_type].objects.get_or_create(
            ticket_fk=ticket, defaults={"ticket_fk": ticket}
        )
        # The above code is declaring a variable named "is_first_time".
        is_first_time = sub_model[1]
        sub_model = sub_model[0]
    sub_model_fields = models_list[ticket.ticket_type]._meta.get_fields()
    sub_model_field = [field.name for field in sub_model_fields if field.concrete]
    sub_model_verbose_field = [
        field.verbose_name for field in sub_model_fields if field.concrete
    ]
    print("sub_model : ", sub_model)
    print("sub_model_fields : ", sub_model_fields)
    print("sub_model_field : ", sub_model_field)
    print("sub_model_verbose_field : ", sub_model_verbose_field)
    if is_first_time:
        for j in sub_model_field:
            if getattr(sub_model, j) is None:
                reply = WhatsappMsg.objects.filter(key=j).first().msg
                return reply
    for i in sub_model_field:  # second models save msg
        print("HERE ------------------->>>", i)
        print("HELLO ------------------->>>", getattr(sub_model, i))
        if getattr(sub_model, i) is None:
            print("HERE ================>>>", i)
            try:
                print("in try msg :", msg)
                setattr(sub_model, i, msg)
                print("setatter ========= >>>", setattr(sub_model, i, msg))

                if i == "packing_slip_no":
                    if CustomerWiseItem.objects.filter(
                            packing_slip_no__iexact=str(msg)
                    ).exists():
                        sub_model.save()
                    else:
                        return (
                            WhatsappMsg.objects.filter(key="packing_slip_no_error")
                            .first()
                            .msg
                        )

                elif i == "SerialNo":
                    if CustomerWiseItem.objects.filter(
                            SerialNo__iexact=str(msg)
                    ).exists():
                        sub_model.save()

                    else:
                        return (
                            WhatsappMsg.objects.filter(key="SerialNo_error").first().msg
                        )
                # elif i == "installation_drop_down":
                #     print("msg : ", WhatsappMsg.objects.filter(key="installation_drop_down").first().msg)
                #     return (
                #         WhatsappMsg.objects.filter(key="installation_drop_down").first().msg
                #     )
                # if msg ==

                else:
                    print("---------------IN ELSE---------------")
                    sub_model.save()
                # else:
                #     sub_model.save()
                if i == "add_another_record" and msg == True:
                    SpareDetail.objects.create(ticket_fk=ticket)
                    return WhatsappMsg.objects.filter(key="part_name").first().msg
                break
            except Exception:
                traceback.print_exc()
                break
            finally:
                sub_model.refresh_from_db()

    for j in sub_model_field:  # second models send msg
        if getattr(sub_model, j) is None:
            reply = WhatsappMsg.objects.filter(key=j).first().msg
            return reply
    count = 1
    print("HHHHHHHHHHHHHHHHHHHHHH", ticket.is_saved)
    if ticket.is_saved == False:
        print("____________________HERE in IS SAVE IF____________________")
        if ticket.ticket_type == 3:
            ticket.is_saved = True
            ticket.save()
            spare_detial = SpareDetail.objects.filter(ticket_fk=ticket)
            reply = ""
            for spare in spare_detial:
                for j, k in zip(
                        sub_model_field, sub_model_verbose_field
                ):  # second models send msg
                    if j in ["id", "ticket_fk", "add_another_record"]:
                        continue
                    data = getattr(spare, j)
                    if data == True:
                        data = "yes"
                    if data == False:
                        data = "no"
                    reply = reply + f"{count}. " + k + "\n"
                    reply = reply + f"{data}" + "\n\n"
                    count = count + 1
                count = 1
                reply = reply + "---------------" + "\n"
            return f"""REVIEW THE DETAIL ENTERD BY YOU \n{reply}DO YOU WANTS TO SAVE/CREATE TICKET OR DELETE TICKET \n TYPE "SAVE" FOR SAVE AND "DELETE" FOR DELETE TICKET
            """
        else:
            ticket.is_saved = True
            ticket.save()
            reply = ""
            for j, k in zip(
                    sub_model_field, sub_model_verbose_field
            ):  # second models send msg
                if j in ["id", "ticket_fk"]:
                    continue
                data = getattr(sub_model, j)
                if data == True:
                    data = "yes"
                if data == False:
                    data = "no"
                reply = reply + f"{count}. " + k + "\n"
                reply = reply + f"{data}" + "\n\n"
                count = count + 1
            return f"""REVIEW THE DETAIL ENTERD BY YOU \n{reply}DO YOU WANTS TO SAVE/CREATE TICKET OR DELETE TICKET \n TYPE "SAVE" FOR SAVE AND "DELETE" FOR DELETE TICKET
            """

    if msg.lower() == "save":
        ticket = create_ticket_whatsapp(ticket=ticket, sub_model=sub_model)
        return f"""TICKET CREATED SUCCESSFULLY
YOUR TICKET NUMBER IS *{ticket.ticket_number}*
        """

    elif msg.lower() == "delete":
        sub_model.delete()
        ticket.delete()
        return "TICKET DELETED SUCCESSFULLY \n DO YOU WANT TO CREATE OTHER TICKET"
    # return "Are you Sure you want to store this details
    else:
        return "PLEASE WRITE ONLY SAVE OR DELETE"

#     global count
#     msg = str(msg).lower()  # Convert message to lowercase for case-insensitive comparisons
#     if msg in ["hi", "hello", "help","HI","Hi"]:
#         count = 1
#         return "Hello! How can I assist you?\n1. Claim Intimation.\n2. Claim Submission.\n3. Know your Claim Status."
#     elif msg == "1":
#         return f"Follow this link to create a new claim intimation:\n{BASE_URL}web#cids=1&menu_id=222&action=335&model=claim.intimation&view_type=form"
#     elif msg == "3":
#         count = 3
#         return "Enter your claim intimation number"
#     elif msg == "2":
#         count = 2
#         return "Enter claim intimation number"
#     elif count == 2:
#         count = 2
#         url = f"{BASE_URL}api/raise_claim/{msg}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             test = response.json().get("message", "Claim not available")
#             return test
#         else:
#             return response.json().get("message", "Claim not available")
#     elif count == 3:
#         count = 3
#         url = f"{BASE_URL}api/claims_status/{msg}"
#         response = requests.get(url)
#         if response.status_code == 200:
#             return response.json().get("message", "Claim not available")
#     else:
#         return "Please enter a valid Claim Intimation Number..!"

# Nikhil End




# def MessageGenerator(mobile, msg, message_time):
#     print("message_time: ", message_time)
#     print("mobile: ", mobile)
#     print("msg: ", msg)

#     dt2 = datetime.now()
#     print("Date and Time is:", dt2)
#     # convert timestamps to datetime object

#     # time = message_time
#     time = 1690898095
#     dt1 = datetime.fromtimestamp(time)
#     print("Datetime Start:------------", dt1)
#     print("Datetime End:--------------", dt2)

#     # Difference between two timestamp in hours:minutes:seconds format
#     delta = dt2 - dt1
#     print("Difference is:-----------", delta)

#     whatsapp_tempdata = WhatsappTempData.objects.filter(mobile=mobile).first()
#     print("whatsapp_tempdata: ", whatsapp_tempdata)
#     # if whatsapp_tempdata and whatsapp_tempdata.msg_step is not 0:
#     if whatsapp_tempdata and whatsapp_tempdata.msg_step != 0:
#         if whatsapp_tempdata.msg_step == 1:
#             print("in if")
#             try:
#                 whatsapp_tempdata.ticket_type = int(msg)
#                 whatsapp_tempdata.save()

#             except Exception:
#                 print("in except")
#                 whatsapp_tempdata.msg_step = whatsapp_tempdata.msg_step - 1
#                 whatsapp_tempdata.save()
#                 reply = """Select anyone option on below this:
#                 1.Installation
#                 2.Service
#                 3.Spares
#                 4.Sales Inquiry
#                 5.Other
#                 6.Repair
#                 """
#                 return reply
#             whatsapp_tempdata.msg_step = whatsapp_tempdata.msg_step + 1
#             whatsapp_tempdata.save()
#             reply = "enter mobile number"
#             return reply
#         elif whatsapp_tempdata.msg_step == 2:
#             MoNo = msg
#             print("MoNo: ", MoNo)

#     else:
#         print("in else")
#         WhatsappTempData.objects.update_or_create(
#             mobile=mobile, msg_step=1, defaults={"mobile": mobile}
#         )
#         reply = """Select anyone option on below this:
#         1.Installation
#         2.Service
#         3.Spares
#         4.Sales Inquiry
#         5.Other
#         6.Repair
#         """

#         return reply


def create_ticket_whatsapp(ticket, sub_model):
    kwargs = {}
    print("Ticket : ", ticket)
    print("sub_model : ", sub_model)
    if ticket.ticket_type == 1:
        customer_wise_item = CustomerWiseItem.objects.filter(
            packing_slip_no=sub_model.packing_slip_no
        )
        print("customer_wise_item")
        print(customer_wise_item)
        for i in customer_wise_item:
            print("FIRST FOR LOOP", i)
        main_ticket = MainTicket.objects.create(
            ticket_type=ticket.ticket_type,
            mobile_no=ticket.mobile_no,
            address=ticket.address,
            customer_fk=customer_wise_item.first().customer_user,
            is_guest=True,
        )
        print(main_ticket)
        for i in customer_wise_item:
            print("HERE IN LOOP ------------ >>>", i)
            main_ticket.customer_wise_item.add(i)

    elif ticket.ticket_type in [2, 6]:
        customer_wise_item = CustomerWiseItem.objects.filter(SerialNo=sub_model.SerialNo)
        main_ticket = MainTicket.objects.create(
            ticket_type=ticket.ticket_type,
            mobile_no=ticket.mobile_no,
            address=ticket.address,
            customer_fk=customer_wise_item.first().customer_user,
            is_guest=True,
        )
        for i in customer_wise_item:
            main_ticket.customer_wise_item.add(i)
    else:
        main_ticket = MainTicket.objects.create(
            ticket_type=ticket.ticket_type,
            mobile_no=ticket.mobile_no,
            address=ticket.address,
            is_guest=True,
        )

    if ticket.ticket_type == 1:
        sub_model_pending = None
        sub_model_ready = None
        sub_model_during_enginner_visit = None
        sub_model_not_understood_list = None
        sub_model_further_guideliness_needed = None
        if sub_model.installation_drop_down == "1":  # pending
            sub_model_pending = True
            sub_model_ready = False
            sub_model_during_enginner_visit = False
            sub_model_not_understood_list = False
            sub_model_further_guideliness_needed = False
        elif sub_model.installation_drop_down == "2":  # ready
            sub_model_pending = False
            sub_model_ready = True
            sub_model_during_enginner_visit = False
            sub_model_not_understood_list = False
            sub_model_further_guideliness_needed = False
        elif sub_model.installation_drop_down == "3":  # during_enginner_visit
            sub_model_pending = False
            sub_model_ready = False
            sub_model_during_enginner_visit = True
            sub_model_not_understood_list = False
            sub_model_further_guideliness_needed = False
        elif sub_model.installation_drop_down == "4":  # not_understood_list
            sub_model_pending = False
            sub_model_ready = False
            sub_model_during_enginner_visit = False
            sub_model_not_understood_list = True
            sub_model_further_guideliness_needed = False
        elif sub_model.installation_drop_down == "5":  # further_guideliness_needed
            sub_model_pending = False
            sub_model_ready = False
            sub_model_during_enginner_visit = False
            sub_model_not_understood_list = False
            sub_model_further_guideliness_needed = True

        MainInstallation.objects.create(
            ticket_fk=main_ticket,
            work_order_no=sub_model.work_order_no,
            packing_slip_no=sub_model.packing_slip_no,
            receive_in_good_condition=sub_model.receive_in_good_condition,
            equipement_brief=sub_model.equipement_brief,
            product_trial_readliness_date=sub_model.product_trial_readliness_date,
            pending=sub_model_pending,
            ready=sub_model_ready,
            during_enginner_visit=sub_model_during_enginner_visit,
            not_understood_list=sub_model_not_understood_list,
            further_guideliness_needed=sub_model_further_guideliness_needed,
        )
    if ticket.ticket_type == 2:
        sub_model_temporary_running = None
        sub_model_running_with_rejection = None
        sub_model_breakdown = None
        if sub_model.service_drop_down == "1":  # temporary_running
            sub_model_temporary_running = True
            sub_model_running_with_rejection = False
            sub_model_breakdown = False

        elif sub_model.service_drop_down == "2":  # running_with_rejection
            sub_model_temporary_running = False
            sub_model_running_with_rejection = True
            sub_model_breakdown = False

        elif sub_model.service_drop_down == "3":  # breakdown
            sub_model_temporary_running = False
            sub_model_running_with_rejection = False
            sub_model_breakdown = True

        MainService.objects.create(
            ticket_fk=main_ticket,
            problem_brief=sub_model.problem_brief,
            temporary_running=sub_model_temporary_running,
            running_with_rejection=sub_model_running_with_rejection,
            breakdown=sub_model_breakdown,
        )
    if ticket.ticket_type == 4:
        MainSalesInquiry.objects.create(
            ticket_fk=main_ticket,
            inquiry_brief=sub_model.inquiry_brief,
            process_type=sub_model.process_type,
            max_kg=sub_model.max_kg,
        )
    if ticket.ticket_type == 5:
        MainOtherService.objects.create(
            ticket_fk=main_ticket,
            equipment_name=sub_model.equipment_name,
            quary_brief=sub_model.query_brief,
        )
    if ticket.ticket_type == 6:
        MainRepair.objects.create(
            ticket_fk=main_ticket,
            courier_name=sub_model.courier_name,
            courier_mobile_no=sub_model.courier_mobile_no,
        )
    if ticket.ticket_type == 3:
        spare = MainSpares.objects.create(ticket_fk=main_ticket)
        spare_detail = SpareDetail.objects.filter(ticket_fk=ticket)
        for i in spare_detail:
            MainSpareDetail.objects.create(
                spare=spare,
                part_name=i.part_name,
                part_desciption=i.part_desciption,
                qunatity=i.qunatity,
            )
        spare_detail.delete()
        ticket.delete()
        return main_ticket
    sub_model.delete()
    ticket.delete()
    return main_ticket
