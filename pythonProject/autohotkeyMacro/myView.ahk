Gui, Show, w400 h340, KAKAO MyView auto
Gui, Add, Text, x111 y20, *카카오뷰 원격 자동 인증 설정*
Gui, Add, Text, x20 y55, VIEW 인증 대상 COUNT 

Gui, Add, edit, x165 y50 w50 h20 vCnt +Number, 9999
Gui, Add, Text, x20 y80, VIEW 타겟 윈도우 창 
Gui, Add, Edit, x165 y75 w200 h20 vTitle, Samsung DeX

Gui, Add, Text, x20 y115, 개별 상세 설정 (* 체크는 필수 값)%Title%
Gui, Add, DropDownList, x20 y135 w120 h999 vSELTYPE, BLACK THEME||WHITE THEME
Gui, Add, DropDownList, x150 y135 w120 h999 vSELTYPE1, BLACK THEME||WHITE THEME
;기본적으로 font 사이즈보다 1픽셀 커야 얼추 매칭된다.
Gui, Add, edit, x290 y135 w30 h20 vFontSize +Number, 15
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
xloc:=20   ;20 <> 230
yloc:=105

startRangeX:=0
startRangeY:=0
searchRangeX:=1920
searchRangeY:=570
searchDetail:=80
Delay=Delay*1000

workDir=%A_scriptDir%\image

Check:=0
;기본 값 설정
if (SELTYPE = "BLACK THEME")
    fileName:=""
else if (SELTYPE = "WHITE THEME")
    fileName:= "_m"

activation = True

Loop, %Cnt%
{
    yloc:=yloc + FontSize
    ;1000 픽셀이 넘어가면 초기화
    ;x 값을 다음줄로 건너 뛰기
    if (yloc > 1005)
    {
        yloc := 105 + FontSize
        xloc := xloc + 210
    }

    WinActivate, %Title%
    Mouseclick,left,xloc,yloc
    ;Sleep, %Delay%
    limitTime=0
    currTime=0
    formattime, limitTime, , yyyyMMddhhmmss
    limitTime+= 15, Seconds
    
    channelDisable:=0
    While(channelDisable=0) 
    {
        formattime, currTime, , yyyyMMddhhmmss
        if (limitTime < currTime)
        {
            channelDisable = 1
        }

        ;if (Number)
        imagesearch,xx,yy,1800,100,1980,200, *%searchDetail% %workDir%\channelDisable%fileName%.png
        if(ErrorLevel = 0) 
        {
            ;WinActivate, %Title%
            Mouseclick,left,xx+10,yy+10
            ChannelBlock:=0
            While (ChannelBlock=0)
            {
                imagesearch,xx,yy,1050,500,1150,600, *%searchDetail% %workDir%\ChannelBlock%fileName%.png
                if(ErrorLevel = 0)
                {
                    ;WinActivate, %Title%
                    Mouseclick,left,xx+10,yy+10
                    channelComplete:=0
                    While (channelComplete=0)
                    {
                        imagesearch,xx,yy,1050,500,1150,600, *%searchDetail% %workDir%\channelComplete%fileName%.png
                        if(ErrorLevel = 0)
                        {
                            Mouseclick,left,xx+10,yy+10
                            ;WinActivate, %Title%
                            channelDisable=1
                            ChannelBlock=1
                            channelComplete=1
                            break
                        }
                    }
                }
            }
        }
        
        ;WinActivate, %Title%
        imagesearch,xx,yy,1800,100,1980,200, *%searchDetail% %workDir%\channelEnable%fileName%.png
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
        formattime, currTime, , yyyyMMddhhmmss
        if (limitTime < currTime)
        {
            channelEnable = 1
        }

        ;WinActivate, %Title%
        imagesearch,xx,yy,1800,100,1980,200, *%searchDetail% %workDir%\channelEnable%fileName%.png
        if(ErrorLevel = 0)
        {
            ;WinActivate, %Title%
            Mouseclick,left,xx+10,yy+10
            ChannelAdd:=0
            While (ChannelAdd=0)
            {
                imagesearch,xx,yy,950,500,1100,560, *%searchDetail% %workDir%\channelAdd%fileName%.png
                if(ErrorLevel = 0)
                {
                    ;WinActivate, %Title%
                    Mouseclick,left,xx+23,yy
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
    
        formattime, currTime, , yyyyMMddhhmmss
        if (limitTime < currTime)
        {
            channelHome = 1
        }

        imagesearch,xx,yy,0,40,50,100, *%searchDetail% %workDir%\channelHome%fileName%.png
        if(ErrorLevel = 0)
        {
            ;WinActivate, %Title%
            Mouseclick,left,xx+10,yy+10

            mainHome:=0
            While (mainHome=0)
            {
                ;WinActivate, %Title%
                imagesearch,xx,yy,40,40,130,90, *%searchDetail% %workDir%\mainHome%fileName%.png
                if(ErrorLevel = 0)
                {
                    channelHome=1
                    mainHome=1
                    break
                }
            }
        }   
    }

    formattime, currTime, , yyyyMMddhhmmss
    if (limitTime < currTime)
    {
        break
    }
}

;기본 값 설정
if (SELTYPE1 = "BLACK THEME")
    fileName:=""
else if (SELTYPE1 = "WHITE THEME")
    fileName:= "_m"

xloc:=20   ;20 <> 230
yloc:=105

;WinActivate, %Title%
is_next_kakao = False
While(is_next_kakao)
{
    imagesearch,xx,yy,800,1000,1200,1080, *%searchDetail% %workDir%\kakaoNext.png
    if(ErrorLevel = 0)
    {
        ;WinActivate, %Title%
        Mouseclick,left,xx+15,+yy+20
        break
    }
}

;카카오 넘어가는 지점 1초 강제 세팅
Sleep, 1000

Loop, %Cnt%
{
    yloc:=yloc + FontSize
    ;1000 픽셀이 넘어가면 초기화
    ;x 값을 다음줄로 건너 뛰기
    if (yloc > 1005)
    {
        yloc := 105 + FontSize
        xloc := xloc + 210
    }

    WinActivate, %Title%
    Mouseclick,left,xloc,yloc
    ;Sleep, %Delay%
    limitTime=0
    currTime=0
    formattime, limitTime, , yyyyMMddhhmmss
    limitTime+= 10, Seconds
    
    channelDisable:=0
    While(channelDisable=0) 
    {
        ;WinActivate, %Title%
        formattime, currTime, , yyyyMMddhhmmss
        if (limitTime < currTime)
        {
            channelDisable = 1
        }

        ;if (Number)
        ;WinActivate, %Title%
        imagesearch,xx,yy,1800,100,1980,200, *%searchDetail% %workDir%\channelDisable%fileName%.png
        if(ErrorLevel = 0) 
        {
            ;WinActivate, %Title%
            Mouseclick,left,xx+10,yy+10
            ChannelBlock:=0
            While (ChannelBlock=0)
            {
                imagesearch,xx,yy,1050,500,1150,600, *%searchDetail% %workDir%\ChannelBlock%fileName%.png
                if(ErrorLevel = 0)
                {
                    ;WinActivate, %Title%
                    Mouseclick,left,xx+10,yy+10
                    channelComplete:=0
                    While (channelComplete=0)
                    {
                        imagesearch,xx,yy,1050,500,1150,600, *%searchDetail% %workDir%\channelComplete%fileName%.png
                        if(ErrorLevel = 0)
                        {
                            Mouseclick,left,xx+10,yy+10
                            ;WinActivate, %Title%
                            channelDisable=1
                            ChannelBlock=1
                            channelComplete=1
                            break
                        }
                    }
                }
            }
        }
        
        ;WinActivate, %Title%
        imagesearch,xx,yy,1800,100,1980,200, *%searchDetail% %workDir%\channelEnable%fileName%.png
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
        formattime, currTime, , yyyyMMddhhmmss
        if (limitTime < currTime)
        {
            channelEnable = 1
        }

        ;WinActivate, %Title%
        imagesearch,xx,yy,1800,100,1980,200, *%searchDetail% %workDir%\channelEnable%fileName%.png
        if(ErrorLevel = 0)
        {
            ;WinActivate, %Title%
            Mouseclick,left,xx+10,yy+10
            ChannelAdd:=0
            While (ChannelAdd=0)
            {
                imagesearch,xx,yy,950,500,1100,600, *%searchDetail% %workDir%\channelAdd%fileName%.png
                if(ErrorLevel = 0)
                {
                    ;WinActivate, %Title%
                    Mouseclick,left,xx+23,yy
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
    
        formattime, currTime, , yyyyMMddhhmmss
        if (limitTime < currTime)
        {
            channelHome = 1
        }

        imagesearch,xx,yy,0,40,50,100, *%searchDetail% %workDir%\channelHome%fileName%.png
        if(ErrorLevel = 0)
        {
            ;WinActivate, %Title%
            Mouseclick,left,xx+10,yy+10

            mainHome:=0
            While (mainHome=0)
            {
                ;WinActivate, %Title%
                imagesearch,xx,yy,40,40,130,90, *%searchDetail% %workDir%\mainHome%fileName%.png
                if(ErrorLevel = 0)
                {
                    channelHome=1
                    mainHome=1
                    break
                }
            }
        }   
    }

    formattime, currTime, , yyyyMMddhhmmss
    if (limitTime < currTime)
    {
        break
    }
}

return

F12::
Reload

GuiClose:
ExitApp