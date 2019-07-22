class EhError(Exception):
    pass


class TopicError(EhError):
    pass


class TopicStoreInvalidRoot(EhError):
    pass


class TopicInvalidRootPath(EhError):
    pass


class InvalidValue(EhError):
    pass


class UnimplementedFeature(EhError):
    pass
