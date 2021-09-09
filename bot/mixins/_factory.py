from quora import User


class QuoraUser(User):
    def profile(self, *args, cache_exp=180, **kwargs):
        return super().profile(*args, **kwargs, cache_exp=cache_exp)

    def knows_about(self, *args, cache_exp=3600, **kwargs):
        return super().knows_about(*args, cache_exp=cache_exp, **kwargs)

    def answers(self, *args, cache_exp=300, **kwargs):
        return super().answers(*args, cache_exp=cache_exp, **kwargs)


class ObjectFactory:
    def get_quora(self, username):
        self.logger.info(f"Generating User object for {username} ")
        return QuoraUser(
            username,
            cache_manager=self._cache,
            # session=self._session,
        )
