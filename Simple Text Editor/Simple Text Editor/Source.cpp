#include<FL/Fl.h>
#include<FL/Fl_Box.h>
#include<FL/Fl_Window.h>
#include <FL/Fl_Double_Window.H>
#include< FL/Fl_Text_Buffer.h>
#include <FL/Fl_Button.H>
#include <FL/Fl_Input.H>
#include <FL/Fl_Return_Button.H>
#include <FL/Fl_Text_Editor.H>


int            changed = 0;
char           filename[256] = "";
Fl_Text_Buffer* textbuf;

class EditorWindow : public Fl_Double_Window {
public:
    EditorWindow(int w, int h, const char* t) {
    };
    ~EditorWindow() {
    };

    Fl_Window* replace_dlg;
    Fl_Input* replace_find;
    Fl_Input* replace_with;
    Fl_Button* replace_all;
    Fl_Return_Button* replace_next;
    Fl_Button* replace_cancel;

    Fl_Text_Editor* editor;
    char               search[256];
};





int main()
{
	Fl_Window window(200, 200, "Window title");
	Fl_Box box(0, 0, 200, 200, "Hey, I mean, Hello, World!");
	window.show();
	return Fl::run();
}
