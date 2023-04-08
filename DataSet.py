import glob

fieldImageFile = glob.glob("data/0/*")

for idx, fieldFile in enumerate(fieldImageFile):
    field = fieldFile.split("\\")[-1]
    imageFile = glob.glob(fieldFile + "/*")

    print(f"{field} : {len(imageFile)}개")