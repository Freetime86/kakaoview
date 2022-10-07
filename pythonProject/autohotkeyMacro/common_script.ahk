;function for click with non activate on computer screen
post_click(output, title)
{
    StringSplit, LISTArray, output, `, 
    fx:=LISTArray1 
    fy:=LISTArray2

    lparam:=fx|fy<<16
    PostMessage, 0x201,1, %lparam%, ,%title%
    PostMessage, 0x202,1, %lparam%, ,%title%
}