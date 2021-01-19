from django.shortcuts import render,redirect, get_object_or_404,reverse
from .models import *
from .forms import *
from django.conf import settings
import hashlib
import datetime
from .Calculator import *

'''
此函数是返回一个十六进制字符串
@:param s 传来的用户名
@:param salt 默认的值这里默认为keeping
@:return hexdigest 返回摘要作为十六进制字符串值
'''
def hash_code(s, salt='keeping'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

'''
此函数是返回一串十六进制编码作为验证码，将验证码传入到ConfirmString中
@:param user 传入一个user对象
@:return code 十六进行编码
'''
def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    ConfirmString.objects.create(code=code, user=user)
    return code

'''
进行邮箱确认函数
@:param email 要发送的邮箱
@:param code 验证码
'''
def send_email(email, code):

    from django.core.mail import EmailMultiAlternatives

    subject = '来自电子记账系统的注册确认邮件'

    text_content = '''如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                       <p>感谢注册<a href="http://{}/keeping/confirm/?code={}" target=blank>点击此处</a></p>
                       <p>请点击站点链接完成注册确认！</p>
                       <p>此链接有效期为{}天！</p>
                       '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

'''
转到主页面
@:param request
'''
def index(request):
    if not request.session.get('is_login', None):
        return redirect('login')
    EDU = CalO(outcome.objects.filter(things="e",userID=request.session.get("user_id")))
    LIF = CalO(outcome.objects.filter(things="l",userID=request.session.get("user_id")))
    MED = CalO(outcome.objects.filter(things="m",userID=request.session.get("user_id")))
    SAL = CalI(income.objects.filter(things="s",userID=request.session.get("user_id")))
    one = CalO(outcome.objects.filter(data__month=1,userID=request.session.get("user_id")))
    two = CalO(outcome.objects.filter(data__month=2,userID=request.session.get("user_id")))
    three = CalO(outcome.objects.filter(data__month=3,userID=request.session.get("user_id")))
    four = CalO(outcome.objects.filter(data__month=4,userID=request.session.get("user_id")))
    five = CalO(outcome.objects.filter(data__month=5,userID=request.session.get("user_id")))
    six =  CalO(outcome.objects.filter(data__month=6,userID=request.session.get("user_id")))
    seven = CalO(outcome.objects.filter(data__month=7,userID=request.session.get("user_id")))
    eight =CalO(outcome.objects.filter(data__month=8,userID=request.session.get("user_id")))
    nine =CalO(outcome.objects.filter(data__month=9,userID=request.session.get("user_id")))
    ten =CalO(outcome.objects.filter(data__month=10,userID=request.session.get("user_id")))
    ele =CalO(outcome.objects.filter(data__month=11,userID=request.session.get("user_id")))
    twe =CalO(outcome.objects.filter(data__month=12,userID=request.session.get("user_id")))
    monthout = []
    monthout.append(one)
    monthout.append(two)
    monthout.append(three)
    monthout.append(four)
    monthout.append(five)
    monthout.append(six)
    monthout.append(seven)
    monthout.append(eight)
    monthout.append(nine)
    monthout.append(ten)
    monthout.append(ele)
    monthout.append(twe)
    return render(request, 'index.html',{"e":EDU,"l":LIF,"m":MED,"s":SAL,"monthout":monthout})

'''
登录处理函数，此函数用到了表单
@:param request
'''
def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('index')
    if request.method == "POST":
        login_form = LoginForm(request.POST) #登录表单进行验证
        message = '请检查填写的内容！'
        if login_form.is_valid():
            #从form 中获取用户输入的表单信息
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                #从model中获取用户
                users = user.objects.get(name=username)
                #todo 加入正则表达式验证是否合法，然后返回页面上？或者前端加html5的正则表达式？
            except:
                message = '用户不存在！'
                return render(request, 'login.html',locals())

            if not users.has_confirmed:
                message = '该用户还未经过邮件确认！'
                return render(request, 'login.html', locals())

            if users.passwd == password:
                request.session['is_login'] = True #设置了登录限制
                request.session['user_id'] = users.pk
                request.session['user_name'] = users.name
                return redirect('index')
            else:
                message = '密码不正确！'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())

    login_form = LoginForm()
    return render(request, 'login.html', locals())

'''
注册处理函数，此函数用到了表单
@:param request
'''
def register(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('index')
    if request.method == "POST":
        register_form = RegisterForm(request.POST) #函数
        message = '请检查填写的内容！'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'register.html', locals())
            else:
                same_name_user = user.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'register.html', locals())
                same_email_user = user.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'register.html', locals())

                new_user = user()
                new_user.name = username
                new_user.passwd = password1
                new_user.email =email
                new_user.save()

                code = make_confirm_string(new_user)
                send_email(email, code)
                message = '请前往邮箱进行确认！'
                return render(request, 'confirm.html', locals())
        else:
            return render(request, 'register.html', locals())

    register_form = RegisterForm()
    return render(request, 'register.html', locals())

'''
此函数是用来确认验证的
@:param request 
'''
def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = ConfirmString.objects.get(code=code)
    except:
        message = '无效的确认请求!'
        return render(request, 'confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'confirm.html', locals())

'''
登出按钮
'''
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("login")
    request.session.flush()
    return redirect("login")

def incomes(request):
    if not request.session.get('is_login', None):#没登录无法使用
        return redirect('login')
    if request.method == "POST":
        income_form = IncomeForm(request.POST)
        if income_form.is_valid():
            detail = income_form.cleaned_data.get('detail')
            inmoney = income_form.cleaned_data.get('inmoney')
            things = income_form.cleaned_data.get('things')
            date = income_form.cleaned_data.get('date')
            users = user.objects.filter(pk=request.session.get("user_id")).first()
            new_incomey = income()
            new_incomey.detail =detail
            new_incomey.inmoney =inmoney
            new_incomey.userID =users
            new_incomey.things =things
            new_incomey.data =date
            new_incomey.save()
            task1 = income.objects.all()
            return redirect("index")
        else:
            return render(request, 'income.html', locals())

    income_form = IncomeForm()
    return render(request,"income.html",{"form":income_form})

def outcomes(request):
    if not request.session.get('is_login', None):#没登录无法使用
        return redirect('login')
    if request.method == "POST":
        outcome_form = OutcomeForm(request.POST)
        if outcome_form.is_valid():
            detail = outcome_form.cleaned_data.get('detail')
            outmoney = outcome_form.cleaned_data.get('outmoney')
            things = outcome_form.cleaned_data.get('things')
            date = outcome_form.cleaned_data.get('date')
            users = user.objects.filter(pk=request.session.get("user_id")).first()
            new_outcome = outcome()
            new_outcome.detail =detail
            new_outcome.outmoney =outmoney
            new_outcome.userID =users
            new_outcome.things =things
            new_outcome.data =date
            new_outcome.save()
            return redirect("index")
        else:
            return render(request,'outcome.html',locals())

    outcome_form = OutcomeForm()
    return render(request,"outcome.html",{"form":outcome_form})

def statistics(request):
    if not request.session.get('is_login', None):#没登录无法使用
        return redirect('login')
    if request.method == "POST":
        if 'year' in request.POST and request.POST['year']:
            year_in = CalI(income.objects.filter(data__year=request.POST['year'],userID=request.session.get("user_id")))
            year_out = CalO(outcome.objects.filter(data__year=request.POST['year'],userID=request.session.get("user_id")))
            return render(request, 'statistics.html', locals())
        if 'myear' in request.POST and request.POST['myear'] and 'mmonth' in request.POST and request.POST['mmonth']:
            month_in = CalI(income.objects.filter(data__year=request.POST['myear'],data__month=request.POST['mmonth'],userID=request.session.get("user_id")))
            month_out = CalO(outcome.objects.filter(data__year=request.POST['myear'],data__month=request.POST['mmonth'],userID=request.session.get("user_id")))
            return render(request, 'statistics.html', locals())
        if 'dyear' in request.POST and request.POST['dyear'] and 'dmonth' in request.POST and request.POST['dmonth']and 'dday' in request.POST and request.POST['dday']:
            day_in = CalI(
                income.objects.filter(data__year=request.POST['dyear'], data__month=request.POST['dmonth'],data__day=request.POST['dday'],userID=request.session.get("user_id")))
            day_out = CalO(
                outcome.objects.filter(data__year=request.POST['dyear'], data__month=request.POST['dmonth'],data__day=request.POST['dday'],userID=request.session.get("user_id")))
            return render(request, 'statistics.html', locals())
        #后面是直接返回结果的

    return render(request, 'statistics.html', locals())

def show_income(request):
    if not request.session.get('is_login', None):#没登录无法使用
        return redirect('login')
    task1 = income.objects.filter(userID=request.session.get("user_id"))
    return render(request, "show_income.html", {"task1": task1,})

def show_outcome(request):
    if not request.session.get('is_login', None):#没登录无法使用
        return redirect('login')
    task1 = outcome.objects.filter(userID=request.session.get("user_id"))
    return render(request, "show_outcome.html", {"task1": task1,})

def show_edu(request):
    if not request.session.get('is_login', None):#没登录无法使用
        return redirect('login')
    task1 = outcome.objects.filter(things="e",userID=request.session.get("user_id"))
    return render(request, "show_edu.html", {"task1": task1,})

def show_med(request):
    if not request.session.get('is_login', None):#没登录无法使用
        return redirect('login')
    task1 = outcome.objects.filter(things="m",userID=request.session.get("user_id"))
    return render(request, "show_med.html", {"task1": task1,})

def show_lif(request):
    if not request.session.get('is_login', None):#没登录无法使用
        return redirect('login')
    task1 = outcome.objects.filter(things="l",userID=request.session.get("user_id"))
    return render(request, "show_lif.html", {"task1": task1,})

def show_sal(request):
    if not request.session.get('is_login', None):#没登录无法使用
        return redirect('login')
    task1 = income.objects.filter(things="s",userID=request.session.get("user_id"))
    return render(request, "show_sal.html", {"task1": task1,})
