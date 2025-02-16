from error import InternalError

# A hook for all message sending
async def send_message(target, msg: str):
    if not callable(getattr(target, "send", None)):
        raise InternalError(f"getting target without \"send\" methhod: {target}")
    
    await target.send(msg)