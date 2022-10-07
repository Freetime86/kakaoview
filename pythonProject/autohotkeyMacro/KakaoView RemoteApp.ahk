Gui, Add, Text, x15 y15 w150 h30, 한탄강오토캠핑장 매크로
Gui, Add, Button, x15 y40 w90 h30, 예약시작
Gui, Add, Button, x105 y40 w90 h30, 초기화
Gui, Add, Button, x15 y70 w90 h30, 재실행
Gui, Add, Button, x105 y70 w90 h30, 일시정지
Gui, Add, Radio, x15 y110 w70 h15 vR1 Checked, 1박2일
Gui, Add, Radio, x15 y130 w70 h15 vR2, 2박3일
Gui, Add, Radio, x15 y150 w70 h15 vR3, 3박4일
Gui, Add, Checkbox, x15 y170 w150 h15 vC1 Checked, 강변야영장(마사토)
Gui, Add, Checkbox, x15 y190 w150 h15 vC2 Checked, 강변야영장(파쇄석)
Gui, Add, Checkbox, x15 y210 w150 h15 vC3 Checked, 언덕야영장(파쇄석)
Gui, Add, Text, x15 y240 w150 h20, 결재정보 입력
Gui, Add, Text, x15 y265 w30 h20, 이름
Gui, Add, Edit, x45 y260 w50 h20 vName, 박상민
Gui, Add, Text, x15 y290 w50 h20, 생년월일
Gui, Add, Edit, x70 y285 w80 h20 vBirth, 860705
Gui, Add, Text, x15 y315 w40 h20, 이메일
Gui, Add, Edit, x55 y310 w60 h20 vMailid, psm0705
Gui, Add, Text, x115 y315 w40 h20, @
Gui, Add, Edit, x127 y310 w70 h20 vMaildo, gmail.com
Gui, Add, Text, x15 y340 w40 h20, 연락처
Gui, Add, Edit, x55 y335 w30 h20 vPhone1, 010
Gui, Add, Edit, x90 y335 w30 h20 vPhone2, 2486
Gui, Add, Edit, x125 y335 w30 h20 vPhone3, 3038
Gui, Add, Text, x15 y365 w80 h20, 비밀번호
Gui, Add, Edit, x75 y360 w120 h20 vPass, cjswosla86
Gui, Add, Text, x15 y390 w80 h20, 차량번호
Gui, Add, Edit, x75 y385 w80 h20 vLicenceNo, 176너5418

Gui, Add, Text, x15 y430 w150 h20, 윈도우 창 명 입력
Gui, Add, Edit, x15 y450 w180 h20 vTitle, 상민의 Galaxy S20+ 5G
Gui, Add, Text, x15 y480 w180 h20, 정확도 1-255  처리 1000 = 1초
Gui, Add, Edit, x15 y500 w70 h20 vimageAccuracy, 50
Gui, Add, Edit, x90 y500 w70 h20 vdelay, 50
Gui, Show

Return

Button예약시작:
;GUI 변동 값 확정
Gui,Submit,nohide

;유저 세팅 변수 선언
;라디오
if R1 = 1
	targetCount:=1
if R2 = 1
	targetCount:=2
if R3 = 1
	targetCount:=3
;선호사이트, C1:강변야영장(마사토), C2:강변야영장(파쇄석), C3:언덕야영장(파쇄석)
if C1 = 1
	siteA:=1
if C2 = 1
	siteB:=2
if C3 = 1
	siteC:=3

;개발자용 기본 세팅 VALUE
workDir=%A_scriptDir%\image

;script import
#Include %A_scriptDir%\Gdip_All.ahk
#Include %A_scriptDir%\Gdip_ImageSearch.ahk

PostClick(FoundX,FoundY){

	lparam:=FoundX|FoundY<<16

	PostMessage,0x201,1,%lparam%,,%Title%

	PostMessage,0x202,0,%lparam%,,%Title%

	Sleep, 1000

}

Loop
{
    path=%workDir%\heart_empty.bmp
    WinActivate, %Title%
    imagesearch,x,y,0,0,1920,1080, *%imageAccuracy% %path%
    if(ErrorLevel = 0) 
    {
        ;ControlClick,xfx yfy, %Title%,,,, NA
        ;ImageSearch, fx,fy, 0,0,%A_ScreenWidth%,%A_ScreenHeight%,*%imageAccuracy% %workDir%\areaSite%A_Index%.bmp
        ;lparam:=xx|yy<<16
        ;PostMessage, 0x201,1, %lparam%, ,%Title%
        ;PostMessage, 0x202,1, %lparam%, ,%Title%
        postclick(x,y)
        ;Mouseclick,left,x,y
        break
    }

}
return


Gdip_Shutdown(pToken)
Return

Button초기화:
Reload

Button재실행:
Suspend

Button일시정지:
Pause

;재시작
F3::
Reload