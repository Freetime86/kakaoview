GetMWeek(Cal)
{
	FormatTime, _YYYY, %Cal%, yyyy
	FormatTime, _MM, %Cal%, M
	FormatTime, _DD, %Cal%, d

	timeString := _YYYY "0101"

	;시작일 매년 01월 01일
	FormatTime, currentDate,%timeString%,yyyyMMdd
	FormatTime, daySeq, %timeString%, WDay ; 1,2,3,4,5,6,7 1은 일요일
	;일요일시작기점 신규 주차 시작시점은 8번째 = 1번째
	addSeq:= 8-daySeq
	
	;기본1주차 시작 최대 매월 5주차까지만 카운트
	weekCount:=1
	FormatTime, preyear, %currentDate%, yyyy
	FormatTime, premonth, %currentDate%, M
	FormatTime, preday, %currentDate%, d

	;최초 주차 일요일 값으로 세팅
	currentDate += addSeq, days
	loop
	{
		FormatTime, thismonth, %currentDate%, M
		FormatTime, thisDay, %currentDate%, d

		;다음 주차로 이동 시 월 변경이 일어나면 주차 카운트 1로 초기화
		if (premonth != thismonth)
		{
			;달 변경시 현재 달 정보 저장 비교 값으로 사용하기 위함
			FormatTime, preyear, %currentDate%, yyyy
			FormatTime, premonth, %currentDate%, M
			FormatTime, preday, %currentDate%, d
			weekCount:=1
		} else {
			;1주차씩 올리기
			currentDate += 7, days
			weekCount++
		}

		;날짜 차일 체크 -7 ~ 7 범주내에 들어와야 해당 차수 인정
		pdiffDays:= _DD - thisDay
		mdiffDays:= thisDay - _DD
		if (_MM = thismonth And (pdiffDays < 7 OR mdiffDays > -7))
		{
			calWeek := weekCount
			break
		}
	}
	return calWeek
}