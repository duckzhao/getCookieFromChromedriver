import sys
from PyQt5.QtWidgets import QTabWidget, QToolBar, QLineEdit, QWidget, QHBoxLayout, QApplication, QMainWindow, QMessageBox, QInputDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings


# 创建主窗口
class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('自制浏览器')
        # 设置窗口大小900*600
        self.resize(1300, 700)
        self.show()

        # 剪切板
        self.clipboard = app.clipboard()

        # 加载配置文件中的默认url
        with open('./启动地址.txt', mode='r', encoding='utf-8') as f:
            url = f.read()
            print(url)
            # exit()

        # 创建tabwidget（多标签页面）
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_Tab)
        self.setCentralWidget(self.tabWidget)

        # 第一个tab页面
        self.webview = WebEngineView(self)  # self必须要有，是将主窗口作为参数，传给浏览器
        # 禁止缓存cookie等东西到本地
        self.webview.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, False)
        self.webview.load(QUrl(url))
        self.create_tab(self.webview)

        # 使用QToolBar创建导航栏，并使用QAction创建按钮
        # 添加导航栏
        navigation_bar = QToolBar('Navigation')

        # navigation_bar.setBaseSize(10, 10)

        # 添加导航栏到窗口中
        self.addToolBar(navigation_bar)

        # 添加复制cookie按钮,以及基本网页事件按钮
        self.back_button = navigation_bar.addAction('后退')
        self.next_button = navigation_bar.addAction('前进')
        self.stop_button = navigation_bar.addAction('停止')
        self.reload_button = navigation_bar.addAction('刷新')
        self.copy_ck_button = navigation_bar.addAction('复制CK')

        # 导航栏按钮绑定事件
        self.back_button.triggered.connect(self.webview.back)
        self.next_button.triggered.connect(self.webview.forward)
        self.stop_button.triggered.connect(self.webview.stop)
        self.reload_button.triggered.connect(self.webview.reload)
        self.copy_ck_button.triggered.connect(self.copy_ck)

        # 添加URL地址栏
        self.urlbar = QLineEdit()
        # 让地址栏能响应回车按键信号
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        # 让浏览器相应url地址的变化
        self.webview.urlChanged.connect(self.renew_urlbar)

    # 显示地址
    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('https')
        self.webview.setUrl(q)

    # 响应输入的地址
    def renew_urlbar(self, q):
        # 将当前网页的链接更新到地址栏
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    # 创建tab页面
    def create_tab(self, webview):
        self.tab = QWidget()
        self.tabWidget.addTab(self.tab, "新建页面")
        self.tabWidget.setCurrentWidget(self.tab)

        # 渲染到页面
        self.Layout = QHBoxLayout(self.tab)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Layout.addWidget(webview)

    # 关闭tab页面
    def close_Tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
        else:
            self.close()  # 当只有1个tab时，关闭主窗口

    # 复制cookie
    def copy_ck(self):
        cookie = self.webview.get_cookie()
        self.clipboard.setText(cookie)
        print('cookie 已经复制', cookie)
        QMessageBox.about(self, '提示', 'cookie复制成功！')

# 创建浏览器，重写重写createwindow方法实现页面连接的点击跳转
class WebEngineView(QWebEngineView):
    def __init__(self, mainwindow, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow
        # 清除所有历史记录，防止cookie覆盖
        # QWebEngineProfile.clearHttpCache()
        QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies()
        # 绑定cookie被添加的信号槽
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}  # 存放cookie字典

    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.mainwindow)
        self.mainwindow.create_tab(new_webview)
        return new_webview

    def onCookieAdd(self, cookie):  # 处理cookie添加的事件
        name = cookie.name().data().decode('utf-8')  # 先获取cookie的名字，再把编码处理一下
        value = cookie.value().data().decode('utf-8')  # 先获取cookie值，再把编码处理一下
        print(f'捕获cookie  {name}, {value}')
        self.cookies[name] = value  # 将cookie保存到字典里

    # 获取cookie
    def get_cookie(self):
        # 暂时不需要document.cookie
        # self.__getCookieRunJs()
        # 按照淘宝确认能够发送出消息的cookie字段 和 排列顺序 来
        cookie_kay_list = ['_samesite_flag_', 'cookie2', 't', '_tb_token_', 'cna', 'xlly_s', 'sgcookie', 'unb', 'uc3',
                           'csg', 'lgc', 'cookie17', 'dnk', 'skt', 'existShop', 'uc4', 'tracknick', '_cc_', '_l_g_',
                           'sg', '_nk_', 'cookie1', 'mt', 'uc1', 'thw', 'isg', 'l', 'tfstk']
        cookie_str = ''
        for temp_cookie in cookie_kay_list:
            # 如果目标字段在缓存的cookie中
            if temp_cookie in self.cookies.keys():
                value = self.cookies[temp_cookie]
                cookie_str += (temp_cookie + '=' + value + ';' + ' ')  # 将键值对拿出来拼接一下
                print('成功定位到 {} 字段'.format(temp_cookie))
            else:
                print('缺失 {} 字段'.format(temp_cookie))
        cookie_str = cookie_str[: -2]

        # cookie_str = ''
        # for key, value in self.cookies.items():  # 遍历字典
        #     cookie_str += (key + '=' + value + ';' + ' ')  # 将键值对拿出来拼接一下
        # cookie_str = cookie_str[: -2]
        return cookie_str  # 返回拼接好的字符串

    # 使用document方式获取cookie
    def __getCookieRunJs(self):
        runJs = '''
        function getCookie(){return document.cookie}
        getCookie();
        '''
        self.page().runJavaScript(runJs, self.__getCookieByJs)
        # self.mainwindow.page().runJavaScript(runJs, self.__getCookieByJs)

    def __getCookieByJs(self, result):
        print(result)  # 打印这个的这个result就是cookie了

# 程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 创建主窗口
    browser = MainWindow(app)
    browser.show()
    # 运行应用，并监听事件
    sys.exit(app.exec_())
