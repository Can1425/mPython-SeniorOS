# FTReader - by LP_OVER
# Copyright (c) 2024 LP_OVER
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import gc
class GetLogo:
    def __init__(self,LogoLoc):
        self.LogoLoc = LogoLoc
        self.LogoSize = ""
    def Logo(self,LogoNum):
        LogoData = ""
        with open(self.LogoLoc) as f:
            f.seek(0)
            for i in range(LogoNum+1):
                LogoData = f.readline()
        LogoData = eval("[{}]".format(LogoData))
        gc.collect()
        return bytearray(LogoData)
    def LogoLength(self):
        if self.LogoSize != "":return self.LogoSize
        LogoLen = 0
        with open(self.LogoLoc) as f:
            f.seek(0)
            while f.readline() != "":
                LogoLen += 1
        self.LogoSize = LogoLen
        return LogoLen