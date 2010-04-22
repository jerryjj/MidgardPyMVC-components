import logging
log = logging.getLogger(__name__)

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.i18n.translation import _

from midgardmvc.lib.base import BaseController, render
import midgardmvc.lib.helpers as h

import time
import simplejson
import datetime

from cogen.core import queue, events
from cogen.core.coroutines import coro
from cogen.core.pubsub import PublishSubscribeQueue
from cogen.core.util import priority

pubsub = PublishSubscribeQueue()

class Client:
    def __init__(self, name):
        self.messages = queue.Queue(10)
        self.dead = False
        self.name = name
    
    @coro
    def watch(self):
        """This is a coroutine that runs permanently for each participant to the
        chat. If the participant has more than 10 unpulled messages this
        coroutine will die.

        `pubsub` is a queue that hosts the messages from all the
        participants.
          * subscribe registers this coro to the queue
          * fetch pulls the recent messages from the queue or waits if there
        are no new ones.

        self.messages is another queue for the frontend comet client (the
        pull action from the ChatController will pop messages from this queue)
        """
        yield pubsub.subscribe()
        while 1:
            messages = yield pubsub.fetch()
            print messages
            try:
                yield self.messages.put_nowait(messages)
            except:
                print 'Client %s is dead.' % self
                self.dead = True
                break

class PostController(BaseController):
    
    def new(self):
        """This action puts a message in the global queue that all the clients
        will get via the 'pull' action."""
        
        message = dict(
            content=request.POST['content']
        )
        
        yield request.environ['cogen.call'](pubsub.publish)(
            message
        )
        
        yield simplejson.dumps(message)
    
    def queue(self):
        """This action does some state checking (adds a object in the session
        that will identify this chat participant and adds a coroutine to manage
        it's state) and gets new messages or bail out in 10 seconds if there are
        no messages."""
        if not 'client' in session or session['client'].dead:
            client = Client("chat_demo")
            session['client'] = client
            session.save()
            yield request.environ['cogen.core'].events.AddCoro(client.watch, prio=priority.CORO)
            return
        else:
            client = session['client']

        yield request.environ['cogen.call'](client.messages.get)(timeout=10)

        if isinstance(request.environ['cogen.wsgi'].result, events.OperationTimeout):
            pass
        elif isinstance(request.environ['cogen.wsgi'].result, Exception):
            import traceback
            traceback.print_exception(*request.environ['cogen.wsgi'].exception)
        else:
            yield simplejson.dumps(request.environ['cogen.wsgi'].result)