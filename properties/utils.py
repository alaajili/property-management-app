from django.core.mail import send_mail

def send_payment_notification_email(tenant, payment):
	"""
	Send an email to the tenant to notify them of an upcoming payment
	"""

	subject = 'Payment Due Reminder'
	message = f'Hi {tenant.name},\n\nThis is a reminder that your payment of {payment.amount} is due on {payment.due_date}. Please make sure to settle it on time.\n\nBest regards,\nProperty Management Team'
	from_email = 'no-reply@test.com'
	recipient_list = [tenant.email]
	send_mail(subject, message, from_email, recipient_list, fail_silently=False)