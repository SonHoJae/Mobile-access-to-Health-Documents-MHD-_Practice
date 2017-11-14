import tkinter as tk
from tkinter.filedialog import askopenfile
import _client
import json
class TkinterUI(tk.Frame):
    def __init__(self, parent): 

        self.parent = parent

        self.file = None

        self.button_get = tk.Button(text='GET', command= self.getBtnListener)
        self.button_get.config(width = 10)
        self.button_get.grid(row=0,column=0)

        self.button_post = tk.Button(text='POST', command=self.postBtnListener)
        self.button_post.config(width = 10)
        self.button_post.grid(row=1,column=0)

        self.button_upload = tk.Button(text="UPLOAD", command=self.uploadChooseBtnListener)
        self.button_upload.config(width=10)
        self.button_upload.grid(row=2,column=0)

        self.button_retrieve = tk.Button(text="RETRIEVE", command=self.retrieveBtnListener)
        self.button_retrieve.config(width=10)
        self.button_retrieve.grid(row=3,column=0)

        self.button_postDocument = tk.Button(text="POST_DOCUMENT", command=self.postDocumentBtnListener)
        self.button_postDocument.config(width=10)
        self.button_postDocument.grid(row=4,column=0)

        self.label_address = tk.Label(self.parent, text = 'Address', bg = "#a1dbcd")
        self.label_address.grid(row = 0, column=1)

        self.entry_address = tk.Entry(self.parent)
        self.entry_address.config(width = 40)
        self.entry_address.grid(padx=10,row=1,column=1)

        self.label_json = tk.Label(self.parent, text = 'json', bg = "#a1dbcd")
        self.label_json.grid(row = 3, column=1)

        self.text_json = tk.Text(self.parent)
        self.text_json.config(width = 40,height=10)
        self.text_json.grid(padx=10,row=4,column=1) 
        
        self.label_result = tk.Label(self.parent,text = 'Result', bg = "#a1dbcd")
        self.label_result.grid(row=5,column=1,)

        self.text_result = tk.Text(self.parent)
        self.text_result.config(width = 40,height=10)
        self.text_result.grid(padx=10,row=6,column=1) 

        self.button_submit = tk.Button(text="Submit", command = self.submitBtnListener)
        self.button_submit.config(width = 10)
        self.button_submit.grid(row=7,column=1)

    def mainLoop(self):
        self.parent.mainloop()
        
    def getBtnListener(self): 
        self.text_result.delete('1.0', 'end')
        base = '/'.join(self.entry_address.get().rsplit('/')[0:3])
        base = base+'/'
        query = '/'.join(self.entry_address.get().rsplit('/')[3:])
        print('aa')
        print(base)
        print(query)
        self.text_result.insert('end', _client.getInformation(base, query))

    def postBtnListener(self): 
        self.text_result.delete('1.0', 'end')
        self.text_result.insert('end', _client.post(self.entry_address.get(), self.text_json.get('1.0', 'end')))

    def uploadChooseBtnListener(self):
        self.file = askopenfile("r")
        self.text_result.insert('end','filename:'+self.file.name)
        self.entry_address.delete(0, 'end')
        self.entry_address.insert(0,'http://localhost:5002/hojae/upload/'+self.file.name.split('/')[-1])

    def postDocumentBtnListener(self):
        self.file = askopenfile("r")
        self.text_result.delete('1.0', 'end')
        print(self.entry_address.get())
        print(self.file.name)
        self.text_result.insert('end',_client.postBundle(self.entry_address.get(),self.file.name))

    def submitBtnListener(self):
        _client.transferFile(self.file, self.entry_address.get())
        
    def retrieveBtnListener(self):
        _client.retrieveFile(self.entry_address.get())
    

    def defaultJson(self,default):
        default = {
            "Patient": {
                "administrativeGenderCode": "M", 
                "birthTime": "19910707", 
                "patientName": "Hojae"
            }
        }
        self.text_json.insert('end',json.dumps(default))
    def defaultAddress(self,default):
        default = {
            "Patient": {
                "administrativeGenderCode": "M", 
                "birthTime": "19910707", 
                "patientName": "Hojae"
            }
        }
        default = 'http://localhost:8080/REST/Binary/108fba88a-dbd9-45b8-9dc0-b41a706bb6ab'
        self.entry_address.insert(0,default)
        
def mainLoop():
    window = tk.Tk()
    window.title("Embeded Computing_hojae") 
    window.configure(background = "#a1dbcd")
    window.minsize(width=400, height=400) 
    window.wm_iconbitmap('son.ico')
    mainUI = TkinterUI(window)
    mainUI.defaultJson('')
    mainUI.defaultAddress('')
    mainUI.mainLoop()  

mainLoop()
