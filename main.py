from widget_fact import *
from model import *
from controller import *
from view import *




def main():
    root = tk.Tk()
    factory = WidgetFactory()
    model = ApplicationModel()
    controller = ApplicationController(model, None)
    view = ApplicationView(root, factory, model, controller)
    controller.view = view
    root.mainloop()

if __name__ == "__main__":
    main()
