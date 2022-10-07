def compareboard(lastBoardList, current_title):
    result = True
    for title in lastBoardList:
        print("제목 비교 : " + current_title)
        print("입력 대상 - " + title)
        if title == current_title:
            result = False
    return result


def filterWords(wordList, compareSentence):
    result = True

    for badWord in wordList:
        if compareSentence.find(badWord) == 0:
            print("현재 제목 : " + compareSentence)
            print("문제의 단어 : " + badWord)
            result = False

    return result


def split_input_data(input_data):
    result_list = []
    try:
        input_data = input_data.strip().replace('\n', '').replace(' ', '')
        for channel in input_data.split(','):
            if channel != '':
                result_list.append(channel)
    finally:
        return result_list
