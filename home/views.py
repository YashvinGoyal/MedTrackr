from django.shortcuts import render,redirect,HttpResponse
from home.models import feedback,Medical,Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from django.utils import timezone
import smtplib
import uuid,os
from django.conf import settings
from django.core.mail import send_mail
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
import pytz
# Create your views here.
# when you have to use redirect function use it with name that you have given in path in url.py like redirect('fake')

SCOPES = ["https://www.googleapis.com/auth/calendar"]
#     flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes=SCOPES)
#     credentials=flow.run_local_server()
#     pickle.dump(credentials,open("token.pkl","wb"))
#     credentials=pickle.load(open("token.pkl","rb"))


def main(cont,cont1,time,email):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        
        #To see list of events in calender:
        # now = datetime.now().isoformat()+"Z"
        # event_result = service.events().list(calendarId="primary", timeMin=now,
        #                                      maxResults=10, singleEvents=True, orderBy="startTime").execute()
        # events = event_result.get('items', [])
        # if not events:
        #     print("No upcoming events")
        # for eve in events:
        #     start = eve["start"].get("dateTime", eve["start"].get("date"))
        #     print(start, eve["summary"])
        # }
        
        # if time and date are not in sting format: 
        # local_timezone = pytz.timezone('Asia/Kolkata')
        # local_offset = timedelta(hours=5, minutes=30)
        # start_time_local = local_timezone.localize(datetime(2023, 7, 1, 9, 0, 0))+local_offset
        # end_time_local = local_timezone.localize(datetime(2023, 7, 1, 14, 0, 0))+local_offset
        
        
        #if time and date are in string format:
        date_string = timezone.now().date().strftime('%Y-%m-%d')
        time_string = time
        # time_stringg = st+timedelta(hours=0,minutes=45)
        # Parse the date and time string
        event_date = datetime.strptime(date_string, '%Y-%m-%d')
        event_time = datetime.strptime(time_string, '%H:%M')
        # eventt_time= datetime.strptime(time_stringg, '%H:%M')
        # Combine the date and time into a single datetime object
        event_datetime = datetime.combine(event_date.date(), event_time.time())
        event_datetime1=datetime.combine(event_date.date(), event_time.time())
        # Set the start and end times in the local time zone (Asia/Kolkata)
        local_timezone = 'Asia/Kolkata'
        start_time_local = event_datetime + timedelta(hours=5, minutes=30)
        end_time_local = event_datetime1 + timedelta(hours=5, minutes=60)
        
        # Convert the start and end times to UTC
        start_time_utc = start_time_local.astimezone(pytz.utc)
        end_time_utc = end_time_local.astimezone(pytz.utc)
        event = {
            'summary': f'{cont}',
            'location': 'Your House',
            'description': f'{cont1}',
            'start': {
                'dateTime': start_time_utc.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_time_utc.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=15'
            ],
            # 'attendees': [
            #     {'email': 'lpage@example.com'},
            #     {'email': 'sbrin@example.com'},
            # ],
            # 'reminders': {
            #     'useDefault': False,
            #     'overrides': [
            #         {'method': 'email', 'minutes': 24 * 60},
            #         {'method': 'popup', 'minutes': 10},
            #     ],
            # },
        }
        # generate event at specfic email id:
        eve = service.events().insert(calendarId=email, body=event).execute()
        
        # generate event on developer email id:
        # eve = service.events().insert(calendarId="primary", body=event).execute()
        # print(f'jfjsdj'%{eve.get('htmlLink')})

    except HttpError as err:
        print(err)


def home(request):
    return render(request,'base.html')

def feedbackk(request):
    if request.method=='POST':
        emaill=request.POST['emaill']
        namee=request.POST['namee']   
        phone=request.POST['phonee']
        text=request.POST['textt']
        fedd=feedback(email=emaill,name=namee,phone=phone,text=text)
        fedd.save()
        return redirect('home')

def fakd_login(request):
    return render(request,'login.html')
def verify(request,auth_token):
    try:
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                return redirect('home')
            else:
                profile_obj.is_verified=True
                profile_obj.save()
                return redirect('home')
        else:
            return HttpResponse("404-NOT FOUND")   
    except Exception as e:
        print(e)
        return redirect('home')
        
    
def loginn(request):
    if request.method=='POST':
        namee=request.POST['namey']
        pass1=request.POST['passwordd']
        userr=authenticate(username=namee,password=pass1)
        if userr is not None:
            prof=Profile.objects.filter(user=userr).first()
            if prof.is_verified:
                login(request,userr)
                return redirect('home')
            
            else:
                return redirect('fake')
        else:
            return render(request,'login.html') 
            # return redirect('fakd_login')            
    
    return render(request,'login.html')    

def signup(request):
    if request.method=='POST':
        namee=request.POST['name']
        emaill=request.POST['email']
        pass1=request.POST['password']
        pass2=request.POST['cnfpassword']
        if pass1!=pass2:
           return redirect('signup')
        if User.objects.filter(email=emaill).first():
            return redirect('signup')
        myuser=User.objects.create_user(namee,emaill,pass1)
        myuser.save()
        auth_token = str(uuid.uuid4())
        profile_obj = Profile.objects.create(user=myuser,auth_token=auth_token)
        profile_obj.save()
        send_email_after_registeration(emaill, auth_token)
        return render(request,'login.html') 
    
    return render(request,'signup.html')

def logoutt(request):
    logout(request)
    return redirect('home')

def addmed(request):
    user=request.user
    if request.method=='POST':
        ename=request.POST['ename']
        doss=request.POST['doss']
        freq=request.POST['freq']
        med=Medical(user=user,nameM=ename,doses=doss,frequency=freq)
        main(ename,doss,freq,request.user.email)
        med.save()
    return render(request,'adddos.html')

def viewdos(request):
    userr=request.user
    medi=Medical.objects.filter(user=userr)
    dictt={'medi':medi}
    return render(request,'viewdos.html',dictt)

def edit(request,sno):
    dos=Medical.objects.filter(sno=sno).first()
    dic={'dos':dos}
    return render(request,'edit.html',dic)

def update(request,sno):
    user=request.user
    if request.method=='POST':
        ename=request.POST['ename']
        doss=request.POST['doss']
        freq=request.POST['freq']
        med=Medical(sno=sno,user=user,nameM=ename,doses=doss,frequency=freq)
        main(ename,doss,freq,request.user.email)
        med.save()
        
    return redirect('viewdoses')    
   
def delete(request,sno):
    doss=Medical.objects.filter(sno=sno).delete()
    return redirect('viewdoses')

def send_email_after_registeration(email, token):
    # subject='Your Account need to be verifred',
    # message=f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    # email_from=settings.EMAIL_HOST_USER
    # recipient_list=[email]
    # send_mail(subject,message,email_from,recipient_list)
    # instance of MIMEBase and named as p

    fromaddr = "scraper0000@gmail.com"
    toaddr = f"{email}"

    msg = MIMEMultipart()
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Prediction results"

    # string to store the body of the mail
    body = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent

    # p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    # p.set_payload((attachment).read())

    # encode into base64
    # encoders.encode_base64(p)

    # p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    # msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "ueqzcspenwccecft")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()