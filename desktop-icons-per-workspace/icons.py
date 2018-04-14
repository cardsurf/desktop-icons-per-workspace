from gi.repository import Gtk
from gi.repository import Pango
import sys
import os



columns = [ "File name", "Is visible" ];
row_filename_index = 0;
row_is_visible_index = 1;

def read_csv(filepath):
    rows = []
    with open(filepath, 'r') as f:
        for line in f.readlines():
            row = line.strip().split(',')
            rows.append(row)
    return rows;

class MyWindow(Gtk.ApplicationWindow):

    def __init__(self, app):

        Gtk.Window.__init__(self, title="Visible files", application=app);
        
        # Set windows initial size
        self.set_default_size(800, 600);

        # Create model
        self.model = Gtk.ListStore(str, bool)

        # Get list of desktop files
        self.home = os.path.expanduser('~');
        self.desktop = os.path.join(self.home, "Desktop");
        files = os.listdir(self.desktop);

        # Populate model
        for file in files:
            filename = os.path.basename(file);
            is_visible = filename[0] != '.';
            model_row = [ filename, is_visible ];
            self.model.append(model_row);

        # Create view
        self.view = Gtk.TreeView(model=self.model)

        for i, column in enumerate(columns):
            cell = None
            column = None

            if i == row_filename_index:
                # Add filename column
                cell = Gtk.CellRendererText();
                cell.props.weight_set = True;
                cell.props.weight = Pango.Weight.BOLD;
                column = Gtk.TreeViewColumn(columns[i], cell, text=i)
            elif i == row_is_visible_index:
                # Add is visible column
                cell = Gtk.CellRendererToggle();
                cell.connect("toggled", self.on_checkbox_toggled, i, columns[i]);
                column = Gtk.TreeViewColumn(columns[i], cell)
                column.add_attribute(cell, "active", 1)

            column.set_fixed_width(380);
            column.set_resizable(True);
            self.view.append_column(column)

        # Create scrollbar
        self.scrolled_window = Gtk.ScrolledWindow();
        self.scrolled_window.set_border_width(10);
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.ALWAYS);
        # Add view
        self.scrolled_window.add(self.view);

        # Create buttons
        self.button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6);
        self.button_apply = Gtk.Button(label="Apply");
        self.button_apply.connect("clicked", self.on_button_apply_clicked);
        self.button_close = Gtk.Button(label="Close");
        self.button_close.connect("clicked", self.on_button_close_clicked);
        self.button_box.pack_start(self.button_apply, True, True, 0);
        self.button_box.pack_start(self.button_close, True, True, 0);

        # Add scrollbar and buttons
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6);
        self.box.expand = False;
        self.box.fill = False;
        self.box.pack_start(self.scrolled_window, True, True, 0);
        self.box.pack_start(self.button_box, False, False, 0);
        self.add(self.box);

    # Toggle checkbox
    def on_checkbox_toggled(self, widget, path, column, data):
        self.model[path][column] = not self.model[path][column]

    # Toggle file visbility
    def on_button_apply_clicked(self, widget):
        for i, model_row in enumerate(self.model):

            filename_old = model_row[row_filename_index];
            filename_new = filename_old;
            is_visible = filename_old[0] != '.';
            is_checked = model_row[row_is_visible_index];

            if is_visible and not is_checked:
                filename_new = "." + filename_old;
            elif not is_visible and is_checked:
                filename_new = filename_old[1:];

            if(filename_old != filename_new):
                filepath_old = os.path.join(self.desktop, filename_old);
                filepath_new = os.path.join(self.desktop, filename_new);
                os.rename(filepath_old, filepath_new);
                self.model[i][row_filename_index] = filename_new;
                break;

    # Close application
    def on_button_close_clicked(self, widget):
        application = self.get_application();
        Gtk.Application.quit(application);




class MyApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self);

    def do_activate(self):
        win = MyWindow(self);
        win.show_all();

    def do_startup(self):
        Gtk.Application.do_startup(self);


app = MyApplication()
status = app.run(sys.argv)
sys.exit(status)

