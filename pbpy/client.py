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
import logging

import requests
import discord
import json
import asyncio
import socketio

from . import errors


class PBclient:
    """
    Rappresenta un client che si connette a primebots.it

    Questa classe interagisce direttamente con l'API di primebots.it

    `Va inizializzata prima di poter eseguire le altre funzioni.`
    """

    client: discord.Client

    def __init__(self, client: discord.Client, token: str, autoupdate: bool = False, logger: bool = False, **kwargs):
        """
        :param client: Discord Client
        :param token: primebots.it API Token
        :param autoupdate: Auto-Aggiornamento dei server riportati sul sito
        :param logger: Debug Logs
        """
        self.socket = socketio.AsyncClient(logger=logger)

        self.token = token
        self.client = client
        self.client_id = None
        self.auto_update = autoupdate
        self.loop = kwargs.get("loop", client.loop)

        self.loop.create_task(self._socket_connect())

        self.loop.create_task(self._socket_logger())

        if self.auto_update:
            self._auto_update_task = self.loop.create_task(self._auto_update())

    async def update_guilds(self):
        """
        Aggiorna manualmente il contatore di server presente sul sito, prende in maniera automatica la quantita di server in cui e' presente il bot
        """
        req = requests.post(url='https://primebots.it/api/' + str(self.client.user.id) + '/guilds/' + self.token,
                            headers={'content-type': 'application/json'},
                            data=json.dumps({'botGuilds': len([x for x in self.client.guilds])}))
        self.client.dispatch('count_update')  # on_count_update
        if req.status_code == 401:
            logging.error("API Token non valido")
            return

    async def has_voted(self, userID):
        """
        Controlla se un utente ha votato

        :param userID: ID dell'utente
        :return: bool
        """
        await self._ensure_user_bot()
        req = requests.get(
            'https://primebots.it/api/' + str(self.client.user.id) + '/vote/' + str(userID) + '/' + self.token)
        if req.status_code == 401:
            logging.error("API Token non valido")
            return
        res = req.json()
        return res['hasVoted']

    async def get_votes(self) -> [int]:
        """
        Da come return una lista contenente gli ID degli utenti che hanno votato il bot.

        :return: [ID, ID]
        """
        await self._ensure_user_bot()
        req = requests.get('https://primebots.it/api/' + str(self.client.user.id) + '/votes/' + self.token)
        if req.status_code == 401:
            logging.error("API Token non valido")
            return
        res = req.json()
        return res['votes']

    async def _ensure_user_bot(self):
        # Controlla se la cache del bot e' pronta
        await self.client.wait_until_ready()
        if self.client_id is None:
            self.client_id = self.client.user.id

    async def _auto_update(self):
        # Aggiorna automaticamente il guild counter ogni ora. ~Loop gestito dal client~
        await self._ensure_user_bot()
        while not self.client.is_closed():
            try:
                await self.update_guilds()
                self.client.dispatch('count_update')  # on_count_update
            except errors.HTTPException:
                pass
            await asyncio.sleep(3600)

    async def _socket_connect(self):
        # ~Loop gestito dal client~
        if not self.socket.connected:
            await self.socket.connect('https://primebots-api-js.herokuapp.com')
            await asyncio.sleep(5)  # Aspetta che la connessione sia pronta
            await self.socket.emit('createRoom', data=self.token)

    async def _socket_logger(self):
        # Controlla gli eventi e li manda al bot.
        # ~Loop gestito dal client~
        self.socket.on('ok', handler=self._on_socket_ok)
        self.socket.on('newVote', handler=self._on_socket_newvote)
        await asyncio.sleep(0.5)

    def _on_socket_ok(self):
        # on_socket_ready
        self.client.dispatch('socket_ready')

    def _on_socket_newvote(self, sid):
        # on_vote(data)
        self.client.dispatch('vote', sid['id'])
