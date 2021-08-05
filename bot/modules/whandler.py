from watcher.events.quora import (
    AnswerCountChange,
    FollowerCountChange,
)


@bot.watcher.dispatcher.on(AnswerCountChange)
async def inform_answer_count_change(event):
    destinations = event.data_dict["dispatch_to"]
    if event.countChange >= 1:
        for dest in destinations:
            channel = await bot.fetch_channel(dest["channel_id"])
            await channel.send(
                f"Congratulations!!  <@{dest['discord_id']}> for writing {event.countChange} answer  on Quora."
            )
    else:
        for dest in destinations:
            channel = await bot.fetch_channel(dest["channel_id"])
            await channel.send(
                f"Hii!!  <@{dest['discord_id']}> {abs(event.countChange)} answer(s) is/are not visible on your profile. If you haven't deleted them, it may have collapsed or deleted by Quora."
            )
