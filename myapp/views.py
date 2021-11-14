from django.shortcuts import render
from django.http import HttpResponse
import json,os
from django.conf import settings
import urllib
from django.template.defaulttags import register





# Create your views here.
def index(request):
    with open(os.path.join(settings.BASE_DIR, 'static/jonson/sname.json')) as file:
        data_file = json.load(file)
    context = {'list': data_file}
    if request.method == 'POST':
        currecyfrom,currecyto,toconvert = request.POST['countrycodefrom'],request.POST['countrycodeto'],request.POST['currencytoconvert']
        thisname,toname = context['list'][currecyfrom],context['list'][currecyto]
        moneydata = converter(currecyfrom,currecyto,toconvert,thisname,toname)
    else:
        moneydata = converter(thisname='UAE Dirham',toname='Indian Rupee')
    context['togive'] = moneydata
    context = {'list': data_file,'togive':moneydata}
    return render(request, "pages/hello.html",context)
  
def converter(this='AED', to='INR', amount='1',thisname='',toname=''):
    if amount == "":
        amount = 1
    if this == to:
        moneydata = {0:this,1:to,2:amount,3:"1",4:'1',5:amount,6:thisname,7:toname,8:''}
        return moneydata
    url = f'https://api.exchangerate.host/convert?from={this}&to={to}&amount={amount}'
    try:
        
        response = urllib.request.urlopen(url)
    except:
        moneydata = {0:this,1:this,2:'1',3:"1",4:'1',5:'1',6:thisname,7:thisname,8:'SOMETHING WENT WORNG \nTRY AGAIN LATER'}
        return moneydata
    data = json.load(response)
    rate1,result = data['info']['rate'],data['result']
    temp1,temp2=amount ,rate1
    rate2 = float(temp1)/float(temp2)
    rate2= rate2/float(amount)
    moneydata = {0:this,1:to,2:amount,3:float("{0:.3f}".format(rate1)),4:round(rate2,3),5:round(result,3),6:thisname,7:toname,8:''}
    # 0=this, 1=to , 2=amount to change,, 3=current rate of this for 1 doller,4=current rate of to for 1 doller, 5=converted money
    return moneydata


