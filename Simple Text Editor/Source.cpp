#include<FL/Fl.h>
#include<FL/Fl_Box.h>
#include<FL/Fl_Window.h>
#include <FL/Fl_Double_Window.H>
#include< FL/Fl_Text_Buffer.h>
#include <FL/Fl_Button.H>
#include <FL/Fl_Input.H>
#include <FL/Fl_Return_Button.H>
#include <FL/Fl_Text_Editor.H>
#include <FL/Fl_Menu_Item.H>
#include<FL/Fl_Menu_Bar.H>
#include<FL/fl_ask.H>
#include<string>
#include<iostream>

using namespace std;

class EditorWindow : public Fl_Double_Window {
public:
    EditorWindow(int w, int h, const char* t);
    ~EditorWindow() {
    };

    Fl_Window* replace_dlg;
    Fl_Input* replace_find;
    Fl_Input* replace_with;
    Fl_Button* replace_all;
    Fl_Return_Button* replace_next;
    Fl_Button* replace_cancel;

    Fl_Text_Editor* editor;
    char search[256];

   
};
int changed = 0;
char filename[256] = "";
Fl_Text_Buffer* textbuf;


int loading = 0;
void load_file(char* newfile, int ipos) {
    loading = 1;
    int insert = (ipos != -1);
    changed = insert;
    if (!insert) strcpy(filename, "");
    int r;
    if (!insert) r = textbuf->loadfile(newfile);
    else r = textbuf->insertfile(newfile, ipos);
    if (r)
        fl_alert("Error reading from file \'%s\':\n%s.", newfile, strerror(errno));
    else
        if (!insert) strcpy(filename, newfile);
    loading = 0;
    textbuf->call_modify_callbacks();
}

int main(int argc, char **argv)
{
	/*Fl_Window window(200, 200, "Window title");
	Fl_Box box(0, 0, 200, 200, "Hey, I mean, Hello, World!");
	window.show();*/
    textbuf = new Fl_Text_Buffer;
    Fl_Window* window = new Fl_Window(300, 180);
    window->show(1, argv);

   //if (argc > 1) load_file(argv[1], -1);
    const char* file = "text1.txt";
    char* newStr = new char[strlen(file) + 1];
    strcpy(newStr, file);
    load_file(newStr, -1);

	return Fl::run();
}
