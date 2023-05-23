import os,pathlib,sys,datetime,time,pandas


__author__ = "Derek Whang"
__version__ = "1.0"
__maintainer__ = "Derek Whang"
__email__ = "dezz.whang@gmail.com"

def get_files(directory,filter_file,file_ext):
    try:
        file_list = []
        for it in os.scandir(directory):
            if it.is_dir():
                file_list.extend(get_files(it.path,filter_file,file_ext))
            if it.is_file():
                file_mtime = datetime.datetime.fromtimestamp(it.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                file_ctime = datetime.datetime.fromtimestamp(it.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                file_stat = it.stat()
                file_data = [it.name,it.path,file_stat.st_size,file_mtime,file_ctime]
                if filter and file_ext:
                    if filter_file.lower() in it.name.lower() and it.name.lower().endswith(file_ext.lower()):
                        file_list.append(file_data)
                elif filter_file:
                    if filter_file.lower() in it.name.lower():
                        file_list.append(file_data)
                elif file_ext:
                    if it.name.lower().endswith(file_ext.lower()):
                        file_list.append(file_data)
                else:
                    file_list.append(file_data)

    except Exception as e:
        print("issue with get_files")
        print(e)
        return False

    return file_list

if __name__ == "__main__":
    script_path = "\\\\?\\"+os.path.realpath(__file__)
    script_name = script_path.split("\\")[-1]
    start_time = time.time()
    print(f"{script_name} is now running!")
    target_dir = input("Search directory: ")
    target_dir = pathlib.Path("\\\\?\\"+target_dir).absolute()

    if str(target_dir).lower() == "q" or str(target_dir).lower() == "quit":
        print("Quitting script")
        sys.exit()

    filter_file = input("Filter filename: ")
    if filter_file.lower() == "q" or filter_file.lower() == "quit":
        print("Quitting script")
        sys.exit()

    file_ext = input("File extension: ")
    if file_ext.lower() == "q" or file_ext.lower() == "quit":
        print("Quitting script")
        sys.exit()

    file_list = get_files(target_dir,filter_file,file_ext)

    if not file_list:
        print("No files found")
        sys.exit()

    df = pandas.DataFrame(file_list)
    df.to_csv(script_path.replace(script_name,"output.csv"),index=False,header=["filename","filepath","file_size","file_modified","file_created"])

    end_time = time.time()
    print(f"Runtime: {round(end_time-start_time,2)}s")
    print(f"{script_name} is now ending!")
    sys.exit()
