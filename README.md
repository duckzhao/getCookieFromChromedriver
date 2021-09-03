# getCookieFromChromedriver
使用chrome driver手动保存网页cookie到本地，主要用于应对许多无法逆向cookie，但又频繁需要更换cookie的网站，如tb

为防止网站屏蔽chromedriver，getcookie文件中使用chrome远程调试开启一个真实的浏览器，然后用chromedriver接管

###os.system('"{}" --remote-debugging-port=9222'.format(path))

可能需要更换chromedriver版本和当前chrome匹配才可以！
chromedriver下载地址：http://npm.taobao.org/mirrors/chromedriver/

pyqt_chrome.py 使用 pyqt5 内嵌了一个chrome浏览器，用于可视化的保存cookie到本地，该文件打包后无需依赖本地电脑上的chrome环境