from django.shortcuts import render, redirect
from allauth.account import views

from django.views import View #カスタムユーザー
from accounts.models import CustomUser, Post_Inquiry #カスタムユーザー
from accounts.forms import ProfileForm, SignupUserForm, Inquiry #カスタムユーザー
from django.contrib.auth.mixins import LoginRequiredMixin #カスタムユーザー

from django.db.models import Q

import datetime

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator

import imghdr,hashlib
from django.core.exceptions import ObjectDoesNotExist

class LoginView(views.LoginView):
    template_name = 'accounts/login/login.html'
    
class LogoutView(views.LogoutView):
    template_name = 'accounts/login/logout.html'
    
    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.logout()
        return redirect('/')


class SignupView(views.SignupView):
    template_name = 'accounts/register/signup.html'
    form_class = SignupUserForm

def TermsView(request):
    return render(request, "accounts/register/terms.html")

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        Switch = False

        user_data = CustomUser.objects.get(id=request.user.id)
        return render(request, 'accounts/profile/profile.html', {
            'user_data': user_data,
            'Switch': Switch
        })

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'nick_name': user_data.nick_name,
                'user_screen_id': user_data.user_screen_id,
                'year': user_data.year,
                'course': user_data.course,
                'tel': user_data.tel,
                'job': user_data.job,
                'avatar': user_data.avatar,
            }
        )
        return render(request, 'accounts/profile/profile_edit.html',{
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():

            def validate_unique(self):
                user_screen_id = self
                SearchResult =  CustomUser.objects.filter(~Q(id=request.user.id) & Q(user_screen_id=user_screen_id))
                # print(SearchResult)
                if SearchResult.exists():
                    raise ValidationError(f"{user_screen_id}は既に使われています。別のIDに変更してください")
                    return user_screen_id
                return user_screen_id
            
            user_data = CustomUser.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            
            user_data.nick_name = form.cleaned_data['nick_name']

            # user_screen_id_temp = form.cleaned_data['user_screen_id']
            # user_data.user_screen_id = validate_unique(user_screen_id_temp)
            user_data.user_screen_id = validate_unique(form.cleaned_data['user_screen_id'])
            user_data.year = form.cleaned_data['year']
            user_data.zipcode = form.cleaned_data['zipcode']
            user_data.address = form.cleaned_data['address']
            user_data.buildingname = form.cleaned_data['buildingname']
            user_data.tel = form.cleaned_data['tel']
            user_data.job = form.cleaned_data['job']
            # user_data.avatar = form.cleaned_data[request.FILES['avatar']]
            
            image_file_dict = self.request.FILES
            if image_file_dict:
                user_data.avatar = request.FILES['avatar']
            user_data.save()
            print("success")
            return redirect('account_profile')
        else:
            return redirect('account_profile')
            

class ProfileCheckView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/profile/profile_delete.html')
    
    def post(self, request, *args, **kwargs):
        return redirect('profile_delete', 'True')

class ProfileDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                if self.kwargs['slug'] == "True":
                    CustomUser.objects.get(id=self.request.user.id).delete()
                    self.logout()
            else:
                return redirect('account_profile')
        except:
            return redirect('account_profile')
        return redirect('Index')

class ManageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/manage.html')


class HistoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # item_data = Order.objects.filter(user=request.user.email).all() #id=request.user.id
        return render(request, "app/store/history.html", {
            # 'order': item_data
        })

class OrderHistoryView(LoginRequiredMixin, View):
    # search_data = ''

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            try:
                order = OrderItem.objects.order_by('ordered_date', 'id').reverse().filter(user_id=request.user.id).all()
                # print(order)
                user_data = CustomUser.objects.get(id=request.user.id)

                paginator = Paginator(order, 10)
                p = request.GET.get('p')
                order = paginator.get_page(p)

                context = {
                    'OrderHistory': order,
                    'UserData': user_data,
                }
                return render(request, 'app/store/history.html', context)
            except ObjectDoesNotExist:
                return redirect('management')
        
    def post(self, request, *args, **kwargs):
        # print('POST')
        if request.method == 'POST':
            # print('POST')
                user_data = CustomUser.objects.get(id=request.user.id)
                order = OrderItem.objects.order_by('ordered_date', 'id').reverse().filter(user_id=request.user.id).all()
                search_data = request.POST['search_data']
                print('search:' + search_data)
                result = order.filter(Q(item__title__contains=search_data)).all()
                # Q(title__contains=search_data)
                # print("result: " + result)
                
                paginator = Paginator(result, 10)
                p = request.POST.get('p')
                result = paginator.get_page(p)

                context = {
                    'OrderHistory': result,
                    'UserData': user_data,
                }
                return render(request, 'app/store/history.html', context)
            # try:
            # except:
            #     return redirect('management')
        else:
                return redirect('management')




class InquiryView(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            try:
                form = Inquiry(request.POST or None)
                context = {
                    'form': form
                }
                return render(request, 'accounts/inquiry/inquiry.html', context)
            except ObjectDoesNotExist:
                return redirect('management')
        
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                form = Inquiry(request.POST or None)
                if form.is_valid():
                    inquiry_data = Post_Inquiry()
                    inquiry_data.email = form.cleaned_data['email']
                    inquiry_data.first_name = form.cleaned_data['first_name']
                    inquiry_data.last_name = form.cleaned_data['last_name']
                    inquiry_data.title = form.cleaned_data['title']
                    inquiry_data.summary = form.cleaned_data['summary']
                    inquiry_data.read_field = form.cleaned_data['read_field']
                    inquiry_data.save()
                    return redirect('Inquiry_complete')
            except:
                    return redirect('management')
        return redirect('management')

        

class InquiryCompleteView(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            try:
                inquiry_data = Post_Inquiry.objects.filter(email=request.user.email).order_by('-created').all()[0]
                send_email(inquiry_data)
                return render(request, 'accounts/inquiry/inquiry_send_completely.html')
            except ObjectDoesNotExist:
                return redirect('management')


from django.core.mail import EmailMultiAlternatives
def send_email(inquiry_data):

    mail_title="お問い合わせありがとうございます"
    text_content="""
    　　　　　　　　　　　　{inquiry_data.first_name}様、この度はお問い合わせありがとうございます。
    　　　　　　　　　　　　順にサポートさせていただきますので、ご了承ください。
            """
    html_content=f"""
            <p>{inquiry_data.first_name}様、この度はお問い合わせありがとうございます。
            順にサポートさせていただきますので、ご了承ください。
            </p>
            <h3>タイトル: {inquiry_data.title}</h3>
            <h4>受付番号: {inquiry_data.id}</h4>
            <p>お問い合わせ内容:
            {inquiry_data.summary}
            </p>
            <p>お問い合わせ日時: {inquiry_data.created}</p>
            """

    msg=EmailMultiAlternatives(
            subject=mail_title, 
            body=text_content, 
            from_email='factiohew@gmail.com', 
            to=[inquiry_data.email],
            # reply_to=[]
            )
    msg.attach_alternative(html_content,"text/html")
    msg.send()
