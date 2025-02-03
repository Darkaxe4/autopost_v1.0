from general.utils import singletone
from general.config_parser import parser
import os
#-------------------------------#vk_requests#------------------------------------------#


import vk_api, random

class vk_requester(singletone):
    def __init__(self, path = "config.ini"):
        super().__init__()
        if not self.initialized:
            self.loadconfig(path)
            self.VK = vk_api.VkApi(token= self.auth_token, captcha_handler= self.captcha_handler)
            self.initialized = True
        return

    def loadconfig(self, path = "config.ini"):
        if not os.path.exists(path):
            raise ValueError
        parser.instance.parsefile(path)
        for name, value in parser.instance.getSection("VK"):
            self.__setattr__(name, value)
        self.messagesForRandomPost = []
        for message, text in parser.instance.getSection("messages"):
            self.messagesForRandomPost.append(text)

    def setArgs(self, args):
        if not(args.community_id is None):
            self.community_id = args.community_id
        if not(args.auth_token is None):
            self.auth_token = args.auth_token

    def captcha_handler(self, captcha):
        key = input("Enter captcha code {0}: ".format(captcha.get_rl())).strip()
        return captcha.try_again(key)
    
    def WallClear(self):	
        while True:
            response = self.VK.method("wall.get", {"owner_id":self.community_id, "filter":'postponed'})
            items = response["items"]
            if (response["count"]==0):
                break
            for item in items:
                self.VK.method("wall.delete", {"owner_id":item["owner_id"], "post_id":item["id"]})

    def WallFilteredClear(self, TargetString):
        while True:
            response = self.VK.method("wall.get", {"owner_id":self.community_id, "filter":'postponed'})
            items = response["items"]
            strings=set()
            for item in items:
                if not(item["text"] in strings):
                    strings.add(item["text"])
            if (response["count"]==0)or not(TargetString in strings):
                break
            for item in items:
                if(item["text"]==TargetString):
                    self.VK.method("wall.delete", {"owner_id":item["owner_id"], "post_id":item["id"]})

    def post(self, message = 'Set message here'):
        response = self.VK.method("wall.post", {"owner_id": self.community_id, "message":message})
        return response

    def postRandom(self):
        msg = random.choice(self.messagesForRandomPost)
        response = self.VK.method("wall.post", {"owner_id": self.community_id, "message":msg})
        return response
    
    def delayedPost(self, date, message):
        targetDate = date.timestamp()
        try:
            response = self.VK.method("wall.post", {"owner_id": self.community_id, "message":message, "publish_date":targetDate})
        except:
            raise RuntimeError('caused exception adding delayed post at ' + str(date) + '. Content:%s \n'%message)
        else:
            return response
        
    def delayedPostRandom(self, date):
        targetDate = date.timestamp()
        msg = random.choise(self.messagesForRandomPost)
        try:
            response = self.VK.method("wall.post", {"owner_id": self.community_id, "message":msg, "publish_date":targetDate})
        except:
            raise RuntimeError('caused exception adding delayed post at ' + str(date) + '. Content:%s \n'%msg)
        else:
            return response
