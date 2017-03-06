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
 * \file jsonrpc_tcpserver.h
 * \brief JSON-RPC TCP server.
 * \author Sebastien Vincent
 '''

#ifndef JSONRPC_TCPSERVER_H
#define JSONRPC_TCPSERVER_H

#include <list>

#include "jsonrpc_common.h"
#include "jsonrpc_server.h"

namespace Json

  namespace Rpc
    '''*
     * \class TcpServer
     * \brief JSON-RPC TCP server implementation.
     '''
    class TcpServer : public Server
      public:
        '''*
         * \brief Constructor.
         * \param address network address or FQDN to bind
         * \param port local port to bind
         '''
        TcpServer( std.string& address, port)

        '''*
         * \brief Destructor.
         '''
        virtual ~TcpServer()

        '''*
         * \brief Receive data from the network and process it.
         * \param fd socket descriptor to receive data
         * \return True if message has been correctly received, and
         * response sent, otherwise (mainly send/recv error)
         * \note This method will blocked until data comes.
         '''
        virtual bool Recv(int fd)

        '''*
         * \brief Send data.
         * \param fd file descriptor of the client TCP socket
         * \param data data to send
         * \return number of bytes sent or -1 if error
         '''
        virtual ssize_t Send(int fd, data)

        '''*
         * \brief Wait message.
         *
         * This function do a select() on the socket and Process() immediately 
         * the JSON-RPC message.
         * \param ms millisecond to wait (0 means infinite)
         '''
        virtual void WaitMessage(uint32_t ms)

        '''*
         * \brief Put the TCP socket in LISTEN state.
         '''
        bool Listen()

        '''*
         * \brief Accept a client socket.
         * \return -1 if error, otherwise
         '''
        bool Accept()
        
        '''*
         * \brief Close listen socket and all client sockets.
         '''
        void Close()

        '''*
         * \brief Get the list of clients.
         * \return list of clients
         '''
         std.list<int> GetClients()

      private:
        '''*
         * \brief List of client sockets.
         '''
        std.list<int> m_clients

        '''*
         * \brief List of disconnected sockets to be purged.
         '''
        std.list<int> m_purge


  } ''' namespace Rpc '''

} ''' namespace Json '''

#endif ''' JSONRPC_TCPSERVER_H '''

