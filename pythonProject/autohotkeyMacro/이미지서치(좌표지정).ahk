F1::
Loop, 1
{
ImageSearch,vx,vy, 272,395,285,411,*60 로.png
	if ErrorLevel=0
	{
		
		Click,%vx%,%vy%
		Sleep,800

	}

	if ErrorLevel=1
	{
		MsgBox, 인식을 못한다 이미지바꿔라
	}
}
return

F2::Pause
F3::ExitApp