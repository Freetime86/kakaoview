;카카오뷰 메인 루프
loopviews(cnt, selType, startRangeX, startRangeY, searchRangeX, searchRangeY, searchDetail, Delay, winTitle, waitTime) 
{
    Loop, %cnt%
    {
        ;이미 좋아요가 선택되어 있으면 우회
        imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %A_scriptDir%\nonTargetLike_%selType%.bmp
        if(ErrorLevel = 0) 
        {
            viewCapture(winTitle)
            Sleep, %Delay%
            viewClicker(cnt, selType, startRangeX, startRangeY, searchRangeX, searchRangeY, searchDetail, Delay, winTitle, waitTime)
        
        ;좋아요가 선택되어 있지 않으면 좋아요 선택 진행
        } else {
            imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %A_scriptDir%\targetLike_%selType%.bmp
            if(ErrorLevel = 0) 
            {

            }
        }
    }
}

;카카오뷰 클릭 모듈
viewClicker(cnt, selType, startRangeX, startRangeY, searchRangeX, searchRangeY, searchDetail, Delay, winTitle, waitTime)
{
    boardTabChecker:=0
    While (boardTabChecker=0)
    {
        ;첫번째 보드 찾기
        imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %A_scriptDir%\boardTabChecker_%selType%.bmp
        if(ErrorLevel = 0)
        {
            MsgBox, 첫번째 보드 찾기 성공
            WinActivate, %winTitle%
            Mouseclick,left,xx,yy+50
            
            loadingOn=0
            While (loadingOn=0)
            {
                ;로딩바 체크
                imagesearch,xx,yy,741,117,1195,130, *%searchDetail% %A_scriptDir%\boardTabChecker_%selType%.bmp
                if(ErrorLevel = 0)
                {
                    loadingOn=1
                }
            }

            loadingOff=0
            While (loadingOff=0)
            {
                ;로딩바 체크
                imagesearch,xx,yy,741,117,1195,130, *%searchDetail% %A_scriptDir%\boardTabChecker_%selType%.bmp
                if(ErrorLevel != 0)
                {
                    loadingOff=1
                    Sleep, %waitTime%
                    viewScrolling(winTitle)
                    Sleep, %Delay%

                    ;보드탭 나가기
                    ;imagesearch,xx,yy,startRangeX,startRangeY,searchRangeX,searchRangeY, *%searchDetail% %A_scriptDir%\exitBoardTab_%selType%.bmp
                    ;if(ErrorLevel != 0)
                    ;{
                        ;WinActivate, %winTitle%
                        ;Mouseclick,left,xx,yy
                    ;}
                }
            }
        }
    }
}

;카카오뷰 스크롤링
viewScrolling(winTitle)
{
    WinActivate, %winTitle%
    Mouseclick,left,758,952
    Sleep, 2000
    Mouseclick,left,763,980
    Sleep, 1000
    Mouseclick,left,763,980
    Sleep, 1000
    Mouseclick,left,763,980
    Sleep, 1000
    Mouseclick,left,763,980
    Sleep, 1000
    MouseClickDrag, L, 763, 903, 744, 903
    Sleep, 1000
    viewCapture(winTitle)
}

;카카오뷰 스크롤링
viewScrollRun(winTitle)
{
    WinActivate, %winTitle%
    Mouseclick,left,750,315
    Sleep, 100
    MouseClickDrag, L, 750, 315, 750, 175
    Sleep, 1000
}

;카카오뷰 캡처
viewCapture(winTitle)
{
    WinActivate, %winTitle%
    Mouseclick,left,850,1015
}