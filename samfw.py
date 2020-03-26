import subprocess
import sys
import tarfile
import zipfile
from os import listdir, path, remove
from os.path import isfile, join

main_folder = path.realpath(path.dirname(__file__))
content = path.join(main_folder, "content")


def GetTheZip(mypath):
    """
    Get the zip files in the Original Folder. 
    Parameters: 
    Folder / Location
    Returns: 
    List: Files in the folder as in list 
    TODO : filter the files . 
    """
    ReturningFilesAsList = [f for f in listdir(
        mypath) if isfile(join(mypath, f))]
    return ReturningFilesAsList


if __name__ == '__main__':

    ZipfilesinContentFolder = GetTheZip(content)
    for eachZipFile in ZipfilesinContentFolder:
        if eachZipFile.endswith(".zip"):
            print(eachZipFile)
            zip = zipfile.ZipFile(path.join(content, eachZipFile))
            ZipNameList = zip.namelist()
            for eachFileInsideZip in ZipNameList:
                if eachFileInsideZip.startswith("AP_"):
                    # zip file
                    with zipfile.ZipFile(path.join(content, eachZipFile)) as myzip:
                        # tar file -> out
                        print(eachFileInsideZip)
                        myzip.extract(eachFileInsideZip, path=content)
                        if path.exists(path.join(content, eachZipFile)):
                            tar = tarfile.open(
                                path.join(content, eachFileInsideZip))
                            TarContent = tar.getnames()
                            for SingleIteminTarPackage in TarContent:
                                if SingleIteminTarPackage.startswith("boot") and SingleIteminTarPackage.endswith("lz4"):
                                    # SingleIteminTarPackage is - > boot lz4
                                    print(SingleIteminTarPackage)
                                    tar.extract(
                                        SingleIteminTarPackage, content)
                                    tar.close()  # we are done extracting
                                    # -> Remove Tar
                                    remove(
                                        path.join(content, eachFileInsideZip))
                                    # work on boot
                                    lz4Exe = path.join(main_folder, "lz4.exe")
                                    subprocess.check_call(
                                        [lz4Exe, "-d", path.join(content, SingleIteminTarPackage), path.join(content, "boot.img")])
                                    print("we are done")
                                else:
                                    # This is not LZ4 file.
                                    pass
                        else:
                            # Dosya nereye gitti ?
                            pass
                else:
                    # This is not AP File.
                    pass
        else:
            # This is not Zip File.
            pass
