
from glob import glob
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
from AdharInfo_Extractor import AdharInfo_Extractor
from rich.progress import track
import pytesseract
import pandas as pd 

UPLOAD_DIR = Path () / "uploads"
app = FastAPI()
origins = ["*"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


def Aadhar_Extraction_Process():

    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

    DF = pd.DataFrame(columns=["Student Name","Adhar Number","DOB","Gender","Address"])
    list_front_img = [file for file in glob(f"{UPLOAD_DIR}/*") if ".1." not in file]
    list_back_img = [file for file in glob(f"{UPLOAD_DIR}/*") if ".1." in file]
    
    excel_file_path = os.getcwd()

    for i,front_img,back_img in zip(track(range(len(list_front_img)), description="Extraction Process..."),list_front_img,list_back_img):
        
        adhar_info_extractor = AdharInfo_Extractor(front_img,back_img)

        adhar_number = adhar_info_extractor.adhar_number
        adhar_name = adhar_info_extractor.adhar_name
        adhar_dob = adhar_info_extractor.adhar_dob
        adhar_gender = adhar_info_extractor.adhar_gender
        adhar_address = adhar_info_extractor.adhar_address

        details = [adhar_name, adhar_number, adhar_dob, adhar_gender, adhar_address]
        DF.loc[len(DF)+1] = details
        
        print(adhar_name)
        print(adhar_number)
        print(adhar_dob)
        print(adhar_gender)
        print(adhar_address)

        print("----------------------------------------------------")

    
    DF.to_excel(excel_file_path+"/StudentDetails.xlsx",index=False) 

@app.post("/uploadfile/")

async def root(file_upload:list[UploadFile]):
    if not os.path.exists(UPLOAD_DIR):
        os.mkdir(Path() / 'uploads')
            
    file_name = []
    for file in file_upload:
        # print(file)
        file_name.append(Path(file.filename).name)
        data = file.file.read()
        with open(UPLOAD_DIR / Path(file.filename).name,"wb") as f:
            f.write(data)

    if os.listdir(UPLOAD_DIR):
        Aadhar_Extraction_Process()

    fsdfgsr= os.getcwd()
    print(fsdfgsr)
    for f in glob(f'{UPLOAD_DIR}/*'):
        os.remove(f)

    return {"filenames":file_name}

    
