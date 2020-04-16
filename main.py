#!/usr/bin/env python

import logging
import subprocess

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          InlineQueryHandler, Filters,
                          MessageHandler, Updater)

from config import TOKEN, ACCEPTEDUSERS

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

updater = Updater(TOKEN, use_context=True)



def log(msg):
    """TODO: Docstring for log.

    :msg: TODO
    :returns: TODO

    """
    print(msg)
    os.system('notify-send "{}"'.format(msg))

def bothelp(update, context):
    """
    Docstr
    """
    update.message.reply_text("Use /start to test this bot.")


def error(update, context):
    """Log Errors caused by Updates."""
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


def sync(update, context):
    try:
        invoke('sync', ANKIPORTS[update.effective_user.id])
        update.message.reply_text('Done')
    except:
        update.message.reply_text('Error')


def status(update, context):
    """
    Docstr
    """
    update.message.reply_text(str(update)+'\n'+str(context))


def inline_handler(update, context):
    context.bot.answer_inline_query(update.inline_query.id, results=[
                                    InlineQueryResultArticle('art1', 'titel', InputTextMessageContent('message'))])

from python_mpv_jsonipc import MPV
import os
os.environ['PATH'] += os.pathsep + os.path.expanduser('~/.local/bin')
class TelMedia(object):

    """Docstring for TelMedia. """

    def __init__(self):
        """TODO: to be defined. """
        self.lastmsg = 'www.youtube.com'

    def show_url(self, msg):
        """TODO: Docstring for show_url.

        :url: TODO
        :returns: TODO

        """
        if 'ori.mn' in msg or 'instagram.com' in msg:
            os.system('qutebrowser -B ~/.local/share/qutebrowser_kodi {} & disown'.format(msg))
            return
        elif 'reddit.com' in msg:
            os.system('qutebrowser -B ~/.local/share/qutebrowser_kodi {} & disown'.format(msg))
            return
        elif 'www.youtube.com' == msg:
            os.system('qutebrowser -B ~/.local/share/qutebrowser_kodi {} & disown'.format(msg))
            return



        # Use MPV that is running and connected to /tmp/mpv-socket.
        try:
            mpv = MPV(start_mpv=False, ipc_socket="/tmp/tmpmpvsocket")
        except ConnectionRefusedError:
            mpv = MPV(ipc_socket="/tmp/tmpmpvsocket", keep_open=True,
                      title='[telmedia_mpv]', fullscreen=True)
        except FileNotFoundError:
            mpv = MPV(ipc_socket="/tmp/tmpmpvsocket", keep_open=True,
                      title='[telmedia_mpv]', fullscreen=True)
        # You can also send commands.
        mpv.play(msg)
        mpv.command('set', 'pause', 'no')
        return

    def isaccepted(self, uid):
        """TODO: Docstring for isaccepted.

        :uid: TODO
        :returns: TODO

        """
        return uid in ACCEPTEDUSERS

    def replay(self, update, context):
        if not self.isaccepted(update.effective_user.id):
            update.message.reply_text(text='Not authorized.')
            return
        log('Replaying {}'.format(self.lastmsg))
        self.show_url(self.lastmsg)

    def play(self, update, context):
        if not self.isaccepted(update.effective_user.id):
            update.message.reply_text(text='Not authorized.')
            return

        if not context.args is None:
            msg = ' '.join(context.args)
        else:
            msg = update.message.text
        self.lastmsg = msg
        log('Recieved {} from {}'.format(msg, update.effective_user.first_name))
        self.show_url(msg)



def unknown(update, context):
    """
    Docstr
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")

def main():
    """
    Docstr
    """
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    #  updater.dispatcher.add_handler(CommandHandler('sync', sync))
    #  updater.dispatcher.add_handler(InlineQueryHandler(inline_handler))
    #  updater.dispatcher.add_handler(
        #  CommandHandler('ankiaudio', allgame.anki_audio))
    telmedia = TelMedia()
    updater.dispatcher.add_handler(CommandHandler('r', telmedia.replay))
    #  updater.dispatcher.add_handler(CommandHandler('list', allgame.listgames))

    #  updater.dispatcher.add_error_handler(error)

    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.dispatcher.add_handler(MessageHandler(Filters.text, telmedia.play))
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
