import codecs
import glob

import chardet
from tqdm import tqdm

TO_ENCODEING = "utf-8"
PATH = "./" + "*.txt"

def extentEncoding(encoding):
    encoding = encoding.lower()
    if encoding == "euc-kr":
        return "cp949"
    else:
        return encoding

def convert_encoding(file_path):
    with open(file_path, "rb") as f:
        r = f.read()
        findLength = max(len(r), 200)
        detect = chardet.detect(r[:findLength])
        encoding = extentEncoding(detect["encoding"])

        if detect["confidence"] <= 0.2:         return -1
        if encoding.lower() == TO_ENCODEING:    return 0

        try:    content = r.decode(encoding, errors="ignore")
        except: return -1
    
    with codecs.open(file_path, 'w', TO_ENCODEING) as file:
        file.write(content)
    
    return 0




if __name__ == "__main__":
    file_list = glob.glob(PATH)
    print("FOUND %d FILE(S)\n"%len(file_list))

    errorFile = []
    for filePath in tqdm(file_list):
        try:
            if convert_encoding(filePath) == -1:
                errorFile.append(filePath)
        except Exception as e:
            print(e)


    print("\nEncode Success. %d File Failed"%len(errorFile))
    for filePath in errorFile:
        print(filePath.split('/')[-1])