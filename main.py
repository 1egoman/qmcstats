# mc stats plugin
from base import *
from minecraft_query import MinecraftQuery
import os, json


class mc_parser(parser):


  def validate(self):
    with open(os.path.join(self.get_plugin_dir(__file__), "servers.json")) as f:
      self.servers = json.loads( f.read() )
    return "server" in self.query and len([1 for s in self.servers if s in self.query])


  def parse(self, parent):
    # get server
    s = [s for s in self.servers if s in self.query]
    if len(s):

      # make query
      query = MinecraftQuery(self.servers[ s[0] ]["host"], self.servers[ s[0] ]["port"])
      basic_status = query.get_status()

      self.resp["text"] = "%s out of %s players: %s" % (basic_status["numplayers"], basic_status["maxplayers"], ", ".join(basic_status["players"]))
      self.resp["status"] = STATUS_OK
    else:
      # Error!
      self.resp["status"] = STATUS_ERR

    # return
    self.resp["type"] = "mcstats"
    return self.resp