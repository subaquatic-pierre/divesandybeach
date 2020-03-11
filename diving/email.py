from django.template.loader import render_to_string
from django.core.mail import send_mail


class Email:
    def __init__(self, divers, booking_info):
        self.divers = divers
        self.customer_email = booking_info.get('email')
        self.company_email = 'info@divesandybeach.com'
        self.dive_type = booking_info.get('dive_type')
        if booking_info['dive_type'] == 'Shore Dive':
            self.time = booking_info.get('shore_time')
        else:
            self.time = booking_info.get('boat_time')
        self.date = booking_info.get('date')
        self.message = booking_info.get('message')
        self.course = booking_info.get('course')
        self.contact = booking_info.get('contact')
        try:
            self.subject = booking_info['subject']
        except KeyError:
            self.subject = booking_info.get('contact_subject')
        try:
            self.diver_name = divers[0].get('full_name')
        except IndexError:
            self.diver_name = booking_info.get('full_name')
            pass

    @property
    def context(self):
        first_name = self.diver_name.split(' ')[0]
        return {
            'diver_name': first_name,
            'divers': self.divers,
            'main_diver': self.diver_name,
            'booking_id': 12,
            'dive_type': self.dive_type,
            'time': self.time,
            'date': self.date,
            'diver_email': self.customer_email,
            'message': self.message,
            'course': self.course,
            'contact': self.contact
        }

    def send(self):
        msg_plain = self.build_plain_msg()
        msg_html = self.build_html_msg()
        send_mail(self.subject,
                  msg_plain,
                  self.from_email,
                  self.recipients,
                  html_message=msg_html)


class CustomerEmail(Email):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.from_email = self.company_email

    def build_plain_msg(self):
        return render_to_string('diving/email/customer_booking_request_email.txt', self.context)

    def build_html_msg(self):
        return render_to_string('diving/email/customer_booking_request_email.html', self.context)

    def send(self):
        self.recipients = [self.customer_email]
        super().send()


class StaffEmail(Email):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.from_email = self.company_email
        self.subject = f'{self.dive_type} - {self.date} - {self.time}'

    def build_plain_msg(self):
        return render_to_string('diving/email/staff_booking_request_email.txt', self.context)

    def build_html_msg(self):
        return render_to_string('diving/email/staff_booking_request_email.html', self.context)

    def send(self):
        self.recipients = [self.company_email]
        super().send()


class CourseStaffEmail(StaffEmail):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = args[1]['course']
        self.subject = f'Course Booking - {self.course}'
