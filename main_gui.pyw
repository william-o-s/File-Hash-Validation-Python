import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import filedialog
from tkinter import messagebox

from hash_valid_lib import HashFile
from hash_valid_lib import get_avail_hash_types

HASH_TYPES = get_avail_hash_types()

class MainApplication(tk.Frame):
    def __init__(self, parent: tk.Tk, *args, **kwargs):
        """MainApplication contains the Tkinter Frame that forms the main GUI.

        @parent: A Tkinter Tk root parent window for the frame to bind to.
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        #####################
        ### Main Frames setup
        frame_file = tk.Frame(master=parent)
        frame_hashes = tk.Frame(master=parent, relief=tk.GROOVE, borderwidth=5)
        frame_action = tk.Frame(master=parent)

        # NOTE: Layout arranging
        frame_file.pack(ipadx=5, ipady=5, fill=tk.X)
        frame_hashes.pack(padx=5, pady=5, fill=tk.BOTH)
        frame_action.pack(ipadx=5, ipady=5, fill=tk.X)
    
        ##############################
        ### File Selection Frame setup
        label_file = tk.Label(master=frame_file, text="File Address")
        
        self.file_addr = tk.StringVar()
        entry_file = tk.Entry(
                            master=frame_file,
                            width=50,
                            textvariable=self.file_addr)

        button_file = tk.Button(master=frame_file,
                                text="...",
                                command=lambda: self.tk_find_file(
                                                                entry_file,
                                                                self.file_addr))
        # NOTE: The button's command uses a lambda to pass an argument. This can
        # be done instead of partial becauses the argument is not changing here

        # NOTE: Layout setup
        label_file.pack(side=tk.LEFT, padx=3)
        entry_file.pack(side=tk.LEFT, padx=3)
        button_file.pack(side=tk.LEFT, padx=3)

        #####################################
        ### Hash Calculation/Validation Frame
        label_hash_header = tk.Label(
                                    master=frame_hashes,
                                    text="Expected Hashes",
                                    font="Verdana 16 bold")
        label_hash_header.grid(row=0, column=0, columnspan=3)

        # NOTE: To keep the code more flexible with supported hash types, a loop
        # over the possible hash types is used along with a procedural
        # generation of corresponding UI elements (in this case, the Hash Frame)
        self.hash_frame = {}
        for index, hash_type in enumerate(HASH_TYPES, 1):
            textvar_entry_hash = StringVar()
            textvar_label_hashresult = StringVar(value="Waiting")

            label_hash = tk.Label(master=frame_hashes, text=hash_type)
            entry_hash = tk.Entry(
                                    master=frame_hashes,
                                    width=50,
                                    textvariable=textvar_entry_hash)
            label_hashresult = tk.Label(
                                    master=frame_hashes,
                                    textvariable=textvar_label_hashresult)

            # NOTE: Layout setup
            label_hash.grid(row=index, column=0, sticky='e')
            entry_hash.grid(row=index, column=1, sticky='w')
            label_hashresult.grid(row=index, column=2)

            self.hash_frame[hash_type] = {
                                    "ui_entry": entry_hash,
                                    "ui_result": label_hashresult,
                                    "textvar_entry_hash": textvar_entry_hash,
                                    "textvar_result": textvar_label_hashresult
                                    }
        
        ########################
        ### Action Buttons Frame
        self.textvar_status = StringVar(value="Waiting for file")
        self.label_status = tk.Label(
                                    master=frame_action,
                                    font="Verdana 12 bold",
                                    textvariable=self.textvar_status)
                
        self.progressbar_status = ttk.Progressbar(
                                                master=frame_action,
                                                orient=tk.HORIZONTAL,
                                                length=300,
                                                mode='indeterminate')

        self.button_validate = tk.Button(
                                        master=frame_action,
                                        text="Validate",
                                        command=self.validate_all_hashes,
                                        foreground="white",
                                        background="green")

        self.label_status.pack()
        self.progressbar_status.pack(fill=tk.X, pady=10)
        self.button_validate.pack()
    
    def tk_find_file(
                    self,
                    entry: tk.Entry,
                    textvar_entry: tk.StringVar) -> None:
        """Opens a Tkinter file-selection dialog and inserts a selected file's
        directory address into the given Entry element.

        @entry: The Tkinter Entry element containing the directory address.
        @textvar_entry: The StringVar used to contain the Entry element text.
        """
        file_addr = filedialog.askopenfilename(
                                            title="Select target file...",
                                            initialdir="./")
        if file_addr:
            textvar_entry.set(file_addr)
            entry.xview(tk.END)
            self.textvar_status.set("Ready")
    
    def validate_all_hashes(self) -> None:
        """Checks the target file's hash against all given expected hashes.
        """

        # NOTE: Calculation flow:
        #           1. Checks whether a file directory address exists.
        #           2. Iterates over each hash type where an expected hash is
        #               present
        #           3. Calculates the relevant hash and compares it with the
        #               expected hash, updating the UI accordingly
        if self.file_addr.get():
            hashfile = HashFile(self.file_addr.get())
            self.start_progress(True)
            
            for hash_type in HASH_TYPES:
                # NOTE: This may look confusing. In order to access both the UI
                # elements on the application, I save the objects into a
                # dictionary so that it can be picked up by self.
                expected_hash = self.hash_frame[hash_type]["textvar_entry_hash"].get()

                if expected_hash:
                    self.hash_frame[hash_type]["textvar_result"].set("Processing")
                    self.textvar_status.set("Processing "+hash_type)
                    self.parent.update()
                    
                    hashstring = hashfile.hashCalculate(hash_type=hash_type)

                    if hashstring == expected_hash:
                        self.update_frame_hash_status(
                                            hash_type,
                                            "white",
                                            "green",
                                            "Valid")
                    else:
                        self.update_frame_hash_status(
                                            hash_type,
                                            "black",
                                            "red",
                                            "Invalid")
                else:
                    self.update_frame_hash_status(
                                        hash_type,
                                        "black",
                                        "white",
                                        "Waiting")

            self.start_progress(False)

        else:
            messagebox.showerror(
                        title="No target file!",
                        message="Please give a file directory address first.")

    def start_progress(self, starting: bool):
        if starting:
            self.progressbar_status.start()
        else:
            self.textvar_status.set("Finished")
            self.progressbar_status.stop()
    
    def update_frame_hash_status(self, 
                        hash_type: str,
                        foreground: str,
                        background: str,
                        status: str):
        self.hash_frame[hash_type]["ui_entry"].configure(
                                                        foreground=foreground,
                                                        background=background)
        self.hash_frame[hash_type]["textvar_result"].set(status)
        self.parent.update()



def main():
    """CLI-based program.
    """

    #############################
    ### Tkinter Root Window Setup
    tk_root_window = tk.Tk()
    tk_root_window.resizable(width=False, height=False)
    tk_root_window.title("File-Hash Validation")
    tk_root_window.eval("tk::PlaceWindow . center")
    tk_root_window.iconbitmap("img/icon.ico")

    ###########
    ### GUI run
    app = MainApplication(tk_root_window)
    app.pack(fill=tk.BOTH)
    tk_root_window.mainloop()

if __name__ == '__main__':
    main()
