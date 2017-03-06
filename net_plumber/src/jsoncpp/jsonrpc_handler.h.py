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
 * \file jsonrpc_handler.h
 * \brief JSON-RPC server processor engine.
 * \author Sebastien Vincent
 '''

#ifndef JSONRPC_HANDLER_H
#define JSONRPC_HANDLER_H

#include <cstdio>

#include <string>
#include <list>

#include "json/json.h"

#include "jsonrpc_common.h"

namespace Json 

  namespace Rpc
    '''*
     * \class CallbackMethod
     * \brief Abstract callback-style method.
     * \see RpcMethod
     '''
    class CallbackMethod
      public:
        '''*
         * \brief Destructor.
         '''
        virtual ~CallbackMethod()

        '''*
         * \brief Call the method.
         * \param msg JSON-RPC request or notification
         * \param response response produced (may be Json.Value.null)
         * \return True if message has been correctly processed, otherwise
         * \note Have to be implemented by subclasses
         '''
        virtual bool Call( Json.Value& msg, response) = 0

        '''*
         * \brief Get the name of the methods (optional).
         * \return name of the method as std.string
         * \note Have to be implemented by subclasses
         '''
        virtual std.string GetName()  = 0

        '''*
         * \brief Get the description of the methods (optional).
         * \return description
         '''
        virtual Json.Value GetDescription()  = 0


    '''*
     * \class RpcMethod
     * \brief Template class that represent the RPC method.
     *
     * Typically RpcMethod object is created inside another class and use
     * a method of self class. See Handler class documentation for an example
     * of how to use RpcMethod class.
     *
     * \warning As class keep pointer of object reference, should take 
     * care at the lifetime of object you pass in RpcMethod constructor,
     * else it could lead to crash your program.
     '''
    template<class T> class RpcMethod : public CallbackMethod
      public:
        '''*
         * \typedef Method
         * \brief T method signature.
         '''
        typedef bool (T.*Method)( Json.Value& msg, response)

        '''*
         * \brief Constructor.
         * \param obj object
         * \param method class method
         * \param name symbolic name (i.e. system.describe)
         * \param description method description (in JSON format)
         '''
        RpcMethod(T& obj, method, name, description = Json.Value.null)
          m_obj = &obj
          m_name = name
          m_method = method
          m_description = description


        '''*
         * \brief Call the method.
         * \param msg JSON-RPC request or notification
         * \param response response produced (may be Json.Value.null)
         * \return True if message has been correctly processed, otherwise
         * \note JSON-RPC's notification method MUST set response to Json.Value.null
         '''
        virtual bool Call( Json.Value& msg, response)
          return (m_obj.*m_method)(msg, response)


        '''*
         * \brief Get the name of the methods (optional).
         * \return name of the method as std.string
         '''
        virtual std.string GetName()
          return m_name


        '''*
         * \brief Get the description of the methods (optional).
         * \return description
         '''
        virtual Json.Value GetDescription()
          return m_description


      private:
        '''*
         * \brief Object pointer.
         '''
        T* m_obj

        '''*
         * \brief Method of T class.
         '''
        Method m_method

        '''*
         * \brief Symbolic name.
         '''
        std.string m_name

        '''*
         * \brief JSON-formated description of the RPC method.
         '''
        Json.Value m_description


    '''*
     * \class Handler
     * \brief Container of methods which can be called remotely.
     *
     * Preferred use of self class is to construct RpcMethod inside
     * another class and pass <code>*self</code> as obj parameter:\n
     * \n
     * \code
     * class MyClass
     *     *    public:
     *      void Init()
     *     *        method = RpcMethod<MyClass>(*self, &MyClass.RemoteMethod, std.string("remote_method"), std.string("Description"))
     *        m_handler.AddMethod(method)
     *
     *
     *      bool RemoteMethod( Json.Value& msg, response)
     *     *        # do stuff
     *
     *
     *    private:
     *      Handler m_handler
     *
     * \endcode
     * \note Always pass it in function with reference (i.e. void foo(Json.Rpc.Handler& handler)).
     * \see RpcMethod
     '''
    class Handler
      public:
        '''*
         * \brief Constructor.
         '''
        Handler()

        '''*
         * \brief Destructor.
         '''
        virtual ~Handler()

        '''*
         * \brief Add a RPC method.
         * \param method RPC method to add (MUST be dynamically allocated using new)
         * \note Json.Rpc.Handler object takes care of freeing method memory.\n
         * The way of calling self method is:
         * <code>
         * handler.AddMethod(new RpcMethod<MyClass>(...))
         * </code>
         * \warning The "method" parameter MUST be dynamically allocated (using new).
         '''
        void AddMethod(CallbackMethod* method)

        '''*
         * \brief Remote a RPC method.
         * \param name name of the RPC method
         '''
        void DeleteMethod( std.string& name)

        '''*
         * \brief Process a JSON-RPC message.
         * \param msg JSON-RPC message as std.string
         * \param response JSON-RPC response (could be Json.Value.null)
         * \return True if the request has been correctly processed, otherwise
         * (may be caused by parsed error, ...)
         * \note in case msg is a notification, is equal to Json.Value.null 
         * and the return value is True.
         '''
        bool Process( std.string& msg, response)

        '''*
         * \brief Process a JSON-RPC message.
         * \param msg JSON-RPC message as C-String
         * \param response JSON-RPC response (could be Json.Value.null)
         * \return True if the request has been correctly processed, otherwise (may be
         * caused by parsed error, ...)
         * \note in case msg is a notification, is equal to Json.Value.null 
         * and the return value is True.
         '''
        bool Process( char* msg, response)

        '''*
         * \brief RPC method that get all the RPC methods and their description.
         * \param msg request
         * \param response response
         * \return True if processed correctly, otherwise
         '''
        bool SystemDescribe( Json.Value& msg, response)

        '''*
         * \brief Get a std.string representation of Json.Value.
         * \param value JSON message
         * \return string representation
         '''
        std.string GetString(Json.Value value)

      private:
        '''*
         * \brief JSON reader.
         '''
        Json.Reader m_reader

        '''*
         * \brief JSON writer.
         '''
        Json.FastWriter m_writer

        '''*
         * \brief List of RPC methods.
         '''
        std.list<CallbackMethod*> m_methods

        '''*
         * \brief Find CallbackMethod by name.
         * \param name name of the CallbackMethod
         * \return a CallbackMethod pointer if found, otherwise
         '''
        CallbackMethod* Lookup( std.string& name)

        '''*
         * \brief Check if the message is a valid JSON object one.
         * \param root message to check validity
         * \param error complete JSON-RPC error message if method failed
         * \return True if the message is a JSON one, otherwise
         '''
        bool Check( Json.Value& root, error)

        '''*
         * \brief Process a JSON-RPC object message.
         * \param root JSON-RPC message as Json.Value
         * \param response JSON-RPC response that will be filled in self method
         * \return True if the request has been correctly processed, otherwise 
         * (may be caused by parsed error, ...)
         * \note In case msg is a notification, is equal to Json.Value.null 
         * and the return value is True.
         '''
        bool Process( Json.Value& root, response)


  } ''' namespace Rpc '''

} ''' namespace Json '''

#endif ''' JSONRPC_HANDLER_H '''

