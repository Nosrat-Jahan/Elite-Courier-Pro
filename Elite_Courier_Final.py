import tkinter as tk
from tkinter import ttk, messagebox


# ========================================================
# Project  : Elite Courier Pro [Build 1.1.0]
# Developer: Nosrat-Jahan | CSE Undergraduate
# Features : Dynamic Scaling, Multi-Theme Support, OOP
# ========================================================

class CourierManagementSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("Elite Courier Pro v1.1.0")

        # Initial window configuration for optimal visibility
        self.master.geometry("1100x750")
        self.master.minsize(1050, 700)

        # System States
        self.dark_mode_active = True
        self.current_zoom = 1.1  # Default zoom set to 1.1 for better readability
        self.order_database = []

        # UI Color Schematics (Industry Standard HEX)
        self.theme_config = {
            "dark": {
                "background": "#0F0F0F", "foreground": "#F2F2F2", "brand": "#2ECC71",
                "surface": "#1A1A1A", "danger": "#E74C3C", "warning": "#F1C40F", "border": "#2C3E50"
            },
            "light": {
                "background": "#F5F6FA", "foreground": "#2F3640", "brand": "#10B981",
                "surface": "#FFFFFF", "danger": "#E84118", "warning": "#FBC531", "border": "#DCDDE1"
            }
        }

        self.ui_colors = self.theme_config["dark"]
        self._init_interface()

    def _init_interface(self):
        """Initializes and re-renders the core UI components"""
        for widget in self.master.winfo_children():
            widget.destroy()

        color = self.ui_colors
        self.master.configure(bg=color["background"])

        # --- Top Navigation Bar ---
        top_bar = tk.Frame(self.master, bg=color["background"], pady=20)
        top_bar.pack(fill="x")

        # Dynamic Title Scaling
        font_scale = int(26 * self.current_zoom)
        tk.Label(top_bar, text="ELITE COURIER PRO", font=("Inter", font_scale, "bold"),
                 bg=color["background"], fg=color["brand"]).pack()

        # Workspace Utilities (Scale & Theme)
        ctrl_panel = tk.Frame(top_bar, bg=color["background"])
        ctrl_panel.place(x=30, y=25)

        btn_opt = {"font": ("Consolas", 12, "bold"), "bd": 0, "bg": color["surface"], "cursor": "hand2", "padx": 12}
        tk.Button(ctrl_panel, text="+", fg=color["brand"], command=lambda: self.update_view_scale(0.1), **btn_opt).pack(
            side="left", padx=4)
        tk.Button(ctrl_panel, text="-", fg=color["danger"], command=lambda: self.update_view_scale(-0.1),
                  **btn_opt).pack(side="left", padx=4)

        mode_label = "☀ Light" if self.dark_mode_active else "🌙 Dark"
        tk.Button(ctrl_panel, text=mode_label, font=("Inter", 10, "bold"), bd=1, relief="flat",
                  bg=color["surface"], fg=color["foreground"],
                  command=self.switch_theme_engine, padx=15).pack(side="left", padx=15)

        # --- Main Layout Container ---
        self.view_container = tk.Frame(self.master, bg=color["background"], padx=30, pady=10)
        self.view_container.pack(fill="both", expand=True)
        self.view_container.columnconfigure(1, weight=1)
        self.view_container.rowconfigure(0, weight=1)

        # Module: Shipment Entry Form
        self.side_form = tk.LabelFrame(self.view_container, text=" Shipment Entry ",
                                       font=("Inter", int(11 * self.current_zoom), "bold"),
                                       bg=color["background"], fg=color["brand"], padx=25, pady=25, bd=1)
        self.side_form.grid(row=0, column=0, sticky="nsw", padx=(0, 30))
        self._build_entry_form()

        # Module: Data Grid Table
        self.data_grid_panel = tk.Frame(self.view_container, bg=color["background"])
        self.data_grid_panel.grid(row=0, column=1, sticky="nsew")
        self._build_data_table()

    def _build_entry_form(self):
        """Constructs the input fields with adaptive font scaling"""
        color = self.ui_colors
        base_size = int(12 * self.current_zoom)

        lbl_cfg = {"bg": color["background"], "fg": color["foreground"], "font": ("Inter", base_size - 1)}
        ent_cfg = {"font": ("Inter", base_size), "bg": color["surface"], "fg": color["foreground"], "bd": 1,
                   "relief": "flat"}

        # Field: Customer Name
        tk.Label(self.side_form, text="Customer Entity:", **lbl_cfg).pack(anchor="w", pady=(5, 0))
        self.input_name = tk.Entry(self.side_form, **ent_cfg, insertbackground=color["foreground"])
        self.input_name.pack(fill="x", pady=10, ipady=8)
        self.input_name.focus_set()
        self.input_name.bind("<Return>", lambda e: self.input_addr.focus_set())

        # Field: Address
        tk.Label(self.side_form, text="Destination Link:", **lbl_cfg).pack(anchor="w", pady=(5, 0))
        self.input_addr = tk.Entry(self.side_form, **ent_cfg, insertbackground=color["foreground"])
        self.input_addr.pack(fill="x", pady=10, ipady=8)
        self.input_addr.bind("<Return>", lambda e: self.input_charge.focus_set())

        # Field: Billing Charge
        tk.Label(self.side_form, text="Billing Amount ($):", **lbl_cfg).pack(anchor="w", pady=(5, 0))
        self.input_charge = tk.Entry(self.side_form, **ent_cfg, insertbackground=color["foreground"])
        self.input_charge.pack(fill="x", pady=10, ipady=8)
        self.input_charge.bind("<Return>", lambda e: self.process_new_shipment())

        # Logic Triggers
        tk.Button(self.side_form, text="REGISTER SHIPMENT", font=("Inter", base_size, "bold"),
                  bg=color["brand"], fg="white", bd=0, cursor="hand2",
                  command=self.process_new_shipment).pack(fill="x", pady=(35, 12), ipady=14)

        tk.Button(self.side_form, text="Audit Revenue", font=("Inter", base_size - 2, "bold"),
                  bg=color["surface"], fg=color["brand"], bd=1, relief="groove",
                  command=self.trigger_revenue_audit).pack(fill="x", pady=6, ipady=10)

        tk.Button(self.side_form, text="SYSTEM MANIFEST", font=("Inter", base_size - 3, "bold"),
                  bg=color["surface"], fg=color["foreground"], bd=1, relief="groove",
                  command=self.trigger_about_info).pack(fill="x", pady=(35, 0), ipady=8)

    def _build_data_table(self):
        """Initializes the data grid with dynamic column resizing"""
        color = self.ui_colors
        font_size = int(11 * self.current_zoom)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=color["surface"], foreground=color["foreground"],
                        fieldbackground=color["surface"], rowheight=int(45 * self.current_zoom),
                        font=("Inter", font_size), borderwidth=0)
        style.configure("Treeview.Heading", background=color["background"], foreground=color["foreground"],
                        font=("Inter", font_size, "bold"))

        self.shipment_table = ttk.Treeview(self.data_grid_panel, columns=("SN", "Entity", "Status", "Cost"),
                                           show="headings")

        # Scaling column widths based on global zoom level
        cols = {"SN": 60, "Entity": 300, "Status": 160, "Cost": 120}
        for key, val in cols.items():
            self.shipment_table.heading(key, text=key.upper())
            self.shipment_table.column(key, width=int(val * self.current_zoom), anchor="center")

        self.shipment_table.pack(fill="both", expand=True)

        # Life-cycle Control Panel
        op_bar = tk.Frame(self.data_grid_panel, bg=color["background"], pady=20)
        op_bar.pack(fill="x")

        b_opt = {"font": ("Inter", font_size, "bold"), "bd": 1, "padx": 20, "pady": 10, "cursor": "hand2",
                 "relief": "flat"}

        tk.Button(op_bar, text="DELIVERED", bg=color["surface"], fg=color["brand"], **b_opt,
                  command=lambda: self.update_parcel_lifecycle("Delivered")).pack(side="left", padx=5)
        tk.Button(op_bar, text="RETURNED", bg=color["surface"], fg=color["warning"], **b_opt,
                  command=lambda: self.update_parcel_lifecycle("Returned")).pack(side="left", padx=5)
        tk.Button(op_bar, text="VOID ORDER", bg=color["surface"], fg=color["danger"], **b_opt,
                  command=lambda: self.update_parcel_lifecycle("Voided")).pack(side="left", padx=5)
        tk.Button(op_bar, text="PURGE", bg=color["surface"], fg="#7F8C8D", **b_opt, command=self.purge_entry).pack(
            side="right", padx=5)

    def trigger_dialog_box(self, title, content):
        """Generic copyable dialog for financial audits and manifest data"""
        color = self.ui_colors
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.geometry("520x350")
        popup.configure(bg=color["surface"])
        popup.transient(self.master)
        popup.grab_set()

        output = tk.Text(popup, font=("Inter", 12), bg=color["surface"], fg=color["foreground"],
                         bd=0, padx=35, pady=35, height=10)
        output.insert("1.0", content)
        output.configure(state="disabled")
        output.pack(fill="both", expand=True)

        tk.Button(popup, text="ACKNOWLEDGE", font=("Inter", 11, "bold"), bg=color["brand"],
                  fg="white", bd=0, padx=40, pady=12, command=popup.destroy).pack(pady=25)

    def update_view_scale(self, factor):
        """Updates global multiplier and triggers a full UI re-render"""
        next_scale = self.current_zoom + factor
        if 0.8 <= next_scale <= 1.5:
            self.current_zoom = next_scale
            self._init_interface()
            self._sync_table_view()

    def switch_theme_engine(self):
        """Swaps UI colors between Light and Dark mode configs"""
        self.dark_mode_active = not self.dark_mode_active
        self.ui_colors = self.theme_config["dark"] if self.dark_mode_active else self.theme_config["light"]
        self._init_interface()
        self._sync_table_view()

    def process_new_shipment(self):
        """Validates inputs and commits entry to memory"""
        name, loc, val = self.input_name.get(), self.input_addr.get(), self.input_charge.get()
        if name and loc and val:
            try:
                numeric_val = float(val)
                self.order_database.append({"client": name, "fee": numeric_val, "state": "In Transit"})
                self._sync_table_view()
                self.input_name.delete(0, tk.END);
                self.input_addr.delete(0, tk.END);
                self.input_charge.delete(0, tk.END)
                self.input_name.focus_set()
            except ValueError:
                print("Logging: Illegal entry detected in numeric billing field.")

    def _sync_table_view(self):
        """Refreshes Treeview entries based on current order_database state"""
        for node in self.shipment_table.get_children():
            self.shipment_table.delete(node)
        for idx, item in enumerate(self.order_database, 1):
            self.shipment_table.insert("", "end", values=(idx, item['client'], item['state'], f"${item['fee']:.2f}"))

    def update_parcel_lifecycle(self, status_str):
        """Updates the status attribute for selected treeview nodes"""
        target = self.shipment_table.selection()
        if target:
            for node in target:
                data = list(self.shipment_table.item(node, "values"))
                data[2] = status_str
                self.shipment_table.item(node, values=data)

    def purge_entry(self):
        """Removes records from UI with a security confirmation prompt"""
        target = self.shipment_table.selection()
        if target and tk.messagebox.askyesno("Confirm Purge", "Permanently delete selected shipment record?"):
            for node in target:
                self.shipment_table.delete(node)

    def trigger_revenue_audit(self):
        """Calculates aggregate billing fees from active shipments"""
        revenue = sum(item["fee"] for item in self.order_database)
        self.trigger_dialog_box("Financial Audit",
                                f"Total Tracked Revenue Stream:\n${revenue:.2f}\n\n[Data snapshot ready for external logging]")

    def trigger_about_info(self):
        """Displays system meta-data and architectural info"""
        manifest = (
            "Elite Courier Pro | Build 1.1.0\n"
            "-------------------------------------\n"
            "Lead Developer: Nosrat-Jahan\n"
            "Professional Status: CSE Undergraduate\n\n"
            "Tech Stack: Python 3.x with Tkinter UI Framework\n\n"
            "High-performance, object-oriented logistics solution \ndesigned for desktop scalability."
        )
        self.trigger_dialog_box("System Manifest", manifest)


if __name__ == "__main__":
    root_engine = tk.Tk()
    # Apply High-DPI Awareness for Windows OS clarity
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        print(f"DPI Awareness Notification: {e}")

    app = CourierManagementSystem(root_engine)
    root_engine.mainloop()