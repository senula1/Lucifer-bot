import asyncio
import html
import os
import re
from datetime import datetime
from math import ceil

from telethon import Button, custom, events, functions
from telethon.tl.functions.users import GetFullUserRequest

from Lucifer import ALIVE_NAME, CMD_HELP, CMD_LIST, CUSTOM_PMPERMIT, bot
from Lucifer.LuciferConfig import Var

from . import *

fuk_uid = bot.uid
HELP_PIC = "https://telegra.ph/file/73373552e9217e010e853.jpg"
PMPERMIT_PIC = os.environ.get("PMPERMIT_PIC", None)
TELEPIC = (
    PMPERMIT_PIC
    if PMPERMIT_PIC
    else "https://telegra.ph/file/73373552e9217e010e853.jpg"
)
PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
myid = bot.uid
mybot = Var.TG_BOT_USER_NAME_BF_HER
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"
LOG_GP = Var.PRIVATE_GROUP_ID
MESAG = (
    str(CUSTOM_PMPERMIT)
    if CUSTOM_PMPERMIT
    else "`ππΎπΎ π·π΄ππ΄ πΈπ L U C I F E R πΏπΌ ππ΄π²πππΈππ! πΏπ»π΄π°ππ΄ ππ°πΈπ ππΈπ»π» πΌπ πΌπ°πππ΄π π°πΏπΏππΎππ΄. π€"
)
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Lucifer User"
USER_BOT_WARN_ZERO = "`πΈ π·π°ππ΄ ππ°ππ½π΄π³ ππΎπ π½πΎπ ππΎ ππΏπ°πΌ ππ. π½πΎπ ππΎπ π·π°ππ΄ π±π΄π΄π½ π±π»πΎπ²πΊπ΄π³ π°π½π³ ππ΄πΏπΎπππ΄π³ ππ½ππΈπ» π΅πππππ΄ π½πΎππΈπ²π΄.`\n\n**GoodBye!** "

if Var.LOAD_MYBOT == "True":
    USER_BOT_NO_WARN = (
        "**π·π΄π ππ·πΈπ πΈπ L U C I F E R πΏπΌ ππ΄π²πππΈππ !!! π·π΄ππ΄ ππΎ πΏππΎππ΄π²π [{}](tg://user?id={})**\n\n"
        "{}\n\n"
        "π΅πΎπ πππΆπ΄π½π π·π΄π»πΏ, πΏπΌ ππΈπ° {}"
        "\nπΏπ»π΄π°ππ΄ π²π·πΎπΎππ΄ ππ·π ππΎπ π°ππ΄ π·π΄ππ΄, π΅ππΎπΌ ππ·π΄ π°ππ°πΈπ»π°π±π»π΄ πΎπΏππΈπΎπ½\n\n".format(
            DEFAULTUSER, myid, MESAG, botname
        )
    )
elif Var.LOAD_MYBOT == "False":
    USER_BOT_NO_WARN = (
        "**πΏπΌ ππ΄π²πππΈππ πΎπ΅ [{}](tg://user?id={})**\n\n"
        "{}\n"
        "\nπΏπ»π΄π°ππ΄ π²π·πΎπΎππ΄ ππ·π ππΎπ π°ππ΄ π·π΄ππ΄, π΅ππΎπΌ ππ·π΄ π°ππ°πΈπ»π°π±π»π΄ πΎπΏππΈπΎπ½\n".format(
            DEFAULTUSER, myid, MESAG
        )
    )

CUSTOM_HELP_EMOJI = os.environ.get("CUSTOM_HELP_EMOJI", "β")
HELP_ROWS = int(os.environ.get("HELP_ROWS", 3))
HELP_COLOUMNS = int(os.environ.get("HELP_COLOUMNS", 4))

if Var.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:

    @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query.startswith("`βΟcΞΉ?Ξ΅Ρ"):
            rev_text = query[::-1]
            but = [[custom.Button.inline("π¬ Oα΄α΄Ι΄ Κα΄Κα΄ α΄α΄Ι΄α΄ Β»Β»", data="menu")]]
            but += [[custom.Button.inline("π‘ PΙͺΙ΄Ι’ Β»Β»", data="ping")]]
            but += [[Button.url("MΚ α΄α΄sα΄α΄Κ Β»Β»", "tg://user?id={fuk_uid})")]]
            but += [[custom.Button.inline("Mα΄sα΄α΄Κβ’α΄α΄α΄Κs", data="mtools")]]
            but += [[custom.Button.inline("IΙ΄ΚΙͺΙ΄α΄", data="linline")]]
            but += [
                [
                    Button.url("π° Sα΄α΄α΄α΄Κα΄ Ι’Κα΄α΄α΄ Β»Β»", "t.me/Lucifer_support_group"),
                    Button.url("π° Uα΄α΄α΄α΄α΄s α΄Κα΄Ι΄Ι΄α΄Κ", "t.me/LuciferXupdates"),
                ]
            ]
            result = builder.photo(
                file=HELP_PIC,
                text="{}\nπ²ππππ΄π½ππ»π π»πΎπ°π³π΄π³ πΏπ»ππΆπΈπ½π: {}".format(query, len(CMD_LIST)),
                buttons=but,
                link_preview=False,
            )
        elif event.query.user_id == bot.uid and query.startswith("stats"):
            result = builder.article(
                title="Stats",
                text=f"**π»π΄ππ·π°π» ππ± πππ°ππ πΎπ΅ ππ·π΄ [{DEFAULTUSER}](tg://user?id={myid})**\n\n__π±πΎπ πΈπ ππΌπΎπΎππ·π»π πππ½π½πΈπ½πΆ, πΌπ°πππ΄π!__\n\n(c) @Lucifer_support_group",
                buttons=[
                    [custom.Button.inline("Stats", data="statcheck")],
                    [Button.url("Repo", "https://github.com/kaal0408/Lucifer-X")],
                    [
                        Button.url(
                            "π³π΄πΏπ»πΎπ π½πΎπ!",
                            "https://heroku.com/deploy?template=https://github.com/kaal0408/Lucifer-X",
                        )
                    ],
                ],
            )
        elif event.query.user_id == bot.uid and query.startswith("**PM"):
            TELEBT = USER_BOT_NO_WARN.format(DEFAULTUSER, myid, MESAG)
            result = builder.photo(
                file=TELEPIC,
                text=TELEBT,
                buttons=[
                    [
                        custom.Button.inline("Request ", data="req"),
                        custom.Button.inline("Chat π­", data="chat"),
                    ],
                    [custom.Button.inline("To spam π«", data="heheboi")],
                    [custom.Button.inline("What is this β", data="pmclick")],
                ],
            )
        elif event.query.user_id == bot.uid and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"Lucifer - Telegram Userbot.",
                buttons=[
                    [
                        Button.url(
                            "L U C I F E R ππ΄πΏπΎ",
                            "https://github.com/kaal0408/Lucifer-X",
                        ),
                        Button.url(
                            "π³π΄πΏπ»πΎπ π½πΎπ",
                            "https://heroku.com/deploy?template=https://github.com/kaal0408/Lucifer-X",
                        ),
                    ],
                    [Button.url("πππΏπΏπΎππ π²π·π°π", "https://t.me/Lucifer_support_group")],
                ],
            )
        else:
            result = builder.article(
                "ππΎπππ²π΄ π²πΎπ³π΄",
                text="**Welcome to Lethal**\n\n`Click below buttons for more`",
                buttons=[
                    [
                        custom.Button.url(
                            "π Support Group π", "https://t.me/destroyxsupport"
                        )
                    ],
                    [
                        custom.Button.url(
                            "π¨βπ»Source Codeβπ»", "https://github.com/kaal0408/Lucifer-X"
                        ),
                        custom.Button.url(
                            "Deploy π",
                            "https://heroku.com/deploy?template=https://github.com/kaal0408/Lucifer-X",
                        ),
                    ],
                    [
                        custom.Button.url(
                            "Updates βοΈ", "https://t.me/Lucifer_support_group"
                        )
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(rb"helpme_next\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:  # pylint:disable=E0602
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(current_page_number + 1, CMD_LIST, "helpme")
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Please get your own Userbot from @Lucifer_support_group , and don't use mine!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"pmclick")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This ain't for you, master!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"This is the PM Security for {DEFAULTUSER} to keep away spammers and retards.\n\nProtected by [Lucifer](t.me/Lucifer_support_group)"
            )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"menu")))
    async def megic(event):
        if event.query.user_id == bot.uid:
            buttons = paginate_help(0, CMD_LIST, "helpme")
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "This bot ain't for u!!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ping")))
async def _(event):
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds
    reply_pop_up_alert = f"Κα΄α΄β’PΙͺΙ΄Ι’ = {ms} microseconds"
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"req")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This ain't for you, master!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Okay, `{DEFAULTUSER}` would get back to you soon!\nTill then please **wait patienly and don't spam here.**"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"Hey {DEFAULTUSER}, [{first_name}](tg://user?id={ok}) is **requesting** something in PM!"
            await tgbot.send_message(LOG_GP, tosend)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"chat")))
    async def on_pm_click(event):
        event.query.user_id
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This ain't for you, master!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Oho, you want to chat...\nPlease wait and see if {DEFAULTUSER} is in a mood to chat, if yes, he will be replying soon!\nTill then, **do not spam.**"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"Hey {DEFAULTUSER}, [{first_name}](tg://user?id={ok}) wants to PM you for **Random Chatting**!"
            await tgbot.send_message(LOG_GP, tosend)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"plshelpme")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This ain't for you, master!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Oh!\n{DEFAULTUSER} would be glad to help you out...\nPlease leave your message here **in a single line** and wait till I respond π"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"Hey {DEFAULTUSER}, [{first_name}](tg://user?id={ok}) wants to PM you for **help**!"
            await tgbot.send_message(LOG_GP, tosend)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"heheboi")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This ain't for you, master!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Oh, so you are here to spam π€\nGoodbye.\nYour message has been read and successfully ignored."
            )
            await borg(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            first_name = html.escape(target.user.first_name)
            await tgbot.send_message(
                LOG_GP,
                f"[{first_name}](tg://user?id={ok}) tried to **spam** your inbox.\nHenceforth, **blocked**",
            )

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            await event.edit(
                "Menu Closed!!", buttons=[Button.inline("Re-open Menu", data="reopen")]
            )
        else:
            reply_pop_up_alert = (
                "Please get your own userbot from @Lucifer_support_group "
            )
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"statcheck")))
    async def rip(event):
        text = lethalstats
        await event.answer(text, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(rb"helpme_prev\((.+?)\)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:  # pylint:disable=E0602
            current_page_number = int(event.data_match.group(1).decode("UTF-8"))
            buttons = paginate_help(
                current_page_number - 1, CMD_LIST, "helpme"  # pylint:disable=E0602
            )
            # https://t.me/TelethonChat/115200
            await event.edit(buttons=buttons)
        else:
            reply_pop_up_alert = "Please get your own Userbot, and don't use mine!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"reopen")))
    async def megic(event):
        if event.query.user_id == bot.uid:
            buttons = paginate_help(0, CMD_LIST, "helpme")
            await event.edit("Menu-Reopened", buttons=buttons)
        else:
            reply_pop_up_alert = "This bot ain't for u!!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(
        events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"us_plugin_(.*)")
        )
    )
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid:
            plugin_name = event.data_match.group(1).decode("UTF-8")
            help_string = ""
            help_string += f"Commands Available in {plugin_name} - \n"
            try:
                if plugin_name in CMD_HELP:
                    for i in CMD_HELP[plugin_name]:
                        help_string += i
                    help_string += "\n"
                else:
                    for i in CMD_LIST[plugin_name]:
                        help_string += i
                        help_string += "\n"
            except BaseException:
                pass
            if help_string == "":
                reply_pop_up_alert = "{} has no detailed info.\nUse .help {}".format(
                    plugin_name, plugin_name
                )
            else:
                reply_pop_up_alert = help_string
            reply_pop_up_alert += "\n Use .unload {} to remove this plugin\n\
                Β© Lethal".format(
                plugin_name
            )
            if len(help_string) >= 140:
                oops = "List too long!\nCheck your saved messages!"
                await event.answer(oops, cache_time=0, alert=True)
                help_string += "\n\nThis will be auto-deleted in 1 minute!"
                if bot is not None and event.query.user_id == bot.uid:
                    ok = await bot.send_message("me", help_string)
                    await asyncio.sleep(60)
                    await ok.delete()
            else:
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            reply_pop_up_alert = "Please get your own Userbot, and don't use mine!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


def paginate_help(page_number, loaded_plugins, prefix):
    number_of_rows = HELP_ROWS
    number_of_cols = HELP_COLOUMNS
    lethal = CUSTOM_HELP_EMOJI
    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [
        custom.Button.inline(
            "{} {} {}".format(lethal, x, lethal), data="us_plugin_{}".format(x)
        )
        for x in helpable_plugins
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows : number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "π‘οΈ ΦΚΙΚΙ¨ΦΚΦ", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline("βοΈ Close βοΈ", data="close"),
                custom.Button.inline(
                    "ΥΌΙΣΌΘΆ π‘οΈ", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs


async def userinfo(event):
    target = await event.client(GetFullUserRequest(event.query.user_id))
    first_name = html.escape(target.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    return first_name
