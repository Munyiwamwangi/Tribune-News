from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(name, receiver):
	#creating message subject and sender
	subject = 'Welcome to Moringa highlights Newsletter'
	sender = 'james@moringaschool.com'

	#passing in the context variables
	text_context = render_to_string('email/newsemail.html',{"name":name})
	html_content = render_to_string('email/newsemail.html',{"name":name})
	msg = EmailMultiAlternatives(subject,text_context,sender,[receiver])
	msg.attach_alternative(html_content,'text/html')
	msg.send()