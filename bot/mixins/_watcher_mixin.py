from quora import User


class WatcherMixin:
    """"Mixin class for watcher."""

    async def load_watcher_data(self):
        self.watcher_list = {}
        for guild in self.guilds:
            guild_watcher = self.db.get_guild_watcher(guild.id)
            for watcher in guild_watcher:
                update_channel = self.db.get_update_channel(guild.id)
                user = self.db.get_user(user_id=watcher.user_id)
                if user.quora_username not in self.watcher_list.keys():
                    data_dict = {
                        "user_id": user.user_id,
                        "dispatch_to": [
                            {
                                "channel_id": update_channel,
                                "discord_id": user.discord_id,
                            }
                        ],
                    }
                    self.watcher_list[user] = data_dict
                else:
                    data = self.watcher_list[user.quora_username]
                    ls = data["dispatch_to"]
                    ls.append(
                        {
                            "channel_id": update_channel,
                            "discord_id": user.discord_id,
                        }
                    )
                    data["dispatch_to"] = ls
                    self.watcher_list[user.quora_username] = data
        for user, data in self.watcher_list.items():
            if user.answer_count and user.follower_count:
                self.watcher.add_quora(
                    user.quora_username,
                    update_interval=900,
                    data_dict=data,
                    stateInitializer=self.stateCustomizer(
                        user.answer_count, user.follower_count
                    ),
                )
            else:
                u = User(
                    user.quora_username,
                    cache_manager=self._cache,
                    session=self._session,
                )
                u = await u.profile()

                self.db.update_follower_count(user.user_id, u.followerCount)
                self.db.update_answer_count(user.user_id, u.answerCount)
                self.watcher.add_quora(
                    user.quora_username,
                    update_interval=600,
                    data_dict=data,
                )

    def stateCustomizer(
        self,
        answerCount: int,
        followerCount: int,
    ):
        def wrapper(obj):
            obj.answerCount = answerCount
            obj.followerCount = followerCount
            return obj

        return wrapper
