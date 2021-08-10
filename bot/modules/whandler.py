from watcher.events.quora import (
    AnswerCountChange,
    FollowerCountChange,
)
from database import userprofile_api as api


@bot.watcher.dispatcher.on(AnswerCountChange)
async def inform_answer_count_change(event):
    destinations = event.data_dict["dispatch_to"]
    user_id = event.data_dict["user_id"]
    api.update_answer_count(user_id, event.countChange)
    if event.countChange >= 1:
        for dest in destinations:
            channel = await bot.fetch_channel(dest["channel_id"])
            await channel.send(
                f"Congratulations!!  <@{dest['discord_id']}> for writing {event.countChange} answer  on Quora.\nCurrent Answer count: {event.newCount}"
            )
    else:
        for dest in destinations:
            channel = await bot.fetch_channel(dest["channel_id"])
            await channel.send(
                f"Hii!!  <@{dest['discord_id']}> {abs(event.countChange)} answer(s) is/are not visible on your profile. If you haven't deleted them, it may have collapsed or deleted by Quora.\nCurrent Asnwer Count: {event.newCount}"
            )


@bot.watcher.dispatcher.on(FollowerCountChange)
async def inform_follower_count_change(event):
    destinations = event.data_dict["dispatch_to"]
    user_id = event.data_dict["user_id"]
    api.update_follower_count(user_id, event.countChange)
    if event.countChange >= 1:
        for dest in destinations:
            channel = await bot.fetch_channel(dest["channel_id"])
            await channel.send(
                f"Congratulations!!  <@{dest['discord_id']}> , you got {event.countChange} new follower(s) on Quora.\nCurrent follower count: {event.newCount}"
            )
    else:
        for dest in destinations:
            channel = await bot.fetch_channel(dest["channel_id"])
            await channel.send(
                f"Hii!! <@{dest['discord_id']}> {abs(event.countChange)} people unfollowed you on Quora.\nCurrent Follower Count: {event.newCount}"
            )
