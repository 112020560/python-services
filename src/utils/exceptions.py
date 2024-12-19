class DBError(Exception):
    pass


class DoesNotExistError(DBError):
    pass


class IntegrityError(DBError):
    pass


class ServiceError(Exception):
    pass


class MessageValidationError(ServiceError):
    pass


class MissingMessageFieldError(MessageValidationError):
    pass


class InvalidMessageFieldError(MessageValidationError):
    pass


class InsufficientBalanceError(ServiceError):
    pass


class UnlockCardError(Exception):
    pass


class LockCardError(Exception):
    pass


class MissingBinError(Exception):
    pass


class InvalidSnsPayloadError(Exception):
    pass


class DeletedDigitalizationCardError(DBError):
    pass
