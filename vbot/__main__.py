#    This file is part of the Vc distribution.
#    Copyright (c) 2021 kaif-00z
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    License can be found in < https://github.com/kaif-00z/VcBot/blob/main/License> .


from . import *

LOGS.info("Starting...")

try:
    user.start()
except Exception as erc:
    LOGS.info(erc)

group_call_factory = GroupCallFactory(
    user, GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON
)
VC = {}


@user.on(events.NewMessage(outgoing=True, pattern="\\.ping"))
async def ping(event):
    t = time.time()
    x = await event.edit("Pɪɴɢ!!!")
    tt = time.time() - t
    p = float(str(tt)) * 1000
    await x.edit(f"Pɪɴɢ: {int(p)}ms")


@user.on(events.NewMessage(outgoing=True, pattern="\\.help"))
async def help(event):
    await event.edit(
        """
        **Available Commands**:\n
        • `.play <youtube link>` - This command play Audio in Vc.\n
        • `.playvideo <youtube link>` - This command play Video in Vc.\n
        • `.stopvc` - This command stop Vc.\n
        • `.pausevc` - This command pause Vc.\n
        • `.resumevc` - This command resume Vc.\n
        • `.mutevc` - This command mute Vc.\n
        • `.unmutevc` - This command unmute Vc.
       """
    )


@user.on(events.NewMessage(outgoing=True, pattern="\\.play ?(.*)"))
async def play(event):
    link = event.pattern_match.group(1)
    c_id = event.chat_id
    x = await event.edit("`Downloading & Converting...`")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(id)s.mp3",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"{link}"])
        info_dict = ydl.extract_info(link, download=False)
        audio_id = info_dict.get("id") + ".mp3"
    group_call = group_call_factory.get_group_call()
    await group_call.join(event.chat_id)
    await group_call.start_audio(f"{audio_id}")
    VC[c_id] = group_call
    await x.edit(f"`✓Joined Vc Sucessfully in {event.chat_id}.`")


@user.on(events.NewMessage(outgoing=True, pattern="\\.playvideo ?(.*)"))
async def playvideo(event):
    c_id = event.chat_id
    xx = await event.edit("`Converting...`")
    link = event.pattern_match.group(1)
    n = pafy.new(link)
    video = n.getbest().url
    group_call = group_call_factory.get_group_call()
    await group_call.join(event.chat_id)
    await group_call.start_video(f"{video}")
    VC[c_id] = group_call
    await xx.edit(f"`✓Joined Vc Sucessfully in {event.chat_id}.`")


@user.on(events.NewMessage(outgoing=True, pattern="\\.stopvc"))
async def stopvc(event):
    try:
        await VC[event.chat_id].stop()
        await event.edit(f"`✓Successfully Left the Vc in {event.chat_id}.`")
    except BaseException:
        await event.edit(f"`✘Error while Lefting the Vc in {event.chat_id}.`")


@user.on(events.NewMessage(outgoing=True, pattern="\\.pausevc"))
async def pause(event):
    try:
        await VC[event.chat_id].set_pause(True)
        await event.edit(f"`✓Sucessfully pause the Vc in {event.chat_id}`.")
    except BaseException:
        await event.edit(f"`✘Error while pausing the Vc in {event.chat_id}.`")


@user.on(events.NewMessage(outgoing=True, pattern="\\.resumevc"))
async def resume(event):
    try:
        await VC[event.chat_id].set_pause(False)
        await event.edit(f"`✓Sucessfully resume the Vc in {event.chat_id}.`")
    except BaseException:
        await event.edit(f"`✘Error while resuming the Vc in {event.chat_id}.`")


@user.on(events.NewMessage(outgoing=True, pattern="\\.mutevc"))
async def mute(event):
    try:
        await VC[event.chat_id].set_is_mute(True)
        await event.edit(f"`✓Sucessfully mute the Vc in {event.chat_id}.`")
    except BaseException:
        await event.edit(f"`✘Error while muting the Vc in {event.chat_id}.`")


@user.on(events.NewMessage(outgoing=True, pattern="\\.unmutevc"))
async def unmute(event):
    try:
        await VC[event.chat_id].set_is_mute(False)
        await event.edit(f"`✓Sucessfully unmute the Vc in {event.chat_id}.`")
    except BaseException:
        await event.edit(f"`✘Error while unmuting the Vc in {event.chat_id}.`")


LOGS.info("Bot has started...")
user.run_until_disconnected()
