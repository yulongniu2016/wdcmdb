#coding:utf-8
#!/usr/bin/env python

import configparser as cf

def db_config():
  config = cf.RawConfigParser()
  config.read('main.conf')
  host = config.get("mysql","host")
  port = config.get("mysql","port")
  user = config.get("mysql","user")
  pw = config.get("mysql","password")
  name = config.get("mysql","name")

  db = {"host":host, "port":port, "user":user, "pw":pw, "name":name}
  #print("--->db: ",db)
  return db

if __name__=="__main__":
  dbinfo = config_read()
  print(dbinfo)

