# coding:utf-8
# !/usr/bin/env python

__author__ = 'XingHua'

"""

"""

import http.server
import AjaxHandler

PORT = 8080


def AjaxHandlerCallbackFunc(path):
    content = b"None"
    contenttype = "text/plain"
    pathlist = path.split('?', 1)
    if (pathlist[0] == "/"):
        if (len(pathlist) == 1):
            f = open("test.html", "rb")
            content = f.read()
            contenttype = "text/html"
            f.close()
        else:
            args = pathlist[1].split('&')
            cmd = args[0].split('=')
            if cmd[0] == "cmd":
                params = {}
                if len(args) > 1:
                    for arg in args[1:]:
                        param = arg.split('=')
                        val = param[1]
                        try:
                            val = int(val)
                        except ValueError:
                            try:
                                val = float(val)
                            except ValueError:
                                pass
                        params[param[0]] = val
                content = DispatchCmd(cmd[1], params)
    elif (pathlist[0] == "/favicon.ico"):
        f = open("test.png", "rb")
        content = f.read()
        contenttype = "image/png"
        f.close()
    return (content, contenttype)


def DispatchCmd(cmd, args):
    return str({cmd: args}).encode()


if __name__ == "__main__":
    try:
        AjaxHandler.callback = AjaxHandlerCallbackFunc
        server = http.server.HTTPServer(("", PORT), AjaxHandler.AjaxHandler)
        print("HTTP server is starting at port " + repr(PORT) + '...')
        print("Press ^C to quit")
        server.serve_forever()
    except KeyboardInterrupt:
        print("^Shutting down server...")
        server.socket.close()