ControlSendNw(val, title) 
{
	;다 입력되지 않아서 추가 포커스를 삽입
	ControlSend,, {Space}, %Title%
	ControlSend,, {BackSpace}, %Title%
	ControlSend,, %val%, %Title%
}