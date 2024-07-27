import fitz;
import sys;
import json;
from cn_bing_translator import Translator;


translator = Translator(fromLang='en', toLang='zh-Hans')


filename=sys.argv[1];
doc=fitz.open(filename);
res=fitz.open();

with open("dictionary/functions.json","r") as file:
    funcnames=file.read();

funcnames=json.loads(s=funcnames);

print("Translating the PDF. ")

def CountEnglish(txt) : 
    for fname in funcnames["names"] :
        txt=txt.replace(fname,"");
    ans=0;
    for achar in txt :
        if (achar>="a") & (achar<="z") | (achar>="A") & (achar<="Z") :
            ans=ans+1;
    return ans;
def CheckFormular(txt): 
    if CountEnglish(txt)<=3 :
        return True;
    else :
        return False;
    return False;
def main():
    for pageid in range(doc.page_count) :
        page=doc.load_page(pageid);
        texts=page.get_textpage();
        Ctxt=texts.extractDICT(sort=True);

        print("Page "+str(pageid+1)+" translating...")
        with open("tmp\\page"+str(pageid+1)+".json","w",encoding="utf-8") as f:
            f.write(json.dumps(Ctxt));
        
        # Main

        ToTranslate=[""];
        for block in Ctxt["blocks"] : 
            for line in block["lines"] :
                for span in line["spans"] :
                    if CheckFormular(span["text"]) :
                        continue;
                    if len(ToTranslate[len(ToTranslate)-1])+1+len(span["text"])>1500 :
                        ToTranslate.append("");
                    ToTranslate[len(ToTranslate)-1]=ToTranslate[len(ToTranslate)-1]+span["text"]+'\n';
        
        for id in range(len(ToTranslate)):
            result=translator.process(ToTranslate[id]);
            ToTranslate[id]=result;
            print(ToTranslate[id]);
        
        for id in range(len(ToTranslate)):
            ToTranslate[id]=ToTranslate[id].split("\n");
            ToTranslate[id].pop();
            print(ToTranslate[id]);

        cnt=0;
        cur=0;
        for block in Ctxt["blocks"] : 
            for line in block["lines"] :
                for span in line["spans"] :
                    if CheckFormular(span["text"]) :
                        continue;
                    print(cnt,cur);
                    ans=ToTranslate[cur][cnt];
                    cnt=cnt+1;
                    if cnt>=len(ToTranslate[cur]):
                        cur=cur+1;
                        cnt=0;
                    page.add_redact_annot(quad=span["bbox"],text=ans,fontname="china-ss",fontsize=span["size"],fill=None,text_color=(0,0,0),cross_out=False);
                    page.apply_redactions();
                    # add_redact_annot(quad, text=None, fontname=None, fontsize=11, align=TEXT_ALIGN_LEFT, fill=(1, 1, 1), text_color=(0, 0, 0), cross_out=True)


        print("Page "+str(pageid+1)+" done.")

        with open("tmp\\page_translated"+str(pageid+1)+".json","w",encoding="utf-8") as f:
            f.write(json.dumps(page.get_textpage().extractDICT(sort=True)));
        
        doc.save(filename+".translated.pdf");

    
main();

