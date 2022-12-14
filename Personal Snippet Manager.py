import os,datetime as dt
from tkinter import Tk,END,Text,Button,messagebox,Listbox,Label
from tkinter.ttk import Combobox
import pickle
from pyperclip import copy

os.chdir(os.getenv('USERPROFILE'))
if '.PSM' not in os.listdir():
    os.mkdir('.PSM')
os.chdir('.PSM')
main_dir=os.getcwd()

nw=dt.datetime.now().strftime('%Y-%m-%d_%H')
tmp=os.getenv('TEMP')
fb14=('Calibri',14,'bold')

def savepkl(*args):
    with open(tmp+f'\\snippet_files_{nw}.pkl','wb') as f:
        pickle.dump(jsm,f)
    with open('snippets.pkl','wb') as f:
        pickle.dump(jsm,f)

def save(*args):
    js.update({be.get():tb.get("1.0", "end-1c")})#add or replace current snippet
    upd()
    snips.update({apptype.get():js})
    jsm.update({'snips':snips})
    savepkl()
    messagebox.showinfo('_',f'Snippet Saved:\n{be.get()}')

def drop(*args):
    name=be.get()
    if name in js.keys():
        _=js.pop(name)
        snips.update({apptype.get():js})
        jsm.update({'snips':snips})
        be.set('')
        tb.delete("1.0","end-1c")
        savepkl()
        messagebox.showinfo('_',f'Snippet Deleted:\n{name}')
    return

def upd(*args):
    sl.delete(0,END)
    sn=be.get()
    ls=[i for i in js.keys() if i.lower().find(sn.lower())>-1]
    _=[sl.insert(END,i) for i in ls if i.lower()!=sn.lower()]
    be['values'] = ls
    get_code(sn)

def get_code(sn):
    v=js.get(sn)
    if v:
        tb.delete("1.0","end-1c")
        tb.insert(END,v)
        copy(v)

def updapp(*args):
    global js
    global jsm
    if apptype.get() in snips.keys():
        jsm.update({'env':apptype.get()})
        js=jsm['snips'].get(jsm['env'])
        be.set('')
        upd()
        savepkl()
        be.focus()

def sel_snip(*args):
    be.set(sl.get(sl.curselection()))
    get_code(be.get())
    be.focus()

def envnew(*args):
    app=apptype.get()
    if app not in snips.keys():
        snips.update({app:{}})
        jsm.update({'snips':snips})
        savepkl()
        apptype['values'] = list(snips.keys())
        tb.delete("1.0","end-1c")
        w=Tk()
        w.geometry('260x70+0+0')
        Label(w,text=f'-- {app} --\nCategory has been created',
            font=('Calibri',16,'bold')).place(x=10,y=10)

def envdel(*args):
    w=Tk()
    w.geometry('350x90+0+0')
    Label(w,text=f'Are you sure you want to drop {apptype.get()}?',
        font=fb14).place(x=5,y=5)
    def dsnip(*args):
        app=apptype.get()
        _=snips.pop(app)
        jsm.update({'snips':snips})
        w1=Tk()
        w1.geometry('260x70+0+0')
        Label(w1,text=f'-- {app} --\nCategory has been Deleted',
            font=('Calibri',16,'bold')).place(x=10,y=10)
        w.destroy()
        app=list(snips.keys())[0]
        jsm.update({'env':app})
        js=jsm['snips'][app]
        apptype['values'] = list(jsm['snips'].keys())
        apptype.set(app)
        be.set('')
        upd()
        savepkl()
        be.focus()
    Button(w,text='Yes',command=dsnip,font=fb14,bg='#35c521',borderwidth=5,width=7).place(x=50,y=35)
    Button(w,text='No',command=w.destroy,font=fb14,bg='#fa0a10',borderwidth=5,width=7).place(x=200,y=35)

def rec(*args):
    orig=os.getcwd()
    os.chdir(tmp)
    ls=[i for i in os.listdir() if i[:13]=='snippet_files']
    w=Tk()
    n=len(ls)
    mx=min(55+20*n,628)
    w.geometry(f'180x{mx}+0+0')
    w.maxsize(180,mx)
    w.minsize(180,mx)
    l=Label(w,text='Select File to restore to:')
    l.place(x=5,y=35)
    lb=Listbox(w,height=n)
    lb.place(x=5,y=55)
    lb.config(width=28)
    _=[lb.insert(END,i) for i in ls]
    def sel_file(*args):
        global jsm
        print('sel_file called')
        with open(lb.get(lb.curselection()),'rb') as f:
            jsm=pickle.load(f)
        os.chdir(orig)
        with open('snippets.pkl','wb') as f:
            pickle.dump(jsm,f)
        refresh()
        w.destroy()
    Button(w,text='Cancel',command=w.destroy,font=('Calibri',10,'bold'),
        bg='#fa0a10',borderwidth=5,width=18).place(x=20,y=5)
    lb.bind('<ButtonRelease>',sel_file)

def refresh(*args):
    snips=jsm['snips']
    js=snips[jsm['env']]
    apptype['values'] = list(snips.keys())
    be.set('')
    upd()
    be.focus()

def helpgui(*args):
    wh=Tk()
    wh.title('Personal Snippet Manager-Help')
    wh.geometry('470x400+0+0')
    wh.maxsize(470,400)
    wh.minsize(470,400)
    Label(wh,text='How to use this Snippet Manager:',font=('Calibri',14,'italic'),fg='#299c3e').place(x=10,y=10)
    Label(wh,text='Select Category if necessary',font=('Calibri',14)).place(x=10,y=40)
    Label(wh,text="a) Add a new category by typing a name and clicking 'Enter'",font=('Calibri',12)).place(x=40,y=65)
    Label(wh,text="b) Delete a category by holding 'Cntl'+clicking with mouse",font=('Calibri',12)).place(x=40,y=90)
    Label(wh,text='To add a snippet:',font=('Calibri',14)).place(x=10,y=120)
    Label(wh,text='1) type name of snippet',font=('Calibri',12)).place(x=40,y=145)
    Label(wh,text='2) paste code into main box',font=('Calibri',12)).place(x=40,y=170)
    Label(wh,text='3) click Commit button',font=('Calibri',12)).place(x=40,y=195)
    Label(wh,text='To retrieve a snippet',font=('Calibri',14)).place(x=10,y=225)
    Label(wh,text='-start typing the name',font=('Calibri',12)).place(x=40,y=250)
    Label(wh,text='---or---',font=('Calibri',12)).place(x=80,y=290)
    Label(wh,text='-scroll and select desired snippet-',font=('Calibri',12)).place(x=40,y=275)
    Label(wh,text='-click desired snippet displayed',font=('Calibri',12)).place(x=40,y=310)
    Label(wh,text='This will automatically copy to your clipboard\nno need to select and copy display',
        font=('Calibri',14,'italic'),fg='#523fad').place(x=40,y=340)
    return


def jsmnew(*args):
    return {'env': 'python',
 'snips': {'generic': {'data generate': 'www.generatedata.com'},
           'python': {'aes encryption': 'from pyAesCrypt import encryptFile\n'
                                        "encrypt('pwd.txt','set.aes','CM',65536)\n"
                                        '\n'
                                        'from pyAesCrypt import decryptFile\n'
                                        "decryptFile('set.aes','_.txt','CM',65536)\n"
                                        "with open('_.txt','r') as f:\n"
                                        '\thp=r.read()\n'
                                        '\n'
                                        "os.remove('_.txt')",
                      'app maker': '#Exe maker\n'
                                   'import os\n'
                                   'from tkinter import Tk\n'
                                   'from tkinter.filedialog import '
                                   'askdirectory\n'
                                   '\n'
                                   'rt=Tk()\n'
                                   'rt.diretory()=askdirectory()\n'
                                   'rt.destroy()\n'
                                   'os.chdir(rt.directory)\n'
                                   "os.system('auto-py-to-exe')",
                      'business day shifter': 'import datetime as dt\n'
                                              'from pandas.tseries.holiday '
                                              'import USFederalHolidayCalendar '
                                              'as fhd\n'
                                              'td=dt.datetime.now().date()\n'
                                              'fh=fhd().holidays(start=td-dt.timedelta(days=5),end=td+dt.timedelta(5))\n'
                                              'def bus_day(d):#takes date and '
                                              'moves forward until next '
                                              'business day\n'
                                              '\tfor i in range(3):\n'
                                              '\t\tif d.weekday()>4 or d in '
                                              'fh:\n'
                                              '\t\t\td=d+dt.timedelta(1)\n'
                                              '\treturn d\n',
                      'calendar': 'import datetime as dt\n'
                                  'from tkinter import *\n'
                                  'from tkcalendar import Calendar\n'
                                  'wd=Tk()\n'
                                  'st=dt.datetime.now().date()\n'
                                  "l=Label(wd,text=st,font=('Calibri',12,'bold'),fg='#b41f1f')\n"
                                  'l.place(x=5,y=5)\n'
                                  'def cf(*args):\n'
                                  '\tw=Tk()\n'
                                  '\t'
                                  'cal=Calendar(w,selectmode="day",year=st.year,month=st.month,day=st.day,date_pattern=\'Y-m-d\')\n'
                                  '\tcal.pack()\n'
                                  '\tdef getdt(*args);\n'
                                  '\t\tglobal mn\n'
                                  '\t\tmn=cal.get_date()\n'
                                  '\t\tw.destroy()\n'
                                  '\t\tl.config(text=mn)\n'
                                  '\t\treturn\n'
                                  '\tcal.bind(<<CalendarSelected>>,getdt)\n'
                                  "l.bind('<ButtonPress>',cf)",
                      'df html': 'import os\n'
                                 "os.chdir(os.getenv('TEMP'))\n"
                                 "html=df.to_html(na_rep='', "
                                 "index=False,justify='center',border=True)\n"
                                 "html=html.replace('<th>','<th "
                                 'style="background-color:#ecbd4e;font-size:150%;">\')\n'
                                 "html=html.replace('<td>','<td "
                                 'style="background-color:#0095e6;color:blue;font-size:120%;text-align:center;">\')\n' 
                                 "with open('sample.html','w') as f:\n"
                                 '    f.write(html)\n'
                                 '\n'
                                 "os.startfile('sample.html')",
                      'file select': 'from tkinter.filedialog import '
                                     'askopenfile\n'
                                     "file=askopenfile(mode='r',filetypes=[('XLSX "
                                     "files','*.xlsx')]).name\n"
                                     'print(file)',
                      'format sample': "df.col.apply('{:,.1f}%'.format)\n"
                                       "'${0:.0f}'.format(2489.023)",
                      'logging': '#no log file created if no error\n'
                                 'import os,logging\n'
                                 'from io import StringIO()\n'
                                 'logging.basicConfig(stream=logstream,level=logging.INFO)\n'
                                 "logfile='name.log'\n"
                                 '\n'
                                 'try:\n'
                                 "\tlogging.error('Purposeful Error')\n"
                                 '\treturn\n'
                                 'except Exception as e:\n'
                                 '\tlogging.error(e)\n'
                                 "\twith open(logfile,'w') as f:\n"
                                 '\t\tf.write(logstream.getvalue())\n'
                                 '\tos.startfile(logfile)',
                      'random df': 'import pandas as pd, numpy as np\n'
                                   "hl=('Spiderman','Batman')\n"
                                   "dates=list(pd.date_range(start='2022-1-1',end='2022-1-05',freq='D'))\n"
                                   'nd=len(dates)\n'
                                   "df=pd.DataFrame({'col':np.repeat(hl,nd),'Date':dates*2})\n"
                                   "df['Villians']=np.random.randint(0,100,2*nd)\n"
                                   "df['Power']=df['Villians']*.5+np.random.randint(0,20,2*nd)\n",
                      'regexpress df': "df.Column.str.contains('(?:dog)|(?:cat)',case=False,regex=True)",
                      'regular expression': 'from re import search\n'
                                            "search(^r'[a-zA-Z]{2}[w]{1}\\d{t}','abc0003443z4')\n"
                                            '#https://regex101.com',
                      'simple linreg': 'import numpy as np\n'
                                       'x=[3,7,8,10,2]\n'
                                       'y=np.matrix([1,2,5,8,4]).T\n'
                                       'X=np.matrix([x,np.repeat(1,len(x))]).T\n'
                                       'B=(X.T*X).I*X.T*y',
                      'today': 'import datetime as dt\n'
                               'td=dt.datetime.now().date()'},
           'snowflake': {'create database': 'CREATE DATABASE <database>;\n'
                                            '\n'
                                            'CREATE TABLE <table> (\n'
                                            '\tid string,\n'
                                            '\tname string,\n'
                                            '\tdate DATE\n'
                                            '\t);',
                         'grant access': 'GRANT USAGE ON DATABASE <dbname> TO '
                                         'ROLE PUBLIC;\n'
                                         'GRANT USAGE ON SCHEMA '
                                         '<schema>.<dbname> TO ROLE PUBLIC;\n'
                                         'GRANT SELECT ON TABLE '
                                         '<schema>.<dbname> TO ROLE PUBLIC;\n'
                                         '\n'
                                         'CREATE WAREHOUSE <wh name> WITH '
                                         "WAREHOUSE.SIZE='SMALL' "
                                         "WAREHOUSE_TYPE='STANDARD' "
                                         'AUTO_SUSPEND=300 AUTO_RESUME=TRUE;\n'
                                         '\n'
                                         'CREATE ROLE <role>;\n'
                                         'GRANT USAGE ON WAREHOUSE <wh name> '
                                         'to ROLE <role>;\n'
                                         '\n'
                                         '--create a ligin for users\n'
                                         "CREATE USER <user1> PASSWORD='<pwd>' "
                                         'LOGIN_NAME=<user1> '
                                         'DEFAULT_ROLE=<role> '
                                         'DEFAULT_WAREHOUSE=<wh name> '
                                         'MUST_CHANGE_PASSWORD=FALSE;\n'
                                         '\n'
                                         'GRANT ROLE <role> TO USER <user1> ',
                         'multi-cluster': 'CREATE WAREHOUSE <wh name>\n'
                                          "WITH WAREHOUSE_SIZE='XSMALL'\n"
                                          'MIN_CLUSTER_COUNT=1\n'
                                          'MAX_CLUSTER_COUNT=1\n'
                                          "SCALING_POLICY='STANDARD'\n"
                                          'AUTO_SUSPEND=300\n'
                                          'AUTO_RESUME=TRUE;',
                         'pipe setup': '--test first\n'
                                       'COPY INTO <table> FROM @<stage table>\n'
                                       'file_format(type=csv field '
                                       "delimiter='|' skip_header=1);\n"
                                       '\n'
                                       'CREATE OR REPLACE PIPE <pipename>\n'
                                       'auto_ingest=true\n'
                                       'AS COPY INTO <table> FROM @<stage '
                                       'table>\n'
                                       'file_format(type=csv field '
                                       "delimiter='|' skip_header=1);",
                         'stage json': 'USE DATABASE <dbname>\n'
                                       '\n'
                                       'CREATE TABLE <stage table raw> (\n'
                                       '\tjraw VARIANT\t\n'
                                       '\t);\n'
                                       '\n'
                                       '--S3 portion would need login info to\n'
                                       'CREATE or REPLACE stage <json stage> '
                                       "url='S3://bucketpath'\n"
                                       '\n'
                                       'copy into <stage table raw>\n'
                                       '\tfrom @<json stage>/<name.json>\n'
                                       '\tfile_format=(type=json);\n'
                                       '\n'
                                       '--one item deep values  Creates '
                                       'variables to reference\n'
                                       'select col1:key1_set,\n'
                                       '\tcol2:key2_date\n'
                                       'from <stage table raw>;\n'
                                       '\n'
                                       '--use flatten table function to '
                                       'convert JSON data into column\n'
                                       '--applies to array data\n'
                                       'Select value:key1::String,\n'
                                       '\tvalue:key2::String,\n'
                                       '\tjraw:key2_date\n'
                                       'from <stage table raw>\n'
                                       '\t. lateral flatten (input => '
                                       'jraw:<key of arrat> );',
                         'stage sample': '--S3 portion would need login info '
                                         'to\n'
                                         'CREATE or REPLACE stage '
                                         'bulk_copy_example '
                                         "url='S3://bucketpath'\n"
                                         '\n'
                                         '--list files in bucket\n'
                                         'list @bulk_copy_example\n'
                                         '\n'
                                         'USE DATABASE <dbname>\n'
                                         '\n'
                                         'copy into <table>\n'
                                         '\tfrom @bulk_copy_example\n'
                                         "\tpattern='*.csv'\n"
                                         '\tfile_format=(type=csv '
                                         "field_delimiter='|' skip_header=1);",
                         'timetravel': 'AT(offset => -60);\n'
                                       "before(timestamp => '2022-12-04 "
                                       "07:00:00.001' :: timestamp);\n"
                                       "before(statement =>'id of query ie. "
                                       "018c6f1f-00fd-.........');",
                         'timetravel sample': 'select * from <table> AT(offset '
                                              '=> -60)',
                         'zero copy clone': 'create table <table_clone> clone '
                                            '<table>\n'
                                            'create schema <schema_clone> '
                                            'clone <schema>'}}}

def main():
    global jsm
    global js
    global snips
    global sl
    global be
    global apptype
    global tb
    if 'snippets.pkl' in os.listdir():
        with open('snippets.pkl','rb') as f:
            jsm=pickle.load(f)
    else:
        jsm=jsmnew()
    ## Section developed to migrated and not erase current snippets
    if 'snippet_files.pkl' in os.listdir():
        with open('snippet_files.pkl','rb') as f:
            sf=pickle.load(f)
        for k in sf['snips'].keys():
            if k in jsm['snips'].keys():
                for s in sf['snips'][k]:
                    jsm['snips'][k].update({s:sf['snips'][k][s]})
            else:
                jsm['snips'].update({k:sf['snips'][k]})
        os.system(f'move "{main_dir}\\snippet_files.pkl" {tmp}')
    snips=jsm['snips']
    js=snips[jsm['env']]
    wd=Tk()
    wd.title('Personal Snippet Manager')
    wd.geometry('790x628+0+0')
    wd.maxsize(790,628)
    wd.minsize(790,628)
    apptype=Combobox(wd,font=('Calibri',16,'bold'),background='#31c0df',\
        justify='center',postcommand=updapp,width=14,xscrollcommand=updapp)
    apptype['values'] = list(jsm['snips'].keys())
    apptype.place(x=10,y=5)
    apptype.set(jsm['env'])
    apptype.bind('<KeyRelease>',updapp)
    Button(wd,text='Commit',command=save,font=fb14,bg='#35c521',borderwidth=5,width=7)\
        .place(x=5,y=40)
    Button(wd,text='Drop',command=drop,font=fb14,bg='#fa0a10',borderwidth=5,width=7)\
        .place(x=100,y=40)
    Button(wd,text='Recover Past Snippets',command=rec,font=('Calibri',12,'italic'),
        bg='#0000a0',fg='#ffffff',borderwidth=5,width=20,height=1,pady=0).place(x=10,y=580)
    be=Combobox(wd,font=fb14,width=16)
    be['values'] = list(js.keys())
    be.place(x=5,y=90)
    sl=Listbox(wd,font=('Calibri',14),height=19,width=18,fg='#8080c0')
    sl.place(x=5,y=115)
    tb=Text(wd,font=('Courier New',10,'bold'),height=38,width=72,tabs=20\
        ,undo=20,maxundo=20,wrap='none')
    tb.place(x=200,y=5)
    bt=Button(tb,text='?',command=helpgui,font=('Calibri',18,'bold','italic'),bg='#0b539b',fg='white')
    bt.place(x=530,y=5)
    bt.config(width=3,font=('Calibri',14,'bold'))
    upd()
    be.bind('<KeyRelease>',upd)
    be.config(xscrollcommand=upd)
    sl.bind('<ButtonRelease>',sel_snip)
    apptype.bind('<Return>',envnew)
    apptype.bind('<Control-Button-1>',envdel)
    wd.mainloop()
    return

if __name__=='__main__':
    main()

