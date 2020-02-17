from django.template.loader import render_to_string
from django.core.mail import send_mail


class Email:
    def __init__(self, divers, booking_info):
        self.divers = divers
        self.customer_email = booking_info['email']
        self.company_email = 'info@divesandybeach.com'
        self.subject = booking_info['subject']
        self.diver_name = divers[0]['full_name']
        self.dive_type = booking_info['dive_type']
        self.time = booking_info.get('time', None)
        self.date = booking_info['date']
        self.message = booking_info['message']
        self.course = booking_info.get('course', None)

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
            'course': self.course}

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
        self.from_email = self.customer_email
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
        print(args)
        self.course = args[1]['course']
        self.subject = f'Course Booking - {self.course}'
