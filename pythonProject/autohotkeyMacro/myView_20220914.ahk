Gui, Show, w400 h340, KAKAO MyView auto
Gui, Add, Text, x111 y20, *카카오뷰 원격 자동 인증 설정*
Gui, Add, Text, x20 y55, VIEW 인증 대상 COUNT 

Gui, Add, edit, x165 y50 w50 h20 vCnt +Number, 9999
Gui, Add, Text, x20 y80, VIEW 타겟 윈도우 창 
Gui, Add, Edit, x165 y75 w200 h20 vTitle, Samsung DeX

Gui, Add, Text, x20 y115, 개별 상세 설정 (* 체크는 필수 값)%Title%
Gui, Add, DropDownList, x20 y135 w200 h999 vSELTYPE, 상민설정||상민(2)설정|수윤설정
Gui, Add, Text, x20 y175, * 광고 로딩 이후 하드웨어 로딩 대기 시간 설정 [권장5] (초 단위)
Gui, Add, edit, x20 y195 w50 h20 vDelTime +Number, 5
Gui, Add, Text, x20 y225, * 전체적인 매크로 속도 설정 [권장0.5] (초 단위)
Gui, Add, edit, x20 y245 w50 h20 vDelay +Number, 0.5
Gui, Add, Button, x20 y280 w280 h50 gBtn, 마이뷰 추가하기
Gui, Add, Button, x310 y280 w70 h50 gBtn, 멈춤
Gui, Show

return



Btn:
Gui, Submit, NoHide

;script import
#Include %A_scriptDir%\Gdip_All.ahk
#Include %A_scriptDir%\Gdip_ImageSearch.ahk

WinActivate, %Title%
Sleep, 1000
loopcnt:=1
xloc:=50   ;50 <> 300
yloc:=105
loopStop:=0

startRangeX:=0
startRangeY:=95
searchRangeX:=1920
searchRangeY:=1020
searchDetail:=70
Delay=Delay*1000

workDir=%A_scriptDir%\image

Check:=0
;기본 값 설정
if (SELTYPE = "상민설정")
    fileName:=""
else if (SELTYPE = "상민(2)설정")
    fileName:= "_m"
else if (SELTYPE = "수윤설정")
    fileName:="_s"

pre_x:=0
pre_y:=0

Loop, %Cnt%
{
    WinActivate, %Title%
    imagesearch,x,y,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %workDir%\http_txt.png

    if(ErrorLevel = 0 And (((pre_x+50) < x) || (pre_y+10) < y))
    {
        WinActivate, %Title%
        Mouseclick,left,x+10,y+10
        pre_x = x
        pre_x = y
        Sleep, %Delay%
    }
        
    Sleep, %Delay%
    channelDisable:=0
    While(channelDisable=0) 
    {  
        imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %workDir%\channelDisable%fileName%.bmp
        if(ErrorLevel = 0) 
        {
            WinActivate, %Title%
            Mouseclick,left,xx,yy
            Sleep, %Delay%
            ChannelBlock:=0
            While (ChannelBlock=0)
            {
                imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %workDir%\ChannelBlock%fileName%.bmp
                if(ErrorLevel = 0)
                {
                    WinActivate, %Title%
                    Mouseclick,left,xx+30,yy+20
                    Sleep, %Delay%
                    channelComplete:=0
                    While (channelComplete=0)
                    {
                        imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %workDir%\channelComplete%fileName%.bmp
                        if(ErrorLevel = 0)
                        {
                            Mouseclick,left,xx,yy
                            WinActivate, %Title%
                            Sleep, %Delay%
                            channelDisable=1
                            ChannelBlock=1
                            channelComplete=1
                            break
                        }
                    }
                }
            }
        }
        
        WinActivate, %Title%
        imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %workDir%\channelEnable%fileName%.bmp
        if(ErrorLevel = 0) {
            channelDisable=1
            ChannelBlock=1
            channelComplete=1
            break
        }
    }
    
    channelEnable:=0
    While(channelEnable=0) 
    {
        WinActivate, %Title%
        imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %workDir%\channelEnable%fileName%.bmp
        if(ErrorLevel = 0)
        {
            WinActivate, %Title%
            Mouseclick,left,xx,yy
            Sleep, %Delay%
            ChannelAdd:=0
            While (ChannelAdd=0)
            {
                Sleep, 1000
                imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %workDir%\channelAdd%fileName%.bmp
                if(ErrorLevel = 0)
                {
                    WinActivate, %Title%
                    Mouseclick,left,xx+23,yy
                    Sleep, %Delay%
                    ChannelAdd=1
                    channelEnable=1
                    break
                }
            }
        }
    }
    channelHome:=0
    While(channelHome=0) 
    {
       
        imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %workDir%\channelHome%fileName%.bmp
        if(ErrorLevel = 0)
        {
            WinActivate, %Title%
            Mouseclick,left,xx,yy
            Sleep, %Delay% 

            mainHome:=0
            While (mainHome=0)
            {
                WinActivate, %Title%
                imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %workDir%\mainHome%fileName%.bmp
                if(ErrorLevel = 0)
                {
                    channelHome=1
                    mainHome=1
                    break
                }
            }
        }   
    }
}
return

F12::
Reload

GuiClose:
ExitApp