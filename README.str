# PrimeBots Python Wrapper
****

Wrapper in Python per l'API di [prime bots](https://primebots.it/)

# Indice
***
- [Installazione](#installazione)
- [Documentazione](#documentazione)
- [Esempi](#esempi)
- [Meta](#meta)
- [Contribuzione](#contribuzione)
# Installazione
***
**È richiesta la versione di Python 3.5.3 o maggiore**

Installazione tramite pip
```bash
pip install pbpy
```

Installazione tramite source
```bash
pip3 install git+https://github.com/Polliog/primebots-py-wrapper
```

# Documentazione
***
>La documentazione verrà aggiornata col susseguirsi delle versioni

### Indice Documentazione

- [Inizializzazione](#inizializzazione)
- [Eventi](#eventi)
- [Funzioni](#funzioni)
- [Esempi](#esempi)

## Inizializzazione
```python
import pbpy

from discord.ext import commands
class PBots(commands.Cog):
    """
    Esempio di inizializzazione
    """

    def __init__(self, client):
        self.client = client
        self.token = 'API Token' #Ottenibile accedendo alla sezione API nel pannello di modifica del bot
        
        self.pb_client = pbpy.PBclient(self.client, self.token)
                
def setup(client):
    client.add_cog(PBots(client))
```

**Parametri PBclient**

 Parametro |  Descrizione 
 --------- | -----------
 `client` |  discord.Client
 `token` |  `[String]` primebots.it API Token
 `autoupdate`  | `[Bool]` Aggiornamento automatico dei server
 `logger` |  `[Bool]` Debug Logs


## Eventi
***
>Per usare gli eventi si utilizza il decorator @commands.Cog.listener() sopra una funziona col nome dell'evento da controllare piu' eventuali parametri

```python
import pbpy

from discord.ext import commands

class PBots(commands.Cog):
    """
    Esempio dell'utilizzo degli eventi all'interno di un cog
    """

    def __init__(self, client):
        self.client = client
        self.token = 'API Token' #Ottenibile accedendo alla sezione API nel pannello di modifica del bot
        
        self.pb_client = pbpy.PBclient(self.client, self.token)
        
    @commands.Cog.listener()
    async def on_count_update(self):
        """
        Questo evento avviene ogni volta che la conta dei server viene aggiornata
        """
        print("Conta dei server aggiornata")
        
    @commands.Cog.listener()
    async def on_socket_ready(self):
        """
        Questo evento avviene ogni volta che il bot si collega con successo al server dell'API
        """
        print("API pronta!")
        
    @commands.Cog.listener()
    async def on_vote(self, id):
        """
        Questo evento avviene ogni volta che il bot viene votato
        :param ID = id dell'utente che ha votato.
        """
        
        user = self.client.get_user(int(id))
        
        print(f"{user.name} ha votato il bot!")
                
def setup(client):
    client.add_cog(PBots(client))
```

## Funzioni
***
>**I nomi dei comandi usati nella documentazione sono soltanto da esempio**

```python
import pbpy
import discord

from discord.ext import commands
class PBots(commands.Cog):
    """
    Questo esempio mostra come aggiornare manualmente il contatore dei server sul sito ogni ora.
    """

    def __init__(self, client):
        self.client = client
        self.token = 'API Token' #Ottenibile accedendo alla sezione API nel pannello di modifica del bot
        
        self.pb_client = pbpy.PBclient(self.client, self.token)
                
    @commands.command()
    async def update_guilds(self):
        """
        Aggiorna manualmente il numero dei server in cui è presente il bot
        """
        
        await self.pb_client.update_guilds() #Numero dei server preso automaticamente
        
    
    @commands.command()
    async def has_voted(self, ctx, user:discord.User):
        """
        Controlla se un utente ha votato
        
        :param userID = ID dell'utente da controllare
        :return bool
        """
        
        ha_votato = await self.pb_client.has_voted(user.id)
        if ha_votato:
            print("L'utente ha votato")
        else:
            ...
        
    
    
    @commands.command()
    async def get_votes(self):
        """
        Questa funzione ti permette di ricavare una lista di tutti gli utenti che hanno votato il bot
        
        :return [ID, ID, ID]
        """
        
        lista_utenti = await self.pb_client.get_votes()
        
def setup(client):
    client.add_cog(PBots(client))
```
# Esempi
***
>Tutti gli esempi vengono eseguiti all'interno di cogs
> >Attenzione: Il numero dei server mostrati potrebbe essere minore a quello in cui è realmente il bot a causa dei nuovi limiti all'interno dell'API di discord, per attenuare il problema è consigliato avere entrambi gli [Privileged Gateway Intents](https://discordpy.readthedocs.io/en/latest/intents.html)

Aggiornamento manuale della conta dei server ogni ora:

```python
from discord.ext import commands, tasks

import pbpy

class PBots(commands.Cog):
    """
    Questo esempio mostra come aggiornare manualmente il contatore dei server sul sito ogni ora.
    """

    def __init__(self, client):
        self.client = client
        self.token = 'API Token' #Ottenibile accedendo alla sezione API nel pannello di modifica del bot
        self.pb_client = pbpy.PBclient(self.client, self.token)
        
        self.guild_count_update.start()
        
    @tasks.loop(hours=1)
    async def guild_count_update(self):
        """Loop che aggiorna ogni ora automaticamente il contatore dei server sul sito"""
        await self.client.wait_until_ready() #Aspetta che la cache del bot sia pronta, inizializzabile anche esternamente alla funzione
        await self.pb_client.update_guilds() #Prende automaticamente i server in cui e' il bot.

def setup(client):
    client.add_cog(PBots(client))
```

Aggiornamento automatico tramite autoupdate:

```python
from discord.ext import commands

import pbpy

class PBots(commands.Cog):
    """
    Questo esempio mostra come aggiornare automaticamente il contatore dei server sul sito tramite la funzione autoupdate.
    """

    def __init__(self, client):
        self.client = client
        self.token = 'API Token' #Ottenibile accedendo alla sezione API nel pannello di modifica del bot
        self.pb_client = pbpy.PBclient(self.client, self.toke, autoupdate=True) #Autoupdate = True: Aggiornamento automatico ogni ora
        
    @commands.Cog.listener()
    async def on_count_update(self):
        print("Conta dei server aggiornata")

def setup(client):
    client.add_cog(PBots(client))
```

# Meta
***
Libreria distribuita sotto licenza [MIT License](https://github.com/Polliog/primebots-py-wrapper/blob/master/LICENSE.txt). Consulta `LICENSE` per maggiori informazioni.

# Contribuzione
***
1. **Fork** la repo (https://github.com/Polliog/primebots-py-wrapper/fork)
2. **Clone** il progetto
3. **Commit** usando il tuo branch
4. **Push** il tuo lavoro nel tuo fork
5. Invita una **Pull request** in modo da poter controllare i tuoi cambiamenti
