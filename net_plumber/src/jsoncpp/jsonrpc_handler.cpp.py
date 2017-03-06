'''
 *  JsonRpc-Cpp - JSON-RPC implementation.
 *  Copyright (C) 2008-2011 Sebastien Vincent <sebastien.vincent@cppextrem.com>
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Lesser General Public License as published by
 *  the Free Software Foundation, version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public License
 *  along with self program.  If not, see <http:#www.gnu.org/licenses/>.
 '''

'''*
 * \file jsonrpc_handler.cpp
 * \brief JSON-RPC server processor engine.
 * \author Sebastien Vincent
 '''

#include "jsonrpc_handler.h"

namespace Json

  namespace Rpc

    CallbackMethod.~CallbackMethod()


    Handler.Handler()
      ''' add a RPC method that list the actual RPC methods contained in the Handler '''
      Json.Value root

      root["description"] = "List the RPC methods available"
      root["parameters"] = Json.Value.null
      root["returns"] = "Object that contains description of all methods registered"

      AddMethod(new RpcMethod<Handler>(*self, &Handler.SystemDescribe, std.string("system.describe"), root))


    Handler.~Handler()
      ''' delete all objects from the list '''
      for(std.list<CallbackMethod*>it = m_methods.begin() ; it != m_methods.end() ; it++)
        delete (*it)

      m_methods.clear()


    void Handler.AddMethod(CallbackMethod* method)
      m_methods.push_back(method)


    void Handler.DeleteMethod( std.string& name)
      ''' do not delete system defined method '''
      if name == "system.describe":
        return


      for(std.list<CallbackMethod*>it = m_methods.begin() ; it != m_methods.end() ; it++)
        if (*it).GetName() == name:
          delete (*it)
          m_methods.erase(it)
          break




    bool Handler.SystemDescribe( Json.Value& msg, response)
      Json.Value methods
      response["jsonrpc"] = "2.0"
      response["id"] = msg["id"]

      for(std.list<CallbackMethod*>it = m_methods.begin() ; it != m_methods.end() ; it++)
        methods[(*it).GetName()] = (*it).GetDescription()

      
      response["result"] = methods
      return True


    std.string Handler.GetString(Json.Value value)
      return m_writer.write(value)


    bool Handler.Check( Json.Value& root, error)
      Json.Value err
      
      ''' check the JSON-RPC version => 2.0 '''
      if(not root.isObject() or not root.isMember("jsonrpc") or root["jsonrpc"] != "2.0") 
        error["id"] = Json.Value.null
        error["jsonrpc"] = "2.0"
        
        err["code"] = INVALID_REQUEST
        err["message"] = "Invalid JSON-RPC request."
        error["error"] = err
        return False


      if root.isMember("id") and (root["id"].isArray() or root["id"].isObject()):
        error["id"] = Json.Value.null
        error["jsonrpc"] = "2.0"

        err["code"] = INVALID_REQUEST
        err["message"] = "Invalid JSON-RPC request."
        error["error"] = err
        return False


      ''' extract "method" attribute '''
      if not root.isMember("method") or not root["method"].isString():
        error["id"] = Json.Value.null
        error["jsonrpc"] = "2.0"

        err["code"] = INVALID_REQUEST
        err["message"] = "Invalid JSON-RPC request."
        error["error"] = err
        return False


      return True


    bool Handler.Process( Json.Value& root, response)
      Json.Value error
      std.string method

      if not Check(root, error):
        response = error
        return False


      method = root["method"].asString()
      
      if method != "":
        rpc = Lookup(method)
        if rpc:
          return rpc.Call(root, response)


      
      ''' forge an error response '''
      response["id"] = root.isMember("id") ? root["id"] : Json.Value.null
      response["jsonrpc"] = "2.0"

      error["code"] = METHOD_NOT_FOUND
      error["message"] = "Method not found."
      response["error"] = error

      return False


    bool Handler.Process( std.string& msg, response)
      Json.Value root
      Json.Value error
      parsing = False

      ''' parsing '''
      parsing = m_reader.parse(msg, root)
      
      if not parsing:
        ''' request or batched call is not in JSON format '''
        response["id"] = Json.Value.null
        response["jsonrpc"] = "2.0"
        
        error["code"] = PARSING_ERROR
        error["message"] = "Parse error."
        response["error"] = error; 
        return False

      
      if root.isArray():
        ''' batched call '''
        i = 0
        j = 0
        
        for(i = 0 ; i < root.size() ; i++)
          Json.Value ret
          Process(root[i], ret)
          
          if ret != Json.Value.null:
            ''' it is not a notification, to array of responses '''
            response[j] = ret
            j++


        return True

      else:
        return Process(root, response)



    bool Handler.Process( char* msg, response)
      std.string str(msg)

      return Process(str, response)


    CallbackMethod* Handler.Lookup( std.string& name)
      for(std.list<CallbackMethod*>it = m_methods.begin() ; it != m_methods.end() ; it++)
        if (*it).GetName() == name:
          return (*it)



      return 0


  } ''' namespace Rpc '''

} ''' namespace Json '''

