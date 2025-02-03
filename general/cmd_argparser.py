from general.utils import singletone
#-------------------------#argparse#---------------------------------------------------#

import argparse

class argparser(singletone):
    def __init__(self):
        super().__init__()
        if not self.initialized:
            self.parser = argparse.ArgumentParser(prog = "VK autoposting py-script", 
                                                  description= "You can read readme.md", epilog= "darkaxe4@protonmail.com,\t 2023")
            self.defineArgs()
            self.initialized = True
        return
    
    def defineArgs(self):
        self.vk_prefs = self.parser.add_argument_group('VK_prefs', 'VK authorization data')
        self.vk_prefs.add_argument('--community_id', type = int)
        self.vk_prefs.add_argument('--auth_token')

        self.smtp_prefs = self.parser.add_argument_group('SMTP_prefs', 'SMTP authorization and e-mail prefs')
        self.smtp_prefs.add_argument('--host', help = 'host address')
        self.smtp_prefs.add_argument('--to_addr', action = 'append', 
                                     help = 'Adds an e-mail address for message sending (can be specified multiple times)')
        self.smtp_prefs.add_argument('--from_addr', help = 'Specifies an e-mail address to mail-from')
        self.smtp_prefs.add_argument('--login', help = 'SMTP login')
        self.smtp_prefs.add_argument('--password', help = 'SMTP password')
	
        self.parser.add_argument('--post_config_file', help = 'Path to file with posting configuration')

        self.log_settings = self.parser.add_argument_group('Logging preferences')
        self.log_settings.add_argument('--enablelogging', action = 'store_true', 
                                       help = 'You can not switch off the logging if it is enabled in cofig, but otherwise can switch on')
        self.log_settings.add_argument('--livelog', action = 'store_true', help = 'Same with enableLogging')
        self.log_settings.add_argument('--log_path', help = 'Path to folder, where will be saved logs example:\tC:/Logs/\tor\tLogs/ ')

    def parse(self):
        return self.parser.parse_args()