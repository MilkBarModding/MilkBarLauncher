import subprocess
from shutil import copy, rmtree, copytree
import os

# Make sure to have msbuild in your PATH

abovePath = "\\".join(os.getcwd().split("\\")[:-1])

WPFProject = r"WPF .NET 6\Breath of the Wild Multiplayer"
WPFBin = fr"{WPFProject}\bin\Release\net6.0-windows"
GUIAppProject = r"C#\BOTW.DedicatedServer"
DedicatedServerBin = r"C#\BOTW.DedicatedServer\bin\Release"

Output = f"Build"

def copyFile(src, dst):
    if ".pdb" in src:
        return
    if os.path.isdir(src):
        copytree(src, dst)
    else:
        copy(src, dst)
    print(f"Copied \t{src} into \n\t{dst}")

def copyFolder(src, dest, filters = []):
    if not os.path.exists(dest):
      os.mkdir(dest)  
    for file in os.listdir(src):
        anyFilter = False
        for filter in filters:
            if filter in file:
                anyFilter = True

        if anyFilter: continue

        copyFile(rf"{src}\{file}", rf"{dest}\{file}")

def BuildProject(projectFolder):
    subprocess.call(["dotnet", "clean", projectFolder])
    subprocess.call(["dotnet", "build", projectFolder, "/p:Configuration=Release"])

def BuildDLL():
    subprocess.call(["msbuild", r"DLL\InjectDLL\InjectDLL.sln", "/p:Configuration=Release"])

def ClearFolder(FolderToClear, filters = []):
    for file in os.listdir(FolderToClear):

        anyFilter = False
        for filter in filters:
            if filter in file:
                anyFilter = True

        if anyFilter: continue

        if os.path.isdir(fr"{FolderToClear}\{file}"):
            rmtree(fr"{FolderToClear}\{file}")
        else:
            os.remove(fr"{FolderToClear}\{file}")


def ClearFilesWithFilter(FolderToClear, filters = []):
    for file in os.listdir(FolderToClear):
        anyFilter = False
        for filter in filters:
            if filter in file:
                anyFilter = True

        if anyFilter:
            if os.path.isdir(fr"{FolderToClear}\{file}"):
                rmtree(fr"{FolderToClear}\{file}")
            else:
                os.remove(fr"{FolderToClear}\{file}")

            print(f"Cleared {FolderToClear}\{file}")
            return
        
        if os.path.isdir(fr"{FolderToClear}\{file}"):
            ClearFilesWithFilter(fr"{FolderToClear}\{file}", filters)

# ClearFolder(ReleaseFolder, ["git", "Resources"])

if(os.path.exists(Output)):
    ClearFolder(Output)

BuildProject(GUIAppProject)
BuildProject(WPFProject)

BuildDLL()

os.mkdir(f"{Output}\\BNPs")

for file in os.listdir(f"{os.getcwd()}/BNP Files"):
    if not ".bnp" in file: continue
    copyFile(f"{os.getcwd()}/BNP Files/{file}", f"{Output}\\BNPs\\{file}")

input("Press enter to continue")