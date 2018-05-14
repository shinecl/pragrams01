from datetime import datetime

from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from usr.models import UserTicketModel


class AuthMiddleware(MiddlewareMixin):

    def process_request(self,request):

        ticket = request.COOKIES.get('ticket')

        if not ticket:
            pass

        userticket = UserTicketModel.objects.filter(ticket=ticket)
        if userticket:
            if userticket[0].ticket_out_time.replace(tzinfo=None) > datetime.utcnow():
                request.user = userticket[0].u_user
            else:
                UserTicketModel.objects.filter(ticket=ticket).delete()
        else:
            return None


