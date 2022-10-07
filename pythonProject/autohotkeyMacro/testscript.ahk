#Warn All, off
SetWorkingDir %A_ScriptDir% ; Ensures a consistent starting directory.
CoordMode, Mouse, Screen

#Include gdip.ahk ; is in the post attachment if anyone needs

If (!pToken := Gdip_Startup()){
ExitApp
}
return

f1::
WinGet, id, ID, A
return

f2::
pBitmap := Gdip_BitmapFromHWND(id)
Gdip_SaveBitmapToFile(pBitmap, "screen.bmp", 100)
Gdip_DisposeImage(pBitmap)
return

f12::
exitapp