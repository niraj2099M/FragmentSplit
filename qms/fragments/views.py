from django.shortcuts import render,redirect
from .models import players,sess,payoutData
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
import re
# Create your views here.

#a very basic auth wo >> Django built in login forms and user reg
@csrf_exempt
def log(request):

    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username, password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('show')

            

    return render(request,'fragments/login.html',{})


def log_out(request):

    auth.logout(request)
    return redirect('loginpage')


def list_all(request):

    allData=players.objects.all()
    return render(request,'fragments/list.html',{"data":allData})


@login_required(login_url='loginpage')
def show(request):

    if request.method=="POST":
        name=request.POST['name']
        
        
        regex = r'^[a-zA-Z]+(-[a-zA-Z]+)?$'
        if re.match(regex, name):
            try:
                new_data=players(
                    name=name,
                    fragNo=0,
                    wz=0
                )
                new_data.save()
            except:
                return render(request, 'fragments/error.html',{"name":name})            
        else:
            return redirect('show')
    
    allData=players.objects.all()

    totalFrags=0
    totalWz=0
    for d in allData:
        totalFrags=totalFrags+d.fragNo
        totalWz=totalWz+d.wz
    sum=[int(totalFrags),totalWz]

    return render(request, 'fragments/home.html',{"data":allData, "s":sum})


@csrf_exempt
@login_required(login_url='loginpage')
def sessions(request):

    if request.method=="POST":
        date=request.POST['selectedDate']
        timeofDay=request.POST['flexRadioDefault']
        frags=request.POST['integerValue']
        wz=request.POST['wzValue']
        lstPlayerIds=request.POST.getlist('options[]')
        noPlayers=len(lstPlayerIds)
        # print(date)
        # print(timeofDay)
        #print(type(frags))
        #print(type(wz))
        print(lstPlayerIds)
        strPlayerIds=",".join(lstPlayerIds)

        newData=sess(
                dateSession=date,
                time_of_day = timeofDay, 
                noFrag = frags,
                wzCollected = wz,
                noPlayers=noPlayers,
                player_ids=strPlayerIds
        )
        newData.save()

        #update operation
        
        if noPlayers!= 0:
            frags=int(frags)
            wz=int(wz)
            fragsPer=frags/noPlayers
            wzPer=wz/noPlayers

            for id in lstPlayerIds:
                player=players.objects.get(id=id)
                floatFrag=float(player.fragNo)
                floatwz=float(player.wz)


                floatFrag=floatFrag+fragsPer
                floatwz=floatwz+wzPer

                player.fragNo=floatFrag
                player.wz=floatwz
                player.save()
            
            return redirect('sessionD')


    allData=players.objects.all()
    return render(request, 'fragments/session.html',{"data":allData})


@login_required(login_url='loginpage')
def session_data(request):
    allsession=sess.objects.all().order_by('-id')[:10]
    return render(request, 'fragments/sessData.html',{"sessD":allsession })



@login_required(login_url='loginpage')
def undo_session(request,id):

    sessionD=sess.objects.get(id=id)
    frags=sessionD.noFrag
    wz=sessionD.wzCollected
    no=sessionD.noPlayers
    ids=sessionD.player_ids

    lstIds=ids.split(",")
    leng=len(lstIds)
    
    lst_players=[]
    for i in range(0,leng):
        lstIds[i]=int(lstIds[i])
        player=players.objects.get(id=lstIds[i])
        lst_players.append(player)


    return render(request,'fragments/sessUndo.html',{"players":lst_players,"d":sessionD})


@login_required(login_url='loginpage')
def undo_session_confim(request,id):

    sessionD=sess.objects.get(id=id)
    frags=sessionD.noFrag
    wz=sessionD.wzCollected
    no=sessionD.noPlayers
    fp=frags/no
    wzp=wz/no

    ids=sessionD.player_ids

    lstIds=ids.split(",")
    leng=len(lstIds)
    
    for i in range(0,leng):
        lstIds[i]=int(lstIds[i])

    for id in lstIds:
        eachPlayer=players.objects.get(id=id)
        eachPlayer.wz=float(eachPlayer.wz)-wzp
        eachPlayer.fragNo=float(eachPlayer.fragNo)-fp
        eachPlayer.save()

    sessionD.delete()


    return redirect('sessionD')



@csrf_exempt
@login_required(login_url='loginpage')
def updateData(request,id):
    
    if request.method=='POST':
        frags = request.POST['fpay']
        wz = request.POST['wzpay']
        player =players.objects.get(id=id)
        currentFrags=float(player.fragNo)
        currentWz=float(player.wz)

        if((currentFrags-float(frags)) >=0 and (currentWz-int(wz)) >=0):

            player.fragNo=currentFrags-float(frags)
            player.wz=currentWz-int(wz)

            player.save()

            #storing in payout table
            payout=payoutData(
                name=player.name,
                fragsPaid=float(frags),
                wzPaid=int(wz)
            )
            payout.save()

    playerData = players.objects.get(id=id)
    payoutD=payoutData.objects.all().order_by('-id')[:40]
    
    return render(request, 'fragments/update.html', {"pd":playerData, "payd": payoutD})   


