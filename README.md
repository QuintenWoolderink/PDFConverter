U use the pdf converter by placing the .docx or .md file with no images in it in the root of the converer folder

then go to cmd or powershell and cd to the folder
then type the code:
python main.py example.docx --output example.pdf

the example.txt in the line of code needs to be changed to the name of the folder you want to be a pdf
example.docx can be .docx if it is a .docx file if it is a .md file you need to use example.md

you will need to install some things
- install python

go to cmd or powershell cd to the folder location and do a

- pip install python-docx
- pip install docx2txt
- pip install -r requirements.txt
