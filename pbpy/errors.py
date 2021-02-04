"""
The MIT License (MIT)
Copyright (c) 2021 Giuseppe 'Polliog' Pollio
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

class PBexception(Exception):
    pass


class HTTPException(PBexception):
    def __init__(self, response, message):
        self.response = response
        if isinstance(message, dict):
            self.text = message.get('message', '')
            self.code = message.get('code', 0)
        else:
            self.text = message

        fmt = f"{self.response.reason} (status code: {self.response.status})"
        if self.text:
            fmt = f"{fmt}: {self.text}"

        super().__init__(fmt)

class invalidToken(PBexception):
    def __init__(self, response):
        print(response)
